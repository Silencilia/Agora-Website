"""Rebuild a project's cover + gallery derivatives from the raw asset folder.

Cover  : the source file numbered 1  -> main.jpg (max 2400 px)
Gallery: every other file, numeric order -> g01.jpg, g02.jpg, ... (max 2000 px)
         (files listed in MARKERS get a layout suffix, e.g. g09-row.jpg)
"""
from PIL import Image, ImageOps
import os, re

Image.MAX_IMAGE_PIXELS = None
MAIN_DIM, GAL_DIM, QUALITY = 2400, 2000, 85
SOURCE = r'E:\_AGORA\_Website\Projects'
DEST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'src', 'content', 'projects')

JOBS = [
    ('CAA Mengyuan Campus', 'caa-mengyuan-campus'),
    ('West Zhejiang Agro-Tech Industry Park', 'west-zhejiang-agro-tech-industry-park'),
    ('Minsheng Wharf', 'minsheng-wharf'),
    ('West Kowloon Topside Development', 'west-kowloon-topside-development'),
    ('International Land-Sea Center', 'international-land-sea-center'),
]

# slug -> {source file: layout marker}; see ProjectGallery.astro for the markers.
MARKERS = {
    'international-land-sea-center': {'p1.webp': 'row', 'p2.jpg': 'row', 'p3.jpg': 'row', 'p4.jpg': 'set'},
}

# slug -> source files whose derivative was fixed by hand; left as is on rebuild.
#   06.jpg: its three conical axons lie on their side; g05.jpg was re-rendered
#   upright from the portfolio (Portfolio_20250417.pdf, p. 58) instead.
KEEP = {
    'international-land-sea-center': {'06.jpg'},
}

def numkey(f):
    m = re.match(r'(\d+)', f)
    return (0, int(m.group(1))) if m else (1, f.lower())

def derive(src, dst, max_dim):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode != 'RGB':
            im = im.convert('RGB')
        im.thumbnail((max_dim, max_dim), Image.LANCZOS)
        im.save(dst, 'JPEG', quality=QUALITY, progressive=True, optimize=True)
        return im.size, os.path.getsize(dst) // 1024

for raw, slug in JOBS:
    srcdir = os.path.join(SOURCE, raw)
    dstdir = os.path.join(DEST, slug)
    print(f'\n=== {slug} ===')

    files = [f for f in os.listdir(srcdir)
             if os.path.isfile(os.path.join(srcdir, f))
             and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    files.sort(key=numkey)

    cover = next((f for f in files if numkey(f) == (0, 1)), None)
    assert cover, f'no source numbered 1 in {raw}'

    (w, h), kb = derive(os.path.join(srcdir, cover), os.path.join(dstdir, 'main.jpg'), MAIN_DIM)
    print(f'  main.jpg  <- {cover:10} {w}x{h}  ({kb} KB)   [COVER]')

    old = sorted(x for x in os.listdir(dstdir) if re.match(r'g\d+(-\w+)?\.jpg$', x))
    gallery = [f for f in files if f != cover]
    marks = MARKERS.get(slug, {})
    new = set()
    for i, f in enumerate(gallery, start=1):
        name = f'g{i:02d}' + (f'-{marks[f]}' if f in marks else '') + '.jpg'
        new.add(name)
        if f in KEEP.get(slug, set()):
            print(f'  {name:12} <- {f:10} (kept: fixed by hand)')
            continue
        (w, h), kb = derive(os.path.join(srcdir, f), os.path.join(dstdir, name), GAL_DIM)
        r = w / h
        tag = 'FULL-WIDTH' if r >= 1.9 else ('PORTRAIT' if r <= 0.85 else '')
        print(f'  {name:12} <- {f:10} {w}x{h} r={r:.2f} {tag}  ({kb} KB)')

    leftover = [g for g in old if g not in new]
    print(f'  !! LEFTOVER: {leftover}' if leftover else '  (no stale files)')
