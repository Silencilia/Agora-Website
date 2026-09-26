"""Import project index images from the raw asset library.

Reads each project folder in E:\\_AGORA\\_Website\\Projects, takes its MAIN
image, and writes a web-sized derivative (max 2400 px, quality 85 JPEG) to
src/content/projects/<slug>/main.jpg. Existing derivatives are kept
unless --force is passed, so the script is safe to re-run when new projects
are added.

Usage:  python scripts/import_projects.py [--force]
"""

import sys
from pathlib import Path

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None  # sources are very large scans/renders

SOURCE = Path(r"E:\_AGORA\_Website\Projects")
DEST = Path(__file__).resolve().parents[1] / "src" / "content" / "projects"

MAX_DIM = 2400
QUALITY = 85

# Raw folder name -> URL slug
SLUGS = {
    "CAA Mengyuan Campus": "caa-mengyuan-campus",
    "computation": "computation",
    "Contentious City": "gloucester-maritime-trade-campus",
    "Custom Crafted Component": "custom-crafted-component",
    "Eisenman Studio": "eisenman-studio",
    "Imprint of Sound": "imprint-of-sound",
    "Jinqiao Art Center": "jinqiao-art-center",
    "Miami Studio": "miami-studio",
    "Minsheng Wharf": "minsheng-wharf",
    "Monument of Everyone": "monument-of-everyone",
    "NIO House": "nio-house",
    "PITA & BLOOM": "pita-bloom",
    "RAMA": "rama",
    "The Sun also Rises": "the-sun-also-rises",
    "West Zhejiang Agro-Tech Industry Park": "west-zhejiang-agro-tech-industry-park",
    "X-Lab": "x-lab",
}

# Folders without a MAIN.* image fall back to a named file
MAIN_OVERRIDES: dict[str, str] = {}


def find_main(folder: Path) -> Path | None:
    override = MAIN_OVERRIDES.get(folder.name)
    if override:
        return folder / override
    for f in folder.iterdir():
        if f.is_file() and f.stem.upper() == "MAIN":
            return f
    return None


def main() -> None:
    force = "--force" in sys.argv
    for folder in sorted(SOURCE.iterdir()):
        if not folder.is_dir():
            continue
        slug = SLUGS.get(folder.name)
        if not slug:
            print(f"!! no slug mapping for {folder.name!r} - skipped")
            continue
        src = find_main(folder)
        if not src or not src.exists():
            print(f"!! no MAIN image in {folder.name!r} - skipped")
            continue
        dest = DEST / slug / "main.jpg"
        if dest.exists() and not force:
            print(f"   {slug}: exists, skipped")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
            im.save(dest, "JPEG", quality=QUALITY, progressive=True, optimize=True)
        print(f"ok {slug}: {src.name} -> main.jpg ({dest.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
