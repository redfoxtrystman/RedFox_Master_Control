#!/usr/bin/env python3
"""0.3.8: restore LT2 CaveCrawler branch/leaf rules and preserve Frost reference."""
from pathlib import Path
import json
root=Path('.')
runtime=root/'src/main/java/com/glaziolaicefox/lumberlands/tree/Lt2TreeRuntime.java'
text=runtime.read_text()
a=text.index('    private static Vec3 leafSizeBlocks(')
b=text.index('    private Lt2TreeRuntime()',a)
text=text[:a]+'''    private static Vec3 leafSizeBlocks(Lt2Species species, Vec3 sizeFactor, double thicknessStuds, double growthScale) {
        // Source-backed CaveCrawler LeafSizeFactor is relative to branch thickness.
        // 0.75 stud upper terminal branch thickness is a Minecraft port-scale
        // constraint, NOT a source-exact LT2 growth parameter.
        if (species != null && "cavecrawler".equals(species.id())) {
            double terminalThickness = Math.min(thicknessStuds, 0.75);
            return sizeFactor.scale(Lt2TreeRuntime.blocks(terminalThickness) * growthScale);
        }
        // Frost arrived in 2018, after the provided Roblox archive.
        // Preserve screenshot-reference short cyan Glass terminal pieces.
        if (species != null && "frost".equals(species.id()))
            return sizeFactor.scale(STUD_TO_BLOCK * growthScale);
        return sizeFactor.scale(Lt2TreeRuntime.blocks(thicknessStuds) * growthScale);
    }

'''+text[b:]
def one(old,new):
 global text
 n=text.count(old)
 if n!=1: raise RuntimeError(f'Expected one target but found {n}: {old[:100]}')
 text=text.replace(old,new)
one('            if ("cavecrawler".equals(referenceSpecies)) count = 1;\n','')
one('''                if ("cavecrawler".equals(referenceSpecies)) {
                    // Purple Foil terminals: ~0.34-0.48 block wide.
                    leaf.sizeFactor = new Vec3(1.0 + this.random.nextDouble()*0.42,
                            0.50 + this.random.nextDouble()*0.25,
                            0.86 + this.random.nextDouble()*0.44);
                } else if ("frost".equals(referenceSpecies)) {''',
'''                if ("frost".equals(referenceSpecies)) {''')
one('''                if (type == Origin.SPLIT &&
                        ("frost".equals(this.species.id()) || "cavecrawler".equals(this.species.id()))) {''',
'''                if (type == Origin.SPLIT && "frost".equals(this.species.id())) {''')
one('final int maxTips = "frost".equals(this.species.id()) ? 8 : 12;',
'final int maxTips = 8;')
one('wanted = Math.min(wanted, "frost".equals(this.species.id()) ? 2 : 3);',
'wanted = Math.min(wanted, 2);')
one('                    if ("cavecrawler".equals(this.species.id())) thicknessDelta *= 0.33;\n','')
runtime.write_text(text)
props=root/'gradle.properties';s=props.read_text()
assert s.count('mod_version=0.3.7')==1
props.write_text(s.replace('mod_version=0.3.7','mod_version=0.3.8'))
(root/'LUMBERLANDS_0.3.8_REFERENCE_AUDIT.md').write_text("""# LumberLands 0.3.8 reference and texture audit

Axe textures: Four recovered original Roblox textures were gzip-encoded data
wrongly packaged as PNG in 0.3.4 through 0.3.7. Fix the build by decoding the
PNG payload and validating its PNG header. Minecraft's magenta/black fallback
was the result of the invalid packaged texture format.

Cavecrawler: source from user-supplied LT2 TreeSubclasses/CaveCrawler and
TreeSuperClass. Keep 2-5 Foil leaves per terminal, source split multipliers and
the natural thickness growth. Remove invented 12-tip limit, single-leaf cap
and the 0.33 thickness reduction of previous builds. Leaf size is proportional
to section thickness with a documented Minecraft-specific 0.75-stud tip cap.
Bark Navy Blue Neon, inner wood Really Blue, leaves Mulberry Foil.
https://lumber-tycoon-2.fandom.com/wiki/Cavecrawler_Wood

Frost: screenshot-matched white crooked branches and sparing cyan Glass tips.
The 2017 Roblox archive predates Frost (added 2018). Do not claim access
to source-exact Frost growth. Compare against the LT2 wiki thumbnail.
https://lumber-tycoon-2.fandom.com/wiki/Frost_Wood

New growth required; existing tree visuals retain their generated geometry.
In-game visual parity and rigid-body physics remain unverified after CI.
""")
for p in root.rglob('*.json'):json.loads(p.read_text())
print('0.3.8 CaveCrawler source count/split behavior restored, Frost preserved.')
