package com.glaziola.pixelmonrejuvenated;

import com.google.gson.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.FluidTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.loading.FMLPaths;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

/**
 * Pixelmon 9.4.1 legendary spawn rules, implemented as a separate global timed
 * spawner. We do NOT inject legendary entries into Cobblemon's ordinary pools,
 * avoiding thousands of regular natural spawn attempts and incorrect frequency.
 *
 * The data is derived from Pixelmon's spawning/legendaries/*.set.json; biome
 * tags are ported to pixelmonrejuvenated:spawning/*. The engine preserves
 * species, levels, biome restrictions/exclusions, weather, height, moon, time,
 * weighted rarity, vanilla structure restrictions, and location categories.
 */
public final class LegendarySpawnEngine {
    private static final Random RANDOM = new Random();
    private static final WeakHashMap<MinecraftServer, TimerState> SERVERS = new WeakHashMap<>();
    private static final List<Rule> RULES = loadRules();
    private static final String CONFIG_NAME = "pixelmonrejuvenated-legendary-spawns.json";
    private LegendarySpawnEngine() { }
    public static void register() {net.neoforged.neoforge.common.NeoForge.EVENT_BUS.register(LegendarySpawnEngine.class);}

    @SubscribeEvent
    public static void onServerTick(ServerTickEvent.Post event) {
        MinecraftServer server = event.getServer();
        if (server.getPlayerList().getPlayers().isEmpty()) return;
        TimerState state = SERVERS.computeIfAbsent(server, s -> {
            Config settings = Config.load();
            return new TimerState(settings, delay(settings, server.getPlayerCount()));
        });
        if (!state.config.enabled || RULES.isEmpty()) return;
        if (--state.ticksRemaining > 0) return;
        state.ticksRemaining = delay(state.config, server.getPlayerCount());
        try { attempt(server, state.config); }
        catch (Exception exception) {
            System.err.println("[Pixelmon Rejuvenated] Legendary spawn check failed: " + exception);
        }
    }

    /** One chosen online player, like Pixelmon's shared legendary-spawn timer. */
    private static void attempt(MinecraftServer server, Config cfg) {
        List<ServerPlayer> players = server.getPlayerList().getPlayers().stream()
                .filter(p -> p.isAlive() && !p.isSpectator() && p.serverLevel() instanceof ServerLevel)
                .toList();
        if (players.isEmpty()) return;
        ServerPlayer player = players.get(RANDOM.nextInt(players.size()));
        ServerLevel level = player.serverLevel();
        List<Candidate> eligible = new ArrayList<>();
        BlockPos center = player.blockPosition();
        // Different blocks and biomes can all compete in one attempt. Only
        // existing loaded chunks are examined. No forced chunk generation.
        for (int i = 0; i < cfg.searchAttempts; i++) {
            double angle = RANDOM.nextDouble() * (Math.PI * 2.0D);
            double distance = cfg.minDistance + RANDOM.nextDouble() * (cfg.maxDistance - cfg.minDistance);
            int x = center.getX() + (int)Math.round(Math.cos(angle) * distance);
            int z = center.getZ() + (int)Math.round(Math.sin(angle) * distance);
            BlockPos probe = new BlockPos(x, center.getY(), z);
            if (!level.getChunkSource().hasChunk(x >> 4, z >> 4)) continue;
            for (Rule rule : RULES) {
                if (!matchesWorld(rule, level, probe)) continue;
                BlockPos spawn = selectSpot(rule, level, x, z);
                if (spawn == null) continue;
                if (!matchBiomeList(rule.biomes,level,spawn,true) || matchBiomeList(rule.excludedBiomes,level,spawn,false)) continue;
                if (!rule.structures.isEmpty() && !withinRequestedStructure(rule,level,spawn)) continue;
                if ((long)(spawn.getX()-center.getX())*(spawn.getX()-center.getX()) + (long)(spawn.getZ()-center.getZ())*(spawn.getZ()-center.getZ()) < (long)cfg.minDistance * cfg.minDistance) continue;
                eligible.add(new Candidate(rule, spawn));
            }
        }
        if (eligible.isEmpty() || RANDOM.nextDouble() >= cfg.spawnChance) return;
        Candidate selected = weightedChoice(eligible);
        if (selected == null) return;
        spawnAndAnnounce(server, player, level, selected, cfg);
    }

    private static boolean matchesWorld(Rule r, ServerLevel level, BlockPos position) {
        long time = Math.floorMod(level.getDayTime(), 24000L);
        if (!r.times.isEmpty() && r.times.stream().noneMatch(t -> timeMatches(t, time))) return false;
        if (r.moonPhase >= 0 && level.getMoonPhase() != r.moonPhase) return false;
        if (!r.weathers.isEmpty()) {
            String weather = level.isThundering() ? "STORM" : (level.isRaining() ? "RAIN" : "CLEAR");
            if (!r.weathers.contains(weather)) return false;
        }
        return true;
    }

    /** Does not load absent tags or assume Pixelmon is installed. */
    private static boolean matchBiomeList(List<String> references, ServerLevel level, BlockPos pos, boolean emptyMeansAny) {
        if (references.isEmpty()) return emptyMeansAny;
        Holder<Biome> biome = level.getBiome(pos);
        for (String ref : references) {
            try {
                if (ref.startsWith("#")) {
                    TagKey<Biome> tag = TagKey.create(Registries.BIOME, ResourceLocation.parse(ref.substring(1)));
                    if (biome.is(tag)) return true;
                } else if (biome.is(ResourceLocation.parse(ref))) return true;
            } catch (IllegalArgumentException ignored) { }
        }
        return false;
    }

    private static boolean withinRequestedStructure(Rule rule, ServerLevel level, BlockPos pos) {
        // Pixelmon-only generated structures cannot be assumed to exist.
        // Vanilla structures are checked against structures actually containing
        // this candidate point. A missing structure is not silently ignored.
        var structures = level.structureManager().getAllStructuresAt(pos);
        var registry = level.registryAccess().registryOrThrow(Registries.STRUCTURE);
        for (Structure structure : structures.keySet()) {
            ResourceLocation id = registry.getKey(structure);
            if (id != null && rule.structures.contains(id.toString()) && level.structureManager().getStructureWithPieceAt(pos,structure).isValid()) return true;
        }
        return false;
    }

    static boolean timeMatches(String name, long tick) {
        return switch(name) {
            case "DAWN" -> tick >= 23000 || tick < 1000;
            case "MORNING" -> tick >= 0 && tick < 6000;
            case "DAY" -> tick >= 0 && tick < 12000;
            case "AFTERNOON" -> tick >= 6000 && tick < 12000;
            case "DUSK" -> tick >= 12000 && tick < 13000;
            case "NIGHT" -> tick >= 13000 && tick < 23000;
            case "MIDNIGHT" -> tick >= 17000 && tick < 19000;
            default -> false;
        };
    }

    /** Require a valid terrain context as well as biome. Never forcibly spawn in stone. */
    private static BlockPos selectSpot(Rule r, ServerLevel level, int x, int z) {
        int top = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
        boolean belowGround = r.contexts.stream().anyMatch(s -> s.equals("Underground") || s.equals("Indoors"));
        if (belowGround) {
            int floorY = Math.min(top - 4, r.maxY < 999 ? r.maxY : top - 4);
            int lowest = Math.max(level.getMinBuildHeight()+2,r.minY);
            if (floorY < lowest) return null;
            for (int i = 0; i < 48; i++) {
                int y = lowest + RANDOM.nextInt(floorY-lowest+1);
                if (y <= level.getMinBuildHeight() + 1 || y < r.minY) continue;
                BlockPos p = new BlockPos(x,y,z);
                if (openSpace(level,p) && !level.canSeeSky(p) && sturdyBelow(level,p)) return p;
            }
            return null;
        }
        if (r.contexts.stream().anyMatch(s -> s.contains("Water") || s.equals("Liquid Floor"))) {
            for (int y = Math.min(top + 3,level.getMaxBuildHeight()-2); y >= Math.max(level.getMinBuildHeight()+1,top-12); y--) {
                BlockPos p = new BlockPos(x,y,z);
                if (y < r.minY || y > r.maxY) continue;
                boolean water = level.getFluidState(p).is(FluidTags.WATER);
                if ((water || level.getFluidState(p.below()).is(FluidTags.WATER)) &&
                    level.getBlockState(p.above()).isAir()) return p.above();
            }
            return null;
        }
        if (r.contexts.stream().anyMatch(s -> s.contains("Lava"))) {
            for (int y = Math.min(top + 3,level.getMaxBuildHeight()-2); y >= Math.max(level.getMinBuildHeight()+1,top-12); y--) {
                BlockPos p = new BlockPos(x,y,z);
                if (y < r.minY || y > r.maxY) continue;
                if (level.getFluidState(p.below()).is(FluidTags.LAVA) && openSpace(level,p)) return p;
            }
            return null;
        }
        if (r.contexts.contains("Air")) {
            int y = Math.max(r.minY, top + 10 + RANDOM.nextInt(16));
            if (y > r.maxY || y >= level.getMaxBuildHeight()-3) return null;
            BlockPos p = new BlockPos(x,y,z);
            return openSpace(level,p) && level.canSeeSky(p) ? p : null;
        }
        if (top < r.minY || top > r.maxY) return null;
        BlockPos p = new BlockPos(x,top,z);
        if (openSpace(level,p) && sturdyBelow(level,p)) return p;
        return null;
    }
    private static boolean openSpace(ServerLevel world, BlockPos pos) {
        return world.getBlockState(pos).isAir() && world.getBlockState(pos.above()).isAir();
    }
    private static boolean sturdyBelow(ServerLevel world, BlockPos pos) {
        BlockPos floor=pos.below();
        BlockState state=world.getBlockState(floor);
        return state.isSolid();
    }
    private static Candidate weightedChoice(List<Candidate> candidates) {
        double sum=0;
        for (Candidate c:candidates) sum+=Math.max(0,c.rule.rarity);
        if (sum<=0)return null;
        double roll=RANDOM.nextDouble()*sum;
        for (Candidate c:candidates)if ((roll-=Math.max(0,c.rule.rarity))<=0)return c;
        return candidates.get(candidates.size()-1);
    }

    private static void spawnAndAnnounce(MinecraftServer server, ServerPlayer focus, ServerLevel level, Candidate candidate, Config cfg) {
        Rule rule=candidate.rule;
        BlockPos pos=candidate.pos;
        Vec3 p=new Vec3(pos.getX()+0.5D,pos.getY(),pos.getZ()+0.5D);
        String command="spawnpokemonat "+p.x+" "+p.y+" "+p.z+" "+rule.species+" level="+rule.level;
        int result=server.getCommands().performPrefixedCommand(
            focus.createCommandSourceStack().withLevel(level).withPosition(p).withPermission(4).withSuppressedOutput(),command);
        if(result<=0) {
            System.err.println("[Pixelmon Rejuvenated] Legendary spawn command rejected: "+command);
            return;
        }
        String species = pretty(rule.species);
        String biome = level.registryAccess().registryOrThrow(Registries.BIOME).getKey(level.getBiome(pos).value()) == null
            ? "unknown biome" : level.registryAccess().registryOrThrow(Registries.BIOME).getKey(level.getBiome(pos).value()).getPath().replace('_',' ');
        Component message=Component.literal("A legendary "+species+" has spawned nearby in "+biome+"!").withStyle(ChatFormatting.GOLD);
        for (ServerPlayer recipient : server.getPlayerList().getPlayers()) {
            if (recipient.serverLevel()==level && (cfg.globalAnnouncements || recipient.position().distanceToSqr(p)<=cfg.announcementRadius*cfg.announcementRadius))
                recipient.sendSystemMessage(message);
        }
    }
    private static String pretty(String s) {
        return switch(s) {
            case "typenull" -> "Type: Null";
            case "chienpao" -> "Chien-Pao";
            case "chiyu" -> "Chi-Yu";
            case "tinglu" -> "Ting-Lu";
            case "wochien" -> "Wo-Chien";
            default -> s.substring(0,1).toUpperCase(Locale.ROOT)+s.substring(1);
        };
    }
    private static int delay(Config c,int players) {
        double scale=1+(Math.max(1,players)-1)*c.playerMultiplier;
        return Math.max(1200,(int)(c.averageIntervalTicks * (0.6+RANDOM.nextDouble()*0.8)/scale));
    }

    private static List<Rule> loadRules() {
        try(InputStream stream=LegendarySpawnEngine.class.getResourceAsStream("/data/pixelmonrejuvenated/legendary_spawn_rules.json")) {
            if (stream==null)throw new IOException("Legendary rules resource not found");
            JsonObject root=JsonParser.parseReader(new InputStreamReader(stream,StandardCharsets.UTF_8)).getAsJsonObject();
            List<Rule> result=new ArrayList<>();
            for(JsonElement element:root.getAsJsonArray("rules")) result.add(new Rule(element.getAsJsonObject()));
            return Collections.unmodifiableList(result);
        }catch(Exception e){System.err.println("[Pixelmon Rejuvenated] Unable to load legendary rules: "+e);return List.of();}
    }
    static final class Rule {
        final String species; final int level,minY,maxY,moonPhase;
        final double rarity; final List<String> biomes,excludedBiomes,times,weathers,structures,contexts;
        Rule(JsonObject o){
            species=o.get("species").getAsString();level=o.get("level").getAsInt();rarity=o.get("rarity").getAsDouble();
            minY=o.has("minY")?o.get("minY").getAsInt():-999;
            maxY=o.has("maxY")?o.get("maxY").getAsInt():999;
            moonPhase=o.has("moonPhase")?o.get("moonPhase").getAsInt():-1;
            biomes=values(o,"biomes"); excludedBiomes=values(o,"excludedBiomes");
            times=values(o,"times");weathers=values(o,"weathers");
            structures=values(o,"structures");contexts=values(o,"contexts");
        }
        private static List<String> values(JsonObject o,String key){
            if(!o.has(key))return List.of();
            List<String> result=new ArrayList<>();
            for(JsonElement el:o.getAsJsonArray(key))result.add(el.getAsString());
            return result;
        }
    }
    private record Candidate(Rule rule,BlockPos pos) { }
    private static final class TimerState {
        final Config config;int ticksRemaining;
        TimerState(Config config,int ticks) {this.config=config;this.ticksRemaining=ticks;}
    }
    private static final class Config {
        boolean enabled=true;
        int averageIntervalTicks=25000;
        double spawnChance=0.30;
        double playerMultiplier=0.01;
        int searchAttempts=96;
        int minDistance=24,maxDistance=96;
        int announcementRadius=256;
        boolean globalAnnouncements=false;
        static Config load() {
            Path file=FMLPaths.CONFIGDIR.get().resolve(CONFIG_NAME);
            Gson gson=new GsonBuilder().setPrettyPrinting().create();
            try {
                if(Files.isRegularFile(file))try(Reader reader=Files.newBufferedReader(file)){
                    Config read=gson.fromJson(reader,Config.class);
                    if(read!=null) {read.sanitize();return read;}
                }
                Config settings=new Config();Files.createDirectories(file.getParent());
                Files.writeString(file,gson.toJson(settings)+"\n");return settings;
            }catch(Exception e){System.err.println("[Pixelmon Rejuvenated] Using default legendary config: "+e);return new Config();}
        }
        void sanitize() {
            averageIntervalTicks=Math.max(1200,averageIntervalTicks);
            spawnChance=Math.max(0,Math.min(1,spawnChance));
            playerMultiplier=Math.max(0,Math.min(1,playerMultiplier));
            searchAttempts=Math.max(1,Math.min(256,searchAttempts));
            minDistance=Math.max(16,Math.min(96,minDistance));
            maxDistance=Math.max(minDistance+4,Math.min(128,maxDistance));
            announcementRadius=Math.max(32,Math.min(4096,announcementRadius));
        }
    }
}
