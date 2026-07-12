"""Import a curated, ordered set of gallery images per project.

For each project we hand-pick the strongest images (from the raw asset
library) in narrative order and write web-sized derivatives named
g01.jpg, g02.jpg ... into site/src/content/projects/<slug>/. The project
page lays them out automatically by aspect ratio.

Re-run safely; pass --force to regenerate existing derivatives.

Usage:  python scripts/import_gallery.py [--force]
"""

import sys
from pathlib import Path

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

SOURCE = Path(r"E:\_AGORA\_Website\Projects")
DEST = Path(__file__).resolve().parents[1] / "src" / "content" / "projects"

MAX_DIM = 2000
QUALITY = 82

# slug -> (raw folder, [ordered source filenames])
GALLERIES: dict[str, tuple[str, list[str]]] = {
    "jinqiao-art-center": (
        "Jinqiao Art Center",
        [
            "b2.jpg",
            "On-site axon.jpg",
            "C01.jpg",
            "C02_1.jpg",
            "b6.jpg",
            "b1+.jpg",
            "C04.jpg",
            "site plan landscape_final fixed.png",
        ],
    ),
    "nio-house": (
        "NIO House",
        [
            "DNH第十六期 DCA华熙蔚来中心-3_DCA 2.jpg",
            "1619_10_WS_230531_N17_high.jpg",
            "1619_10_WS_230531_N2_high.jpg",
            "1619_10_WS_230531_N14_high.jpg",
            "1619_10_WS_230531_N19_high.jpg",
            "1619_10_WS_230531_N3_high.jpg",
            "1619_10_WS_230531_N8_high.jpg",
            "DNH第十六期 DCA华熙蔚来中心-3_DCA 4.jpg",
            "IMG_8133.JPG",
        ],
    ),
    "miami-studio": (
        "Miami Studio",
        [
            "Main Iso_cropped.jpg",
            "DSC_0655.jpg",
            "DSC_0669.jpg",
            "DSC_0733.jpg",
            "DSC_0739.jpg",
            "Rotated Iso.jpg",
            "preservation axon.jpg",
            "single block flow.jpg",
            "4_ground floor plan.jpg",
            "STREETVIEW_cropped.jpg",
        ],
    ),
    "pita-bloom": (
        "PITA & BLOOM",
        [
            "4_TONED.jpg",
            "8_toned.jpg",
            "7_model.jpg",
            "12.jpg",
            "axon.jpg",
            "warehouse axon.jpg",
            "section a.jpg",
            "components.jpg",
        ],
    ),
    "the-sun-also-rises": (
        "The Sun also Rises",
        [
            "1.jpg",
            "3.jpg",
            "model no plots.jpg",
            "4.jpg",
            "9.jpg",
            "8b.jpg",
            "geometry.jpg",
            "section cropped.jpg",
            "6.jpg",
        ],
    ),
    "imprint-of-sound": (
        "Imprint of Sound",
        [
            "model.jpg",
            "1.jpg",
            "2.jpg",
            "4.jpg",
            "5.jpg",
            "3.jpg",
        ],
    ),
    "contentious-city": (
        "Contentious City",
        [
            "1 bw.jpg",
            "2 bw.jpg",
            "3 bw.jpg",
            "4 bw.jpg",
            "5 bw.jpg",
            "6 bw.jpg",
            "7 bw.jpg",
            "8 bw.jpg",
        ],
    ),
    "caa-mengyuan-campus": (
        "CAA Mengyuan Campus",
        [
            "1_Aerial 1.jpg",
            "10_Aerial 2.jpg",
            "3_Pavilion.jpg",
            "4_Gallery exterior.jpg",
            "5_Gallery interior.jpg",
            "9_Entrance.jpg",
            "7_Studio.jpg",
            "8_playground.jpg",
            "2_Axonometric without roof.jpg",
            "6_PLAN F01.jpg",
        ],
    ),
    "west-zhejiang-agro-tech-industry-park": (
        "West Zhejiang Agro-Tech Industry Park",
        [
            "image_2.jpg",
            "INT_1.jpg",
            "v04.jpg",
            "v05.jpg",
            "v08.jpg",
            "v09.jpg",
            "v10-A.jpg",
            "v10-B.jpg",
            "v06.jpg",
            "3.jpg",
        ],
    ),
    "rama": (
        "RAMA",
        [
            "RAMA_DCA_Preview©️RAWVISION studio-27.jpg",
            "Axon.png",
            "RAMA_DCA_Preview©️RAWVISION studio-50.jpg",
            "RAMA_DCA_Preview©️RAWVISION studio-41.jpg",
            "RAMA_DCA_Preview©️RAWVISION studio-55.jpg",
            "RAMA_DCA_Preview©️RAWVISION studio-29.jpg",
            "RAMA_DCA_Preview©️RAWVISION studio-91.jpg",
            "RAMA_DCA_Preview©️RAWVISION studio-65.jpg",
            "A.INT.jpg",
        ],
    ),
    "monument-of-everyone": (
        "Monument of Everyone",
        [
            "12290_Monument-of-Everyone_Presentation.jpg",
            "12290_Monument-of-Everyone_Functional.jpg",
            "12290_Monument-of-Everyone_Technical.jpg",
        ],
    ),
    "computation": (
        "computation",
        [
            "1.jpg",
            "1a.jpg",
            "1b.jpg",
            "2.jpg",
            "3.jpg",
            "fabrication wmq-021-bright.jpg",
            "fabrication wmq-028-bright.jpg",
            "fabrication wmq-047.jpg",
        ],
    ),
    "custom-crafted-component": (
        "Custom Crafted Component",
        [
            "3.jpg",
            "4.jpg",
            "_DSC0943.jpg",
            "_DSC0949.jpg",
            "1.jpg",
            "2.jpg",
            "passion.jpg",
            "frenzy.jpg",
            "dream.jpg",
            "swirl.jpg",
        ],
    ),
    "eisenman-studio": (
        "Eisenman Studio",
        [
            "axon 1.jpg",
            "axon 2.jpg",
            "axon 3.jpg",
            "1a.jpg",
            "1b.jpg",
            "plan 1.jpg",
            "plan 2.jpg",
            "Lichterfelde Layering_grid.jpg",
            "Lichterfelde Layering_Buldings.jpg",
        ],
    ),
    "x-lab": (
        "X-Lab",
        [
            "1.jpg",
            "1b.jpg",
            "1c.jpg",
            "2.jpg",
            "6.jpg",
            "9.jpg",
            "10.jpg",
            "11.jpg",
            "final rendering.jpg",
            "main section rotated.jpg",
            "D1.jpg",
            "D2.jpg",
        ],
    ),
}


def convert(src: Path, dest: Path) -> tuple[int, int]:
    with Image.open(src) as im:
        # Speed up decoding of very large JPEGs.
        im.draft("RGB", (MAX_DIM * 2, MAX_DIM * 2))
        im = ImageOps.exif_transpose(im)
        # Flatten transparency (e.g. PNG diagrams) onto white, not black.
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
            im = Image.alpha_composite(bg, im).convert("RGB")
        elif im.mode != "RGB":
            im = im.convert("RGB")
        im.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
        im.save(dest, "JPEG", quality=QUALITY, progressive=True, optimize=True)
        return im.size


def main() -> None:
    force = "--force" in sys.argv
    # Optional: restrict to one project, e.g. `--only rama`.
    only = None
    if "--only" in sys.argv:
        idx = sys.argv.index("--only")
        if idx + 1 < len(sys.argv):
            only = sys.argv[idx + 1]
    for slug, (folder, names) in GALLERIES.items():
        if only and slug != only:
            continue
        src_dir = SOURCE / folder
        dest_dir = DEST / slug
        dest_dir.mkdir(parents=True, exist_ok=True)
        # Clear old gallery derivatives when forcing, so removals take effect.
        if force:
            for old in dest_dir.glob("g[0-9][0-9].jpg"):
                old.unlink()
        n = 0
        for name in names:
            src = src_dir / name
            if not src.exists():
                print(f"!! {slug}: missing {name!r}")
                continue
            n += 1
            dest = dest_dir / f"g{n:02d}.jpg"
            if dest.exists() and not force:
                continue
            try:
                w, h = convert(src, dest)
                print(f"ok {slug}/g{n:02d}.jpg  {w}x{h}")
            except Exception as e:
                print(f"!! {slug}: {name!r} -> ERROR {type(e).__name__}: {e}")
                n -= 1
        print(f"   {slug}: {n} gallery images")


if __name__ == "__main__":
    main()
