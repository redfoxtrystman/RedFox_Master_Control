package com.glaziola.pixelmonrejuvenated;

import java.lang.reflect.*;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;

/** Server-only Cobblemon BATTLE_FAINTED integration. Counts battle KOs, not entity deaths. */
public final class BirdOrbBattleHooks {
    private static boolean registered;
    private BirdOrbBattleHooks() {}

    public static synchronized void register() {
        if (registered) return;
        try {
            Class<?> events = Class.forName("com.cobblemon.mod.common.api.events.CobblemonEvents");
            Object observable = events.getField("BATTLE_FAINTED").get(null);
            Class<?> priorityType = Class.forName("com.cobblemon.mod.common.api.Priority");
            Class<?> functionType = Class.forName("kotlin.jvm.functions.Function1");
            @SuppressWarnings({"unchecked", "rawtypes"})
            Object normal = Enum.valueOf((Class<? extends Enum>) priorityType.asSubclass(Enum.class), "NORMAL");
            Object unit = Class.forName("kotlin.Unit").getField("INSTANCE").get(null);
            Object callback = Proxy.newProxyInstance(functionType.getClassLoader(), new Class[]{functionType},
                (proxy,method,args)-> {
                    if (method.getName().equals("invoke") && args != null && args.length == 1) {
                        try { onBattleFaint(args[0]); }
                        catch (Exception e) { System.err.println("[Rejuvenated] Orb battle KO processing failed: " + e); }
                        return unit;
                    }
                    if (method.getName().equals("toString")) return "RejuvenatedOrbBattleFaintListener";
                    if (method.getName().equals("hashCode")) return System.identityHashCode(proxy);
                    if (method.getName().equals("equals")) return proxy == args[0];
                    return unit;
                });
            Method subscribe = null;
            for (Method m : observable.getClass().getMethods()) {
                if (m.getName().equals("subscribe") && m.getParameterCount()==2 &&
                    m.getParameterTypes()[0].isAssignableFrom(priorityType) &&
                    m.getParameterTypes()[1].isAssignableFrom(functionType)) { subscribe = m; break; }
            }
            if (subscribe == null) throw new IllegalStateException("Cobblemon EventObservable.subscribe(Priority, Function1) not found");
            subscribe.invoke(observable, normal, callback);
            registered = true;
            System.out.println("[Rejuvenated] Bird orbs subscribed to Cobblemon BATTLE_FAINTED (250 defeats)");
        } catch (ReflectiveOperationException | IllegalStateException error) {
            throw new IllegalStateException("Cannot register Cobblemon battle charging; verify Cobblemon 1.8.1",error);
        }
    }

    private static Object call(Object obj, String name) throws ReflectiveOperationException {
        return obj.getClass().getMethod(name).invoke(obj);
    }
    private static void onBattleFaint(Object event) throws ReflectiveOperationException {
        Object battle = call(event,"getBattle");
        Object faintedActor = call(call(event,"getKilled"),"getActor");
        Object faintedSide = call(faintedActor,"getSide");
        Iterable<?> actors = (Iterable<?>)call(battle,"getActors");
        Iterable<?> participants = (Iterable<?>)call(battle,"getPlayers");
        Map<UUID,ServerPlayer> online = new HashMap<>();
        Object defeatedPokemon = call(call(event, "getKilled"), "getEffectedPokemon");
        Object species = call(defeatedPokemon, "getSpecies");
        String faintedSpecies = (String)call(species, "getName");
        double orbChance = switch (faintedSpecies.toLowerCase(Locale.ROOT)) {
            case "dragonair" -> 0.10;
            case "dragonite" -> 0.30;
            case "dialga", "palkia", "giratina" -> 1.0;
            default -> 0.0;
        };
        boolean wild = String.valueOf(call(faintedActor,"getType")).equalsIgnoreCase("WILD");
        for (Object p : participants) if (p instanceof ServerPlayer sp) online.put(sp.getUUID(), sp);
        Set<UUID> credited = new HashSet<>();
        for (Object actor : actors) {
            if (call(actor,"getSide").equals(faintedSide)) continue;
            for (Object key : (Iterable<?>)call(actor,"getPlayerUUIDs")) {
                if (!(key instanceof UUID uuid) || !credited.add(uuid)) continue;
                ServerPlayer player = online.get(uuid);
                if (player == null || player.getServer() == null) continue;
                boolean dropOrb = wild && orbChance > 0 && ThreadLocalRandom.current().nextDouble() < orbChance;
                player.getServer().execute(() -> {
                    chargeInventory(player);
                    if (dropOrb) {
                        ItemStack reward = new ItemStack(BirdOrbs.ORB.get());
                        if (!player.getInventory().add(reward)) player.drop(reward, false);
                    }
                });
            }
        }
    }
    private static void chargeInventory(ServerPlayer player) {
        var inventory = player.getInventory();
        for (int slot=0;slot<inventory.getContainerSize();slot++) {
            ItemStack stack = inventory.getItem(slot);
            BirdOrbItem.chargeOne(stack);
        }
    }
}
