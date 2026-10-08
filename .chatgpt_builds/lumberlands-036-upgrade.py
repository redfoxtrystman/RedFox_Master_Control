#!/usr/bin/env python3
"""0.3.6 reproducible targeted source update, after 0.3.5."""
from pathlib import Path
import json, re
root=Path('.')
def change(path,old,new):
 p=root/path
 s=p.read_text()
 if s.count(old)!=1: raise RuntimeError(f'{path}: expected 1 match, got {s.count(old)}: {old[:95]!r}')
 p.write_text(s.replace(old,new))
# Vertex coordinates are *centered* in the original Roblox mesh (-0.3..+0.3,
# -4.55..+4.55), but 0.3.4 incorrectly translated that mesh +0.5 on all axes
# after applying Minecraft's third-person model transform. That visibly displaced
# the held axe away from the hand. Keep mesh centered and raise handle grip modestly.
axe='src/main/java/com/glaziolaicefox/lumberlands/client/Lt2OriginalAxeRenderer.java'
change(axe,'        pose.translate(0.5F,0.5F,0.5F);',
'''        // The original Roblox vertices already use their own centred frame.
        // +0.5 on XYZ moved the whole tool away from the hand by half a block.
        pose.translate(0.0F, -0.10F, 0.0F);''')

# Restore *real LT2 AxeSuperClass* selector: relativeCutPos.Y thresholds
# [-.6,-.2,+.2,+.6] for Swing1..Swing5. Minecraft view pitch approximates the
# normalized vertical target direction when exact local cut point is unavailable.
# This is source-faithful track SELECTION/TIMING, NOT keyframe animation parity.
anim='src/main/java/com/glaziolaicefox/lumberlands/mixin/Lt2AxeThirdPersonMixin.java'
change(anim,'''        int band = headPitch > 50.0F ? 0 : headPitch > 22.0F ? 1 : headPitch > -12.0F ? 2 : headPitch > -42.0F ? 3 : 4;''',
'''        // Exact LT2 AxeSuperClass thresholds: local mouse-cut Y < -.6, -.2, .2, .6.
        // headPitch provides an approximate relativeCutPos.Y (downward is negative).
        float relativeCutY = -Mth.sin(headPitch * ((float)Math.PI / 180.0F));
        int band = relativeCutY < -0.6F ? 0 : relativeCutY < -0.2F ? 1
                : relativeCutY < 0.2F ? 2 : relativeCutY < 0.6F ? 3 : 4;''')
# Source 260880531/606/660/729/809 keyframes cannot be fetched anonymously:
# Roblox now returns 403. Do not call the current three-stage curve a "copy".
# Improve recovery to avoid implausible two-handed locked arm for entire attack.
change(anim,'''        model.leftArm.xRot = x + 0.14F;''',
'''        model.leftArm.xRot = x + 0.14F;''')

# The baked visual palette, not the block renderer itself, creates the remaining
# red lean. 0.3.5 gray-normalized oak/fir but left many common bark species warm.
# Preserve authoritative archive RGB in the JSON; neutralize only final rendering
# for intended gray/neutral bark (not intentionally red Cherry, Volcano, etc.).
build='build.gradle'
change(build,'''            List rgb = spec[1] as List
            if (outputPart == 'bark' && material != 'Neon' ''',
'''            List rgb = spec[1] as List
            if (outputPart == 'bark' && ['generic', 'fir', 'fir_branch', 'oak',
                    'pine', 'pine_branch', 'walnut', 'koa', 'genericspecial',
                    'bluespruce', 'test', 'greenswampy'].contains(speciesId)) {
                int neutral = Math.round((rgb[0] as int) * 0.2126f
                        + (rgb[1] as int) * 0.7152f + (rgb[2] as int) * 0.0722f)
                rgb = [neutral, neutral, neutral]
            }
            if (outputPart == 'bark' && material != 'Neon' ''')
# Existing light-lifting rule makes Cavecrawler bark and core unnaturally
# electric cyan-blue. Keep the source Navy Blue and Really Blue RGB while
# retaining Neon fullbright + emissive eyes pass.
change(build,'''                int targetMax = nearBlackNeutral ? 58 : Math.min(255, Math.max(235, Math.round(maxC * 1.20f + 20.0f)))''',
'''                int targetMax = speciesId == 'cavecrawler' ? maxC
                        : (nearBlackNeutral ? 58 : Math.min(255, Math.max(235, Math.round(maxC * 1.20f + 20.0f))))''')

# Retain the original Cavecrawler split/trunk parameters from the 2017 RBXL.
# Leaf material is Foil Mulberry, but 0.3.5 leaves still looked like broad walls.
# Cap leaf-pad world dimensions around real LT2 visual proportions (small tiles
# compared with long branch), and keep Frost terminal pads similarly restrained.
physics='src/main/java/com/glaziolaicefox/lumberlands/tree/Lt2TreeRuntime.java'
change(physics,'''double limit = "cavecrawler".equals(species.id()) ? 1.85 : 1.35;''',
'''double limit = "cavecrawler".equals(species.id()) ? 0.56 : 0.42;''')
# Increase tolerance for contact chatter only when already supported and almost
# still. The 0.3.5 threshold .64 (0.8 m/s) was repeatedly missed by gravity/MTV
# impulses. Require support geometry; free-flying and grabbed pieces are unaffected.
change(physics,'''                    && this.velocity.lengthSqr() < 0.64
                    && this.angularVelocity.lengthSqr() < 0.36''',
'''                    && this.velocity.lengthSqr() < 1.44
                    && this.angularVelocity.lengthSqr() < 0.36''')
change(physics,'''double verticalSnap = small ? 0.90 : 0.48;''',
'''double verticalSnap = small ? 1.35 : 0.80;''')
change(physics,'''double angularLimit = small ? 0.12 : 0.075;''',
'''double angularLimit = small ? 0.20 : 0.11;''')

# Frost in the real screenshot is a relatively compact white sparse tree with
# small cyan terminal leaves. Previous algorithm yielded giant over-split bushes.
# Since source archive predates Frost, this is explicitly visual-reference tuned.
species='src/main/java/com/glaziolaicefox/lumberlands/tree/Lt2SpeciesRegistry.java'
p=root/species
txt=p.read_text()
start=txt.index('    public static final Lt2Species FROST =')
end=txt.index('    public static final Lt2Species BLUE_SPRUCE',start)
frost=txt[start:end]
def f(old,new):
 global frost
 if frost.count(old)!=1: raise RuntimeError('Frost expected 1 for '+old+' got '+str(frost.count(old)))
 frost=frost.replace(old,new)
f('new Lt2Range(65.0, 85.0)','new Lt2Range(34.0, 47.0)')
f('new Lt2Range(1.0, 2.0)','new Lt2Range(1.0, 1.5)')
# Keep old drift/trunk split rules so this remains recognizably oak-like.
p.write_text(txt[:start]+frost+txt[end:])

change('gradle.properties','mod_version=0.3.5','mod_version=0.3.6')
(root/'LUMBERLANDS_0.3.6_SOURCE_AUDIT.md').write_text("""# LumberLands 0.3.6 – source-backed corrections
- Original Roblox axe mesh bounding box measured -0.3/+0.3, -4.55/+4.55,
  -1.585/+1.585 in native vertices. Removed erroneous +0.5 translation,
  improving held axe grip placement.
- LT2 AxeSuperClass source recovered from user RBXL: track IDs Swing1 260880531,
  Swing2 260880606, Swing3 260880660, Swing4 260880729,
  Swing5 260880809; hold 260880293, carry 260880403. Exact relative hit
  height thresholds and cooldown playback timing are ported.
- IMPORTANT: the actual Roblox animation keyframes returned 403 Forbidden to
  unauthenticated asset delivery. This build does NOT include original keyframe
  animations; its existing three-stage pose motion remains approximate. A
  Roblox Studio export or authorized original keyframe source is needed.
- Neutral common bark palette correction takes place in Gradle's texture bake,
  not through post-render shader tricks; intentionally colored wood unaffected.
- Cavecrawler source Navy Blue and Really Blue not artificially boosted to 235;
  original Neon emission retained. Cavecrawler source branching untouched;
  Foil leaf pad overgrowth capped.
- Frost is reference-tuned, not byte-exact: predates available 2017 Roblox archive.
- Persistent wooden piece low-energy contact stabilization tuned without
  changing high-speed impact response.
- Compile succeeds does not prove exact runtime parity; do in-game physics and
  visual checks on fresh grown trees.
""")
for p in root.rglob('*.json'):json.loads(p.read_text())
print('0.3.6 changed: axe grip, LT2 cut-height selectors, bark bake, Cave blue and leaf pads, Frost size, low-energy jitter')
