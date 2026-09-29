from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import hashlib
from io import BytesIO
from PIL import Image
import sys, time

out = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path('pkvault-src/frontend/public/gen1-glitch').resolve()
rb = out / 'rb'; yellow = out / 'y'; names = out / 'names'
for p in (rb, yellow, names): p.mkdir(parents=True, exist_ok=True)

BASES = [
    'https://archives.bulbagarden.net/wiki/Special:Redirect/file/',
    'https://bulbapedia.bulbagarden.net/wiki/Special:Redirect/file/',
]
UA = 'PKVault-build/alpha52x (Gen-I glitch sprite packaging; source Bulbagarden Archives)'
PNG_SIG = b'\x89PNG\r\n\x1a\n'

def fetch(filename: str) -> bytes:
    last = None
    normalized = filename.replace(' ', '_')
    encoded = quote(normalized, safe='')
    digest = hashlib.md5(normalized.encode('utf-8')).hexdigest()
    urls = [
        f'https://archives.bulbagarden.net/media/upload/{digest[0]}/{digest[:2]}/{encoded}',
        f'https://cdn.bulbagarden.net/upload/{digest[0]}/{digest[:2]}/{encoded}',
        *(base + encoded for base in BASES),
    ]
    for url in urls:
        for attempt in range(3):
            try:
                req = Request(url, headers={'User-Agent': UA, 'Referer': 'https://archives.bulbagarden.net/'})
                with urlopen(req, timeout=30) as r:
                    data = r.read()
                if not data.startswith(PNG_SIG):
                    raise RuntimeError(f'not PNG ({len(data)} bytes)')
                return data
            except Exception as e:
                last = e
                time.sleep(1 + attempt)
    raise RuntimeError(f'failed downloading {filename}: {last}')

def clear_border_white(im: Image.Image) -> Image.Image:
    im = im.convert('RGBA')
    px = im.load()
    w, h = im.size
    seen = bytearray(w * h)
    q = []

    def near_white(x, y):
        r, g, b, a = px[x, y]
        return a > 0 and r >= 238 and g >= 238 and b >= 238

    def add(x, y):
        if x < 0 or y < 0 or x >= w or y >= h:
            return
        i = y * w + x
        if seen[i] or not near_white(x, y):
            return
        seen[i] = 1
        q.append((x, y))

    for x in range(w):
        add(x, 0); add(x, h - 1)
    for y in range(h):
        add(0, y); add(w - 1, y)

    for x, y in q:
        r, g, b, _ = px[x, y]
        px[x, y] = (r, g, b, 0)
        add(x - 1, y); add(x + 1, y); add(x, y - 1); add(x, y + 1)
    return im

def normalize(filename: str, dest: Path):
    im = Image.open(BytesIO(fetch(filename))).convert('RGBA')
    im = clear_border_white(im)
    bbox = im.getchannel('A').getbbox()
    if bbox:
        im = im.crop(bbox)
    im.thumbnail((52, 52), Image.Resampling.NEAREST)
    canvas = Image.new('RGBA', (56, 56), (0, 0, 0, 0))
    canvas.alpha_composite(im, ((56 - im.width)//2, (56 - im.height)//2))
    canvas.save(dest, format='PNG', optimize=True)
    if not canvas.getchannel('A').getbbox():
        raise RuntimeError(f'empty normalized sprite: {filename}')

rb_files = {
    'missingno.png':'Missingno RB.png',
    'b6.png':'Spr 1b 141 f.png',
    'b7.png':'Spr 1b 142 f.png',
    'b8.png':'Ghost I.png',
    'fa.png':'RBGlitchFA.png',
}
for dex in (17,18,24,26,40,61,62,64,72,79,85,94,95,135,174,175,204,205,207,209,213,225,234,236,240,245,250,254,255):
    rb_files[f'dex{dex:03d}.png'] = f'RBGlitch{dex:03d}.png'

y_files = {'missingno.png':'Missingno Y.png'}
for dex in (6,9,11,15,16,18,21,27,40,53,55,62,79,80,84,85,93,121,126,127,128,143,144,159,176,195,202,203,205,206,207,215,229,230,234,245,250,254):
    y_files[f'dex{dex:03d}.png'] = f'YGlitch{dex:03d}.png'

for dest, src in rb_files.items():
    normalize(src, rb / dest)
for dest, src in y_files.items():
    normalize(src, yellow / dest)

for raw in ('E1','EC','ED','EF'):
    (names / f'RBGlitchName{raw}.png').write_bytes(fetch(f'RBGlitchName{raw}.png'))
(names / 'YGlitchNameE0.png').write_bytes(fetch('YGlitchNameE0.png'))
for src in ('RBGlitchName00.png', 'YGlitchName00.png'):
    (names / src).write_bytes(fetch(src))

(out / 'ASSET_SOURCE.txt').write_text(
    'Generation-I glitch front sprites and selected exact name tiles\n'
    'Source: Bulbagarden Archives, packaged into PKVault at build time.\n'
    'Front sprites are border-white cleaned, alpha-cropped, nearest-neighbor fitted, and centered on transparent 56x56 canvases.\n',
    encoding='utf-8')

for p in list(rb.glob('*.png')) + list(yellow.glob('*.png')) + list(names.glob('*.png')):
    if p.stat().st_size < 50:
        raise RuntimeError(f'suspiciously small packaged image: {p}')
print(f'PASS: packaged {len(rb_files)} Red/Blue + {len(y_files)} Yellow Gen-I glitch fronts and exact fallback name tiles')
