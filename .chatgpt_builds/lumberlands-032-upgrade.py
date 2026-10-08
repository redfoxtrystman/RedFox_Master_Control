#!/usr/bin/env python3
"""LumberLands 0.3.2 update from the validated 0.3.1 baseline.
Changes collisions, settling, material tint, and source-backed axe proportions.
"""
from pathlib import Path
import json
root = Path('.')
def edit(path, before, after):
    p=root/path
    original=p.read_text()
    n=original.count(before)
    if n!=1: raise RuntimeError(f'{path}: expected exactly one match but found {n} for {before[:70]!r}')
    p.write_text(original.replace(before,after))

tree='src/main/java/com/glaziolaicefox/lumberlands/tree/Lt2TreeRuntime.java'
visual='src/main/java/com/glaziolaicefox/lumberlands/entity/Lt2TreeVisualEntity.java'
edit(visual,
    'if (tree.level() == level && tree.getBoundingBox().intersects(query)) out.add(tree);',
    'if (tree.level() == level && !tree.geometry().getList("sections", 10).isEmpty() && tree.getBoundingBox().intersects(query)) out.add(tree);')
p=root/visual
s=p.read_text()
a=s.index('            // A long AABB around an angled LT2 Part')
b=s.index('        this.collisionBoxes = List.copyOf(boxes);',a)
s=s[:a]+'''            // Source cuboid rasterization: subdivide across all 3 rotated local axes.
            // Longitudinal-only AABB slices contained phantom air around inclined wood.
            // A per-tree budget keeps enormous LT2 trees from exhausting movement queries.
            int remaining = Math.max(1, sections.size() - index);
            int budget = Math.max(1, (3500 - boxes.size()) / remaining);
            int nx = Math.max(1, Math.min(7, (int)Math.ceil(sx / 0.14)));
            int nz = nx;
            int ny = Math.max(1, Math.min(192, (int)Math.ceil(sy / 0.14)));
            int count = nx * ny * nz;
            if (count > budget) {
                double factor = Math.cbrt((double)count / (double)budget);
                nx = Math.max(1, (int)Math.floor(nx / factor));
                nz = nx;
                ny = Math.max(1, Math.min(192, (int)Math.floor(budget / (double)(nx*nz))));
            }
            double half = sx*0.5;
            for (int yi=0;yi<ny;yi++) {
                double y0=sy*yi/ny, y1=sy*(yi+1)/ny;
                for (int xi=0;xi<nx;xi++) {
                    double x0=-half+sx*xi/nx, x1=-half+sx*(xi+1)/nx;
                    for(int zi=0;zi<nz;zi++) {
                        double z0=-half+sx*zi/nz, z1=-half+sx*(zi+1)/nz;
                        boxes.add(pieceBounds(worldStart,worldQ,x0,x1,y0,y1,z0,z1));
                    }
                }
            }
        }
'''+s[b:]
a=s.index('    private static AABB sliceBounds(')
b=s.index('        double minX = ',a)
s=s[:a]+'''    private static AABB pieceBounds(Vec3 bottomCenter, Quaternionf q,
                                    double x0,double x1,double y0,double y1,double z0,double z1) {
'''+s[b:]
s=s.replace('        double hx = sx * 0.5, hz = sz * 0.5;\n','')
s=s.replace('(xi == 0 ? -hx : hx)','(xi == 0 ? x0 : x1)')
s=s.replace('(zi == 0 ? -hz : hz)','(zi == 0 ? z0 : z1)')
assert 'sliceBounds(' not in s
p.write_text(s)

edit(tree,'''        void refreshPhysicsSections() {
            this.physicsSections.clear();
            if (this.sections.size() <= 72) {''','''        void refreshPhysicsSections() {
            this.physicsSections.clear();
            // Every visible part participates in terrain contact, even on giant trees.
            this.physicsSections.addAll(this.sections);
            if (false) {''')
# The now-dead older ranking branch is intentionally kept compilable. Its addAll was
# replaced above, and the following if(false) means no sections are culled.
edit(tree,
 '''                double maxProjection = this.isSmallPiece() ? 0.55 : 0.85;''',
 '''                double maxProjection = this.isSmallPiece() ? Double.POSITIVE_INFINITY : 2.0;''')
edit(tree,
 '''            this.applyImpulseAtPoint(normal.scale(j), point, false);

            Vec3 after = this.velocityAtPoint(point);''',
 '''            // At rest small pieces otherwise acquire angular velocity from numerical
            // single-point torque, continuously reentering the ground.
            if (this.isSmallPiece() && Math.abs(vn) < 1.0 &&
                    this.angularVelocity.lengthSqr() < 0.36 && normal.y > 0.60) {
                this.velocity = this.velocity.add(normal.scale(-Math.min(0.0,this.velocity.dot(normal))));
                this.angularVelocity = this.angularVelocity.scale(0.60);
                return;
            }
            this.applyImpulseAtPoint(normal.scale(j), point, false);

            Vec3 after = this.velocityAtPoint(point);''')
edit(tree,
 '''            if (!held) this.stabilizeRestingContact();
            this.resolvePlayerSupportAndCarry();''',
 '''            if (!held) this.stabilizeRestingContact();
            if (!held && this.isSmallPiece() && collided && this.supportContact
                    && this.hasWorldSupport() && this.velocity.lengthSqr() < 0.09
                    && this.angularVelocity.lengthSqr() < 0.0625) {
                this.velocity=Vec3.ZERO;
                this.angularVelocity=Vec3.ZERO;
                this.sleeping=true;
                this.quietTicks=Math.max(this.quietTicks,4);
            }
            this.resolvePlayerSupportAndCarry();''')
# Normalize bark RGB toward the original brick color; previous multiplier was ~126%.
edit('build.gradle','float shade = Math.max(0.48f, Math.min(1.38f, luma / 0.72f))',
                    'float shade = Math.max(0.62f, Math.min(1.16f, luma / 0.96f))')
edit('gradle.properties','mod_version=0.3.1','mod_version=0.3.2')
models=root/'src/main/resources/assets/lumberlands/models/block'
for p in models.glob('lt2_*.json'):
    raw=p.read_text()
    if '"shade": false' in raw and not any(k in p.stem for k in
       ('cavecrawler_bark','cavecrawler_wood','spookyneon_wood','snowglow_bark','lonecave_leaf0')):
        p.write_text(raw.replace('"shade": false','"shade": true'))
# Mesh references and part dimensions taken from the 2017 user-supplied LT2 RBXL.
# Every one of these axes uses original Roblox mesh asset 145815658, which is
# external to the RBXL, so this pass aligns source proportions but cannot
# claim to be an original mesh-vertex conversion.
axes={
'gold_axe':('GoldAxe',.8,3.8,1.4,1,.8,.8),
'basic_hatchet':('BasicHatchet',.8,3.8,1.4,1,.6,.7),
'plain_axe':('Axe1',.8,3.8,1.4,1,.775,.7),
'steel_axe':('Axe2',.8,3.8,1.4,1,.8,.8),
'hardened_axe':('Axe3',.8,3.8,1.4,1,.78,.9),
'alpha_axe':('AxeAlphaTesters',.8,3.8,1.4,1,.775,.7),
'beta_axe':('AxeBetaTesters',.8,3.8,1.4,1,.775,.7),
'rukiryaxe':('Rukiryaxe',.8,3.8,1.4,.7,.775,.9),
'fire_axe':('FireAxe',.8,3.2,1,.9,.7,.65),
'silver_axe':('SilverAxe',.8,3.8,1.4,.95,.78,.85),
'end_times_axe':('EndTimesAxe',.8,3.8,1.4,.8,.77,.9),
'chicken_axe':('AxeChicken',.8,3.8,1.4,1,.775,.7),
'candy_cane_axe':('CandyCaneAxe',.6,3.2,1.2,.95,.78,.85)}
reference={}
for name,(lt,*nums) in axes.items():
    a,b,c,x,y,z=nums
    mx=(a*x)/.8; my=(b*y)/(3.8*.8); mz=(c*z)/(1.4*.8)
    path=root/'src/main/resources/assets/lumberlands/models/item'/f'{name}.json'
    model=json.loads(path.read_text())
    def scalar(val,center,mult): return round(center+(val-center)*mult,4)
    for element in model.get('elements',[]):
        for key in ('from','to'):
            v=element[key]
            element[key]=[max(-16,min(32,scalar(v[0],8,mx))),
                          max(-16,min(32,scalar(v[1],0,my))),
                          max(-16,min(32,scalar(v[2],8,mz)))]
        if 'rotation' in element:
            r=element['rotation']['origin']
            element['rotation']['origin']=[scalar(r[0],8,mx),scalar(r[1],0,my),scalar(r[2],8,mz)]
    path.write_text(json.dumps(model,indent=2)+'\n')
    reference[name]={'lt2_folder':lt,'source_part_size':[a,b,c],
                     'source_mesh_scale':[x,y,z], 'mesh_id':145815658,
                     'status':'Source-scaled block-model approximation; original mesh vertices not present in RBXL.'}
(root/'LT2_ORIGINAL_AXE_MESH_REFERENCES.json').write_text(json.dumps(reference,indent=2)+'\n')
# Catch malformed model transformations before starting the 10-minute Gradle build.
for p in root.rglob('*.json'): json.loads(p.read_text())
print('LumberLands 0.3.2 corrections applied, including 13 original LT2 axe size profiles.')
