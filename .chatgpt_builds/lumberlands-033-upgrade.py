from pathlib import Path
import json
root=Path('.')
def change(path,old,new):
 p=root/path
 s=p.read_text()
 assert s.count(old)==1,(path,s.count(old),old[:65])
 p.write_text(s.replace(old,new))
runtime='src/main/java/com/glaziolaicefox/lumberlands/tree/Lt2TreeRuntime.java'
visual='src/main/java/com/glaziolaicefox/lumberlands/entity/Lt2TreeVisualEntity.java'
species='src/main/java/com/glaziolaicefox/lumberlands/tree/Lt2SpeciesRegistry.java'
change(runtime,'    private static final Map<UUID, StandingTree> TREES =',"""    public static boolean isVisualOwned(ServerLevel level, UUID id) {
        if (id == null) return false;
        for (StandingTree tree : TREES.values())
            if (!tree.removed && tree.level == level && id.equals(tree.visualId)) return true;
        for (LooseBody body : LOOSE.values())
            if (!body.removed && body.level == level && id.equals(body.visualId)) return true;
        for (LooseBody body : PENDING_LOOSE)
            if (!body.removed && body.level == level && id.equals(body.visualId)) return true;
        return false;
    }

    private static final Map<UUID, StandingTree> TREES =""")
change(visual,'import net.minecraft.core.registries.BuiltInRegistries;',
'insert' if False else '''import com.glaziolaicefox.lumberlands.tree.Lt2TreeRuntime;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.core.registries.BuiltInRegistries;''')
change(visual,'''                if (tree.level() == level && !tree.geometry().getList("sections", 10).isEmpty()
                        && tree.getBoundingBox().intersects(query)) out.add(tree);''',
'''                if (tree.level() != level || tree.geometry().getList("sections", 10).isEmpty()) continue;
                if (level instanceof ServerLevel server &&
                        !Lt2TreeRuntime.isVisualOwned(server, tree.getUUID())) continue;
                if (tree.getBoundingBox().intersects(query)) out.add(tree);''')
change(visual,'''        super.tick();
        if (!this.level().isClientSide && this.geometry().getBoolean("leafDebris")''',
'''        super.tick();
        if (this.level() instanceof ServerLevel server && this.tickCount > 40
                && !this.geometry().getList("sections", 10).isEmpty()
                && !Lt2TreeRuntime.isVisualOwned(server, this.getUUID())) {
            this.discard();
            return;
        }
        if (!this.level().isClientSide && this.geometry().getBoolean("leafDebris")''')
change(runtime,'        int quietTicks;\n        int contactGraceTicks;',
 '        int quietTicks;\n        int supportSettleTicks;\n        int contactGraceTicks;')
change(runtime,'''            if (!held) this.stabilizeRestingContact();
            // Short loose segments''',
'''            if (!held) this.stabilizeRestingContact();
            // Multiple consecutive real ground contacts must settle small pieces.
            // This avoids gravity/impulse oscillation at the old unreachable sleep threshold.
            if (!held && collided && this.hasWorldSupport()) {
                boolean small = this.isSmallPiece();
                double vLimit = this.surfaceFriction < 0.10 ? 0.18 : (small ? 0.90 : 0.28);
                double wLimit = this.surfaceFriction < 0.10 ? 0.16 : (small ? 0.65 : 0.18);
                if (this.velocity.lengthSqr() < vLimit * vLimit
                        && this.angularVelocity.lengthSqr() < wLimit * wLimit) {
                    ++this.supportSettleTicks;
                    if (this.supportSettleTicks >= (small ? 2 : 8)) {
                        this.velocity = Vec3.ZERO;
                        this.angularVelocity = Vec3.ZERO;
                        this.sleeping = true;
                    }
                } else this.supportSettleTicks = 0;
            } else this.supportSettleTicks = 0;
            // Short loose segments''')
change('build.gradle',
'''            List rgb = spec[1] as List
            def source = cache.containsKey(material)''',
'''            List rgb = spec[1] as List
            if (outputPart == 'bark' && material != 'Neon'
                    && rgb[0] > rgb[1] + 10
                    && Math.abs((rgb[1] as int) - (rgb[2] as int)) <= 8) {
                int r = Math.round((rgb[1] as int) + ((rgb[0] as int) - (rgb[1] as int)) * 0.35f)
                rgb = [r, rgb[1], rgb[2]]
            }
            def source = cache.containsKey(material)''')
p=root/species
s=p.read_text()
a=s.index('    public static final Lt2Species FROST =')
b=s.index('    public static final Lt2Species BLUE_SPRUCE',a)
f=s[a:b]
assert f.count('new Lt2Range(72.0, 96.0)')==1
assert f.count('new Lt2Range(7.0, 12.0), new Lt2Range(2.0, 4.0)')==1
f=f.replace('new Lt2Range(72.0, 96.0)','new Lt2Range(56.0, 74.0)')
f=f.replace('new Lt2Range(7.0, 12.0), new Lt2Range(2.0, 4.0)',
            'new Lt2Range(11.0, 17.0), new Lt2Range(1.0, 2.0)')
f=f.replace('new Lt2Range(35.0, 150.0)','new Lt2Range(32.0, 100.0)')
p.write_text(s[:a]+f+s[b:])
change('gradle.properties','mod_version=0.3.2','mod_version=0.3.3')
(root/'LUMBERLANDS_0.3.3_FIX_STATUS.md').write_text("""# 0.3.3 targeted fixes
Orphaned persisted tree_visual geometry no longer supplies server collision; saved orphans are discarded after 40 ticks.
Grounded low-speed logs enter stable sleep after consecutive supporting contacts.
Near-neutral bark textures have excess magenta corrected at bake time; Neon left unchanged.
Frost overbranching reduced; exact Frost source absent from the user's pre-2018 RBXL.
Original axe vertices/UV assets are not in the source RBXL, and still require a separate asset import.
Not an in-game test and not exact LT2 axe parity.
""")
for j in root.rglob('*.json'): json.loads(j.read_text())
print('0.3.3 source edits complete')
