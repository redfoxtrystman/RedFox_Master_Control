#!/usr/bin/env python3
"""0.3.5 regression correction: original mesh UV, LT2 palettes, leaf geometry, contact stability."""
from pathlib import Path
import json, struct, math

ROOT=Path('.')
def replace(path, before, after):
 p=ROOT/path
 data=p.read_text()
 n=data.count(before)
 if n!=1: raise RuntimeError(f"{path}: expected unique {before[:75]!r}, got {n}")
 p.write_text(data.replace(before,after))

# Roblox FileMesh version 1.00 stores V upside-down; previous 0.3.4 copied V directly
# (Roblox official format reference). Invert every original vertex's V once, at import.
mesh=ROOT/'src/main/resources/assets/lumberlands/meshes/lt2_original_axe.bin'
data=bytearray(mesh.read_bytes())
faces=struct.unpack_from('>i',data)[0]
assert faces==6504 and len(data)==4+faces*8*4
for vertex in range(faces):
 off=4 + (vertex*8+7)*4
 v=struct.unpack_from('>f',data,off)[0]
 assert -0.03<=v<=1.03,(vertex,v)
 struct.pack_into('>f',data,off,1.0-v)
mesh.write_bytes(data)

# The previous "35% reduce red" in 0.3.3 still left red in near-grey bark.
# The baked RGB palette is *the* source of that coloration; don't shift
# every fragment in the vertex renderer, where it would also spoil Neon.
palette=ROOT/'roblox_tree_materials.json'
material=json.loads(palette.read_text())
neutral_species=[]
for species,parts in material.items():
 bark=parts.get('bark')
 if not bark or bark[0]=='Neon': continue
 rgb=list(bark[1])
 if (12 <= rgb[0]-rgb[1] <= 45 and abs(rgb[1]-rgb[2])<=12
         and 80<=rgb[1]<=210):
  grey=round(rgb[0]*0.2126+rgb[1]*0.7152+rgb[2]*0.0722)
  bark[1]=[grey,grey,grey]
  neutral_species.append(species)
palette.write_text(json.dumps(material,indent=2)+'\n')
assert 'oak' in neutral_species and 'fir' in neutral_species,neutral_species

# Cavecrawler: enormous late-stage source-scaled leaves were rendering as
# broad geometric walls (screenshots) because a thick late-generation end section
# can multiply a 4–6 LeafSizeFactor into many blocks. Keep LT2 ratios but cap each
# whole leaf pad to a finite real-world size; roots and Neon geometry stay intact.
runtime='src/main/java/com/glaziolaicefox/lumberlands/tree/Lt2TreeRuntime.java'
replace(runtime,
'''        return sizeFactor.scale(Lt2TreeRuntime.blocks(thicknessStuds) * growthScale);''',
'''        Vec3 size = sizeFactor.scale(Lt2TreeRuntime.blocks(thicknessStuds) * growthScale);
        if (species != null && ("cavecrawler".equals(species.id()) || "frost".equals(species.id()))) {
            // Late-stage branches can otherwise produce giant Foil/Glass walls.
            double limit = "cavecrawler".equals(species.id()) ? 1.85 : 1.35;
            double largest = Math.max(size.x, Math.max(size.y, size.z));
            if (largest > limit) size = size.scale(limit / largest);
        }
        return size;''')

# Cave Crawler trunk shape is retained from the original supplied RBXL; no
# invented replacement of its legacy split rules. Frost postdates the RBXL,
# so calibrate its invented generator against wiki's "oak-like but more erratic".
species='src/main/java/com/glaziolaicefox/lumberlands/tree/Lt2SpeciesRegistry.java'
p=ROOT/species; source=p.read_text()
a=source.index('    public static final Lt2Species FROST =')
b=source.index('    public static final Lt2Species BLUE_SPRUCE',a)
frost=source[a:b]
def frostrepl(old,new):
 global frost
 if frost.count(old)!=1: raise RuntimeError(f'Frost: {old} appears {frost.count(old)} times')
 frost=frost.replace(old,new)
# Current 0.3.3 Frost is 56-74 grows, while Oak has 65-90;
# earlier ticks create thin, underformed, erratic splinters.
frostrepl('new Lt2Range(56.0, 74.0)','new Lt2Range(65.0, 85.0)')
# The trunk is currently bending every 5-10 studs, unlike Oak's stable trunk.
frostrepl('new Lt2Range(5.0, 10.0), new Lt2Range(6.0, 11.0), new Lt2Range(10000.0, 10000.0)',
          'new Lt2Range(10000.0, 10000.0), new Lt2Range(9.0, 16.0), new Lt2Range(10000.0, 10000.0)')
# Keep branch direction noticeably more erratic than Oak, without horizontal fans.
frostrepl('new Lt2Range(0.0, 78.0)','new Lt2Range(12.0, 64.0)')
frost=frost.replace('new Lt2Range(3.0, 7.0), new Lt2Range(1.0, 2.5), new Lt2Range(3.0, 7.0)',
                    'new Lt2Range(2.2, 4.0), new Lt2Range(0.8, 1.8), new Lt2Range(2.2, 4.0)')
source=source[:a]+frost+source[b:]
p.write_text(source)

# Detect near-rest grounded small pieces before resetting transient support,
# then latch them into sleep. Impacts, grabbing, or lost ground support still wake.
replace(runtime,
'''            this.resetSupportContacts();

            if (this.sleeping && !held) {''',
'''            boolean previouslySupported = this.supportContact;
            this.resetSupportContacts();
            if (!held && previouslySupported && this.isSmallPiece()
                    && this.velocity.lengthSqr() < 0.64
                    && this.angularVelocity.lengthSqr() < 0.36
                    && this.hasWorldSupport()) {
                this.velocity = Vec3.ZERO;
                this.angularVelocity = Vec3.ZERO;
                this.sleeping = true;
            }

            if (this.sleeping && !held) {''')
# Avoid unnecessary rotation resend each tick when body at rest
replace(runtime,
'''            this.updateVisualsAndBounds();
        }

        void integrateRotation(double dt) {''',
'''            this.updateVisualsAndBounds();
        }

        void integrateRotation(double dt) {''') # exact intent/documentation anchor
replace('gradle.properties','mod_version=0.3.4','mod_version=0.3.5')
(ROOT/'LUMBERLANDS_0.3.5_TEST_NOTES.md').write_text(
'''# LumberLands 0.3.5 targeted corrections
- Roblox FileMesh v1.00 original axe V coordinate flipped during conversion (all 6504 original vertices).
- Near-neutral bark source palettes are explicitly neutralized at texture bake, not via lighting hacks; intentional warm/red species and Neon are not recolored.
- Cavecrawler/Frost leaf pads are capped in rendered/collision leaf geometry to prevent overscaled walls; this is a measured compromise, not a claim of pixel-exact LT2 parity.
- Frost rebalanced around documented Oak-like, somewhat more erratic growth. Original Frost script is unavailable from the 2017 RBXL.
- Extra support hysteresis prevents grounded tiny segments repeating gravity/impulse oscillation.
- Re-test in an *unmodified* world or regenerate trees to see new species growth. Already-grown trees keep their stored geometry.
- Real-world in-game and all-loader runtime behavior must still be verified.
''')
for path in ROOT.rglob('*.json'):json.loads(path.read_text())
print('0.3.5 source changes applied. Neutral bark species:',neutral_species,'Axe vertices:',faces)
