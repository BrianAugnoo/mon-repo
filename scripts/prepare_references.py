#!/usr/bin/env python3
"""
prepare_references.py - Make reference images usable by humans AND by AI agents.

What it does
  1. Converts any image (avif, webp, heic*, gif, bmp, tiff, jpg, png) to PNG,
     because many agents cannot decode .avif/.webp/.heic.
  2. Downscales very large images (default: longest side 1600 px).
  3. Extracts a dominant color palette (hex + Roblox Color3.fromRGB + a plain-English
     color name) so colors in the prompt are measured, not guessed.
  4. Optionally cuts each image into a grid of tiles for zoomed-in inspection.
  5. Optionally builds one contact sheet with every reference.
  6. Writes manifest.json and manifest.md summarising everything.

Usage
  python prepare_references.py <file-or-dir> [<file-or-dir> ...] --out <out_dir>
         [--max-side 1600] [--colors 8] [--tiles 3x2] [--contact-sheet]

  * HEIC needs `pillow-heif`; if Pillow cannot open a file, the script falls back to
    ffmpeg and then ImageMagick (if installed).
"""
import argparse
import colorsys
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

IMAGE_EXTS = {".avif", ".webp", ".heic", ".heif", ".gif", ".bmp", ".tif", ".tiff",
              ".jpg", ".jpeg", ".png"}


def collect_inputs(paths):
    files = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            files += sorted(f for f in p.rglob("*") if f.suffix.lower() in IMAGE_EXTS)
        elif p.is_file():
            files.append(p)
        else:
            print(f"[warn] not found: {p}", file=sys.stderr)
    return files


def open_image(path: Path) -> Image.Image:
    """Open with Pillow; fall back to ffmpeg, then ImageMagick."""
    try:
        if path.suffix.lower() in {".heic", ".heif"}:
            try:
                import pillow_heif  # type: ignore
                pillow_heif.register_heif_opener()
            except Exception:
                pass
        im = Image.open(path)
        im.seek(0)  # first frame of animated files
        im = ImageOps.exif_transpose(im)
        im.load()
        return im
    except Exception as first_error:
        tmp = Path("/tmp") / f"_prep_{path.stem}.png"
        for cmd in (["ffmpeg", "-y", "-loglevel", "error", "-i", str(path), str(tmp)],
                    ["magick", str(path), str(tmp)],
                    ["convert", str(path), str(tmp)]):
            if shutil.which(cmd[0]):
                try:
                    subprocess.run(cmd, check=True, capture_output=True)
                    if tmp.exists():
                        return Image.open(tmp)
                except Exception:
                    continue
        raise RuntimeError(f"Cannot decode {path.name}: {first_error}")


def color_name(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    deg = h * 360
    if v < 0.15:
        return "near-black"
    if s < 0.12:
        if v > 0.88:
            return "white"
        if v > 0.6:
            return "light grey"
        return "grey" if v > 0.35 else "dark grey"
    if deg < 15 or deg >= 345:
        base = "red"
    elif deg < 40:
        base = "orange"
    elif deg < 65:
        base = "yellow/gold"
    elif deg < 165:
        base = "green"
    elif deg < 200:
        base = "cyan"
    elif deg < 250:
        base = "blue"
    elif deg < 290:
        base = "violet/purple"
    else:
        base = "magenta/pink"
    tone = "dark " if v < 0.4 else ("light " if (v > 0.85 and s < 0.5) else "")
    vivid = "vivid " if (s > 0.75 and v > 0.6) else ("muted " if s < 0.35 else "")
    return f"{tone}{vivid}{base}".strip()


def palette(im: Image.Image, n: int):
    """Dominant colors over opaque pixels only."""
    rgba = im.convert("RGBA")
    rgba.thumbnail((256, 256))
    raw = rgba.tobytes()
    px = [(raw[i], raw[i + 1], raw[i + 2]) for i in range(0, len(raw), 4) if raw[i + 3] > 128]
    if not px:
        return []
    side = max(1, int(len(px) ** 0.5))
    height = max(1, len(px) // side)
    flat = Image.new("RGB", (side, height))
    flat.frombytes(bytes(c for rgb in px[: side * height] for c in rgb))
    q = flat.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette() or []
    counts = sorted(q.getcolors() or [], reverse=True)
    total = sum(c for c, _ in counts) or 1
    out = []
    for c, idx in counts:
        r, g, b = pal[idx * 3: idx * 3 + 3]
        out.append({
            "hex": f"#{r:02X}{g:02X}{b:02X}",
            "roblox": f"Color3.fromRGB({r}, {g}, {b})",
            "name": color_name(r, g, b),
            "share_pct": round(100 * c / total, 1),
        })
    return out


def brightness(im: Image.Image) -> float:
    g = im.convert("L")
    g.thumbnail((128, 128))
    data = g.tobytes()
    return round(sum(data) / len(data) / 255, 3)


def save_tiles(im: Image.Image, out_dir: Path, stem: str, grid: str):
    cols, rows = (int(x) for x in grid.lower().split("x"))
    w, h = im.size
    names = []
    for r in range(rows):
        for c in range(cols):
            box = (c * w // cols, r * h // rows, (c + 1) * w // cols, (r + 1) * h // rows)
            p = out_dir / f"{stem}_tile_r{r + 1}c{c + 1}.png"
            im.crop(box).save(p)
            names.append(p.name)
    return names


def contact_sheet(items, out_path: Path, cell=(480, 300)):
    cols = 2 if len(items) > 1 else 1
    rows = (len(items) + cols - 1) // cols
    label_h = 22
    sheet = Image.new("RGB", (cols * cell[0], rows * (cell[1] + label_h)), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(items):
        t = im.convert("RGB")
        t.thumbnail(cell)
        x, y = (i % cols) * cell[0], (i // cols) * (cell[1] + label_h)
        d.text((x + 6, y + 4), name, fill=(235, 235, 235))
        sheet.paste(t, (x + (cell[0] - t.width) // 2, y + label_h))
    sheet.save(out_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="image files and/or directories")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--max-side", type=int, default=1600)
    ap.add_argument("--colors", type=int, default=8)
    ap.add_argument("--tiles", default=None, help="grid like 3x2 (columns x rows)")
    ap.add_argument("--contact-sheet", action="store_true")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    files = collect_inputs(args.inputs)
    if not files:
        sys.exit("No images found.")

    manifest, sheet_items = [], []
    for f in files:
        try:
            im = open_image(f)
        except Exception as e:  # keep going on a bad file
            print(f"[error] {e}", file=sys.stderr)
            continue
        has_alpha = im.mode in ("RGBA", "LA", "PA") or "transparency" in im.info
        orig_size = im.size
        im = im.convert("RGBA" if has_alpha else "RGB")
        if max(im.size) > args.max_side:
            im.thumbnail((args.max_side, args.max_side), Image.LANCZOS)
        stem = f.stem.replace(" ", "_")
        png = out / f"{stem}.png"
        im.save(png)
        entry = {
            "source": str(f),
            "png": png.name,
            "source_format": f.suffix.lower().lstrip("."),
            "original_size": list(orig_size),
            "output_size": list(im.size),
            "aspect_ratio": round(im.size[0] / im.size[1], 3),
            "has_transparency": has_alpha,
            "mean_brightness_0_1": brightness(im),
            "palette": palette(im, args.colors),
        }
        if args.tiles:
            entry["tiles"] = save_tiles(im.convert("RGB"), out, stem, args.tiles)
        manifest.append(entry)
        sheet_items.append((png.name, im))
        print(f"[ok] {f.name} -> {png.name} {im.size}")

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    lines = ["# Reference manifest", ""]
    for e in manifest:
        b = e["mean_brightness_0_1"]
        mood = "dark scene" if b < 0.35 else ("bright scene" if b > 0.6 else "mid-tone scene")
        lines += [
            f"## {e['png']}",
            f"- source: `{Path(e['source']).name}` ({e['source_format']}), "
            f"{e['original_size'][0]}x{e['original_size'][1]} px, aspect {e['aspect_ratio']}",
            f"- brightness: {b} ({mood}); transparency: {e['has_transparency']}",
            "- dominant colors:",
        ]
        lines += [f"  - `{c['hex']}` {c['name']} ({c['share_pct']}%) -> `{c['roblox']}`"
                  for c in e["palette"]]
        if e.get("tiles"):
            lines.append("- tiles: " + ", ".join(e["tiles"]))
        lines.append("")
    (out / "manifest.md").write_text("\n".join(lines))
    if args.contact_sheet and sheet_items:
        contact_sheet(sheet_items, out / "contact_sheet.png")
        print("[ok] contact_sheet.png")
    print(f"Done: {len(manifest)} image(s) -> {out}/ (see manifest.md)")


if __name__ == "__main__":
    main()