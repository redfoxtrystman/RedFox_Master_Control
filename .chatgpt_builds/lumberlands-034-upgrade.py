#!/usr/bin/env python3
"""Construct Minecraft native rendering resources from ACTUAL Roblox LT2 source assets."""
from pathlib import Path
import urllib.request, gzip, struct, re, shutil, json
root=Path('.')
items=root/'src/main/resources/assets/lumberlands'
meshes=items/'meshes'; meshes.mkdir(parents=True,exist_ok=True)
textures=items/'textures/item'; textures.mkdir(parents=True,exist_ok=True)
assets={
 145815658: meshes/'roblox_raw_axe_mesh.bin',
 145815673: textures/'lt2_original_axe.png',
 290304565: textures/'lt2_original_hardened.png',
 290568345: textures/'lt2_original_beta.png',
 333816720: textures/'lt2_original_fire.png',
}
for asset,output in assets.items():
 request=urllib.request.Request(
   'https://assetdelivery.roblox.com/v1/asset/?id='+str(asset),
   headers={'User-Agent':'RobloxStudio/WinInet'})
 with urllib.request.urlopen(request,timeout=60) as response: data=response.read(15000000)
 if len(data)<10000: raise RuntimeError('Roblox asset unexpectedly short '+str(asset))
 # Roblox delivers textures gzip-wrapped, even though the underlying bytes
 # are PNG. Shipping those compressed bytes as .png caused Minecraft's
 # black/magenta missing-texture fallback on *every* original LT2 axe.
 if output.suffix.lower()=='.png':
  data=gzip.decompress(data) if data.startswith(b'\x1f\x8b') else data
  if not data.startswith(b'\x89PNG\r\n\x1a\n'):
   raise RuntimeError('Not a decoded PNG for Roblox asset '+str(asset))
  import struct
  width,height=struct.unpack('>II',data[16:24])
  if width<32 or height<32 or width>4096 or height>4096:
   raise RuntimeError('Invalid PNG dimensions for '+str(asset))
 output.write_bytes(data)
 print('Retrieved and validated asset',asset,len(data),'bytes')
raw=assets[145815658].read_bytes()
s=(gzip.decompress(raw) if raw.startswith(b'\x1f\x8b') else raw).decode('ascii')
head=[x.strip() for x in s.split('\n',2)[:2]]
if head != ['version 1.00','2168']: raise RuntimeError('wrong Roblox mesh header '+str(head))
groups=re.findall(r'\[([^][]+)\]',s)
if len(groups)!=19512: raise RuntimeError('invalid Roblox vertex group count '+str(len(groups)))
out=meshes/'lt2_original_axe.bin'
with out.open('wb') as fp:
 fp.write(struct.pack('>i',len(groups)//3))
 for i in range(0,len(groups),3):
  p=list(map(float,groups[i].split(',')))
  n=list(map(float,groups[i+1].split(',')))
  uv=list(map(float,groups[i+2].split(',')))
  fp.write(struct.pack('>8f',*(p+n+uv[:2])))
print('Converted original axe mesh',out.stat().st_size,'bytes; 2168 triangles')
assets[145815658].unlink()
repo=Path('../../.chatgpt_builds')
dest=root/'src/main/java/com/glaziolaicefox/lumberlands'
shutil.copyfile(repo/'Lt2OriginalAxeRenderer.java',dest/'client/Lt2OriginalAxeRenderer.java')
shutil.copyfile(repo/'Lt2OriginalAxeItemMixin.java',dest/'mixin/Lt2OriginalAxeItemMixin.java')
mixins=root/'src/main/resources/lumberlands.mixins.json'
m=json.loads(mixins.read_text())
assert 'Lt2OriginalAxeItemMixin' not in m['client']
m['client'].append('Lt2OriginalAxeItemMixin')
mixins.write_text(json.dumps(m,indent=2)+'\n')
props=root/'gradle.properties'
s=props.read_text()
assert s.count('mod_version=0.3.3')==1
props.write_text(s.replace('mod_version=0.3.3','mod_version=0.3.4'))
(root/'LUMBERLANDS_0.3.4_ORIGINAL_AXE_MESH.md').write_text("""# LumberLands 0.3.4 – first genuine ROBLOX LT2 axe mesh import

- The original LT2 shared axe mesh is Roblox asset **145815658**, recovered from
  the supplied 2017 RBXL references and publicly available Roblox asset delivery.
- Decompressed 2168 real triangles (6504 vertices), normals and UV maps. Converted
  into binary mesh data and bundled directly in the mod JAR. The Minecraft
  ItemRenderer mixin draws these original triangles rather than Minecraft cuboids
  for 13 source-backed old axes.
- Original Roblox textures recovered: 145815673 (base), 290304565 (Hardened),
  290568345 (Beta), 333816720 (Fire); these replace manufactured textures
  for the matching axes. Some Roblox image aliases are not resolved from the 2017
  source; shared texture is used as fallback (not a source-exact texture claim).
- Newer axes not in the supplied 2017 RBXL keep old Minecraft approximation.
- This release builds on the 0.3.3 collision, tint, jitter and Frost corrections.
- Requires in-game testing with all three loaders. Build compilation is not a
  reliable test of the renderer being applied to an actual active Minecraft item.
""")
print('LumberLands 0.3.4 real axe mesh and texture sources staged')
