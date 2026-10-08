#!/usr/bin/env python3
"""0.3.7 species-specific LT2 visual-parity pass, grounded in user screenshot silhouettes.
Only Cave Crawler and Frost are reshaped; other species and Neon renderer preserved.
"""
from pathlib import Path
import json
import re

ROOT = Path(".")
runtime = Path("src/main/java/com/glaziolaicefox/lumberlands/tree/Lt2TreeRuntime.java")
registry = Path("src/main/java/com/glaziolaicefox/lumberlands/tree/Lt2SpeciesRegistry.java")
def once(path, old, new):
    src = path.read_text()
    n = src.count(old)
    if n != 1:
        raise RuntimeError(f"{path}: expected one match but found {n}: {old[:100]!r}")
    path.write_text(src.replace(old, new))

# The previous 'limit leaf dimensions' hack still let foliage depend on
# parent thickness. Once source CaveCrawler has grown for 120-200 updates,
# a Foil leaf's world size could hit the cap and turn into a huge flat panel.
# Reference: one small Mulberry purple terminal cap, not broad purple sheets.
# The screenshot Frost equivalent: small cyan Glass terminal blocks.
src=runtime.read_text()
start=src.index("    private static Vec3 leafSizeBlocks(")
end=src.index("    private Lt2TreeRuntime()",start)
src=src[:start]+'''    private static Vec3 leafSizeBlocks(Lt2Species species, Vec3 sizeFactor, double thicknessStuds, double growthScale) {
        // User-reference silhouettes: crisp little cuboids at branch ends, not
        // thickness-amplified rectangular canopies. sizeFactor for these two
        // species is expressed in LT2 studs and fixed at leaf creation.
        // This changes only the terminal leaf visual/physics dimensions.
        if (species != null && ("cavecrawler".equals(species.id()) || "frost".equals(species.id()))) {
            return sizeFactor.scale(STUD_TO_BLOCK * growthScale);
        }
        return sizeFactor.scale(Lt2TreeRuntime.blocks(thicknessStuds) * growthScale);
    }

'''+src[end:]
runtime.write_text(src)

once(runtime,'''            int count = section.unit.species.numLeafParts().randomInt(this.random);
            for (int i = 0; i < count; ++i) {''',
'''            String referenceSpecies = section.unit.species.id();
            int count = section.unit.species.numLeafParts().randomInt(this.random);
            // Reference LT2 screenshots: individual capped branch tips.
            // Old code spawned 2-5 thickness-scaled Foil slabs on each Cave tip,
            // producing the reported purple wall-like canopies.
            if ("cavecrawler".equals(referenceSpecies)) count = 1;
            if ("frost".equals(referenceSpecies)) count = this.random.nextDouble() < 0.82 ? 1 : 0;
            for (int i = 0; i < count; ++i) {''')
once(runtime,'''                leaf.sizeFactor = new Vec3(sp.leafSizeX().random(this.random), sp.leafSizeY().random(this.random), sp.leafSizeZ().random(this.random));
                Quaternionf orient =''',
'''                leaf.sizeFactor = new Vec3(sp.leafSizeX().random(this.random), sp.leafSizeY().random(this.random), sp.leafSizeZ().random(this.random));
                if ("cavecrawler".equals(referenceSpecies)) {
                    // Purple Foil terminals: ~0.34-0.48 block wide.
                    leaf.sizeFactor = new Vec3(1.0 + this.random.nextDouble()*0.42,
                            0.50 + this.random.nextDouble()*0.25,
                            0.86 + this.random.nextDouble()*0.44);
                } else if ("frost".equals(referenceSpecies)) {
                    // Frost: little cyan Glass tiles, sparse, near outermost twigs.
                    leaf.sizeFactor = new Vec3(0.78 + this.random.nextDouble()*0.36,
                            0.43 + this.random.nextDouble()*0.24,
                            0.70 + this.random.nextDouble()*0.45);
                }
                Quaternionf orient =''')

# Real screenshot: moderate number of clear diverging branches, not explosive
# exponential tips. Use distinct limits for Frost and CaveCrawler. Keep
# interconnected Section graphs, so cutting/physics still work for all limbs.
once(runtime,
'''                int wanted = numSplitsRange.randomInt(StandingTree.this.random);
                double minChord =''',
'''                int wanted = numSplitsRange.randomInt(StandingTree.this.random);
                if (type == Origin.SPLIT &&
                        ("frost".equals(this.species.id()) || "cavecrawler".equals(this.species.id()))) {
                    // Shape grammar: sparse crooked Frost (~4-8 branch ends),
                    // with a broader but still legible CaveCrawler crown.
                    final int maxTips = "frost".equals(this.species.id()) ? 8 : 12;
                    int activeTips = 0;
                    for (Section section : StandingTree.this.sections.values()) {
                        if (section.extremity && section.growing
                                && section.unit.species.id().equals(this.species.id())) ++activeTips;
                    }
                    int available = Math.max(1, maxTips - activeTips);
                    wanted = Math.max(1, Math.min(wanted, available));
                    wanted = Math.min(wanted, "frost".equals(this.species.id()) ? 2 : 3);
                }
                double minChord =''')

# Thickening applied to every segment on every grow tick was producing
# oversized dense growth relative to the requested source-silhouette proportions.
# Adjust *geometry itself* (not renderer-only shrink) so cutting, collision
# and fallen wood share those actual narrower limb widths.
once(runtime,
'''                    section.thickness += this.species.thicknessGrow().random(StandingTree.this.random);
                    StandingTree.this.updateSectionDisplay(section);''',
'''                    double thicknessDelta = this.species.thicknessGrow().random(StandingTree.this.random);
                    if ("cavecrawler".equals(this.species.id())) thicknessDelta *= 0.33;
                    // Frost's thin white limbs remain close to Oak proportions.
                    if ("frost".equals(this.species.id())) thicknessDelta *= 0.78;
                    section.thickness += thicknessDelta;
                    StandingTree.this.updateSectionDisplay(section);''')

# Frost original script unavailable (introduced in 2018). The user provided
# authoritative screenshot: compact white branching silhouette with roughly
# a handful of cyan cuboid Glass tips. Tune the topology explicitly instead
# of applying another magic leaf cap to an overgrown bush.
p=registry
src=p.read_text()
a=src.index('    public static final Lt2Species FROST =')
b=src.index('    public static final Lt2Species BLUE_SPRUCE',a)
f=src[a:b]
def onef(old,new):
    global f
    n=f.count(old)
    if n!=1: raise RuntimeError(f'FROST: need one {old!r}, got {n}')
    f=f.replace(old,new)
onef('new Lt2Range(34.0, 47.0)', 'new Lt2Range(38.0, 48.0)')
# More open terminal branching, fewer jagged tiny segments per branch:
onef('new Lt2Range(11.0, 17.0), new Lt2Range(1.0, 1.5)',
     'new Lt2Range(7.0, 11.0), new Lt2Range(2.0, 2.0)')
onef('new Lt2Range(12.0, 64.0)', 'new Lt2Range(24.0, 55.0)')
onef('new Lt2Range(-0.15, 1.0)', 'new Lt2Range(0.12, 1.0)')
onef('new Lt2Range(2.5, 5.0)', 'new Lt2Range(6.0, 10.0)')
onef('new Lt2Range(12.0, 38.0)', 'new Lt2Range(12.0, 26.0)')
onef('new Lt2Range(0.52, 0.66)', 'new Lt2Range(0.40, 0.54)')
src=src[:a]+f+src[b:]
p.write_text(src)

# Keep CaveCrawler's authoritative 2017 branch parameter table (1-3 growth
# interval, 120-200 calls, 2-6 source split count), but the per-split cap above
# prevents unsupported combinatorial sprawl. Original blue & purple palette stays.
once(Path('gradle.properties'),'mod_version=0.3.6','mod_version=0.3.7')
(ROOT/'LUMBERLANDS_0.3.7_REFERENCE_SILHOUETTE.md').write_text('''# 0.3.7 visual-reference correction

Source priority: user-supplied screenshots and LT2 TreeSubclasses/CaveCrawler.
The 2017 RBXL does NOT contain Frost's later 2018 growth script.

## CaveCrawler
- Source-backed CaveCrawler growth data retained in species table.
- 3 children maximum at each split, 12 concurrent tips cap, rather than repeatedly
  spawning visually illegible crowns across the Minecraft scale conversion.
- Grow-section width scaled for a narrow blue branching silhouette.
- Precisely one modest Foil Mulberry leaf cap per active terminal section.
- Bark remains Navy Blue; core remains Really Blue; Neon preserved.

## Frost
- White thin angular sections with no more than 8 active extremities.
- Two-child split, widened split spacing, bent limbs that stay mostly above horizon.
- 82% terminal-leaf chance and compact cyan Glass caps.
- Reference-tuned reconstruction because original Frost source is absent.

All sections retain unified collision, dragging, cutting and loose-body simulation.
Growth changes apply to **new** trees, not saved existing geometry.
This is compiled-source validation, not in-game image comparison.
''')
for p in ROOT.rglob('*.json'): json.loads(p.read_text())
src=runtime.read_text()
assert 'maxTips = "frost".equals(this.species.id()) ? 8 : 12' in src
assert 'if ("cavecrawler".equals(referenceSpecies)) count = 1' in src
print('0.3.7 species-specific topology and reference terminal leaf geometry applied')
