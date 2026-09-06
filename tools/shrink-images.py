#!/usr/bin/env python3
"""Create web-sized image copies.

Requires Pillow: python3 -m pip install Pillow
Run from the project root: python3 tools/shrink-images.py
"""

from argparse import ArgumentParser
from pathlib import Path

from PIL import Image, ImageOps


def shrink(source: Path, destination: Path, max_width: int, quality: int) -> None:
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original)

        if image.width > max_width:
            height = round(image.height * max_width / image.width)
            image = image.resize((max_width, height), Image.Resampling.LANCZOS)

        destination.parent.mkdir(parents=True, exist_ok=True)
        suffix = destination.suffix.lower()

        if suffix in {".jpg", ".jpeg"}:
            image.convert("RGB").save(
                destination,
                quality=quality,
                optimize=True,
                progressive=True,
            )
        elif suffix == ".png":
            image.save(destination, optimize=True)
        elif suffix == ".webp":
            image.save(destination, quality=quality, method=6)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("img"))
    parser.add_argument("--output", type=Path, default=Path("img/small"))
    parser.add_argument("--max-width", type=int, default=1600)
    parser.add_argument("--quality", type=int, default=80)
    args = parser.parse_args()

    supported = {".jpg", ".jpeg", ".png", ".webp"}
    sources = (
        path
        for path in sorted(args.source.iterdir())
        if path.is_file() and path.suffix.lower() in supported
    )

    for source in sources:
        destination = args.output / source.name
        shrink(source, destination, args.max_width, args.quality)
        print(f"{source} -> {destination}")


if __name__ == "__main__":
    main()
