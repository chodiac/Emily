"""Convert the salon's original images into responsive WebP files.

Run from the project root:  python tools/optimize_images.py
Originals live in source-assets/original-images (downloaded from kozmetickisalonemilly.rs).
Output: assets/img/<name>-<width>.webp  (+ a manifest used by build.py for width/height).
"""
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source-assets" / "original-images"
OUT = ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

# semantic name -> original file
NAMED = {
    "hero-tretman-lica": "2025_10_woman-doing-rejuvenating-treatment-2025-02-11-13-59-29-utc-1.jpg",
    "atmosfera-ogrtac": "2023_07_h1-slider04.jpg",
    "atmosfera-maska": "2023_07_h1-slider1.jpg",
    "atmosfera-masaza": "2023_07_h1-slider2.jpg",
    "atmosfera-kupka": "2023_07_h1-slider3.jpg",
    "emilija-portret": "2025_10_photo_2025-10-04_17-55-20.jpg",
    "emilija-salon": "2025_10_photo_2025-10-04_17-55-25.jpg",
    "emilija-madero": "2025_08_28.jpg",
    "emilija-lampa": "2025_08_30.jpg",
    "tretman-para": "2025_09_WhatsApp-Image-2025-09-02-at-17.52.15_b8e337dd.jpg",
    "tretman-pinda": "2025_09_WhatsApp-Image-2025-09-02-at-17.45.25_d5718ee1.jpg",
    "tretman-ultrazvuk": "2025_08_26.jpg",
    "tretman-green-peel": "2025_09_WhatsApp-Image-2025-09-02-at-17.28.40_c3c79e7f.jpg",
    "salon-kamenje": "2025_09_WhatsApp-Image-2025-09-02-at-17.50.00_ca74b6e1.jpg",
    "tretman-maska-lice": "2025_09_WhatsApp-Image-2025-09-02-at-17.34.25_44811e36.jpg",
    "tretman-maska-crna": "2025_08_27.jpg",
    "tretman-derma-pen": "2025_08_65715_lg.jpg",
    "tretman-ledja": "2025_08_16.jpg",
    "anticelulit-rezultat-1": "2025_10_74942_lg.jpg",
    "anticelulit-rezultat-2": "2025_10_77103_lg.jpg",
    "izlog-salona": "2026_09_ChatGPT-Image-Sep-12-2026-10_38_26-PM.png",
}
GALLERY = ["66205_lg", "24", "19", "16", "20", "4", "23", "17", "21", "14", "12", "15",
           "71422_lg", "68380_lg", "77103_lg", "74942_lg", "10", "65332_lg", "8", "34", "9",
           "11", "3", "6", "1", "69373_lg", "13", "33", "22", "18", "5", "7", "65715_lg", "27", "32", "26"]

WIDTHS = [480, 960, 1600]
manifest = {}


def export(name, src):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    out_widths = []
    for tw in WIDTHS:
        if tw > w and out_widths:
            continue
        tw = min(tw, w)
        th = round(h * tw / w)
        im.resize((tw, th), Image.LANCZOS).save(OUT / f"{name}-{tw}.webp", "WEBP", quality=78, method=6)
        out_widths.append(tw)
    if out_widths[-1] < w <= 2000:  # keep the native size for lightbox / large screens
        im.save(OUT / f"{name}-{w}.webp", "WEBP", quality=78, method=6)
        out_widths.append(w)
    manifest[name] = {"w": w, "h": h, "widths": out_widths}


for name, f in NAMED.items():
    export(name, SRC / f)
seen = set()
for g in GALLERY:
    f = SRC / (f"2025_10_{g}.jpg" if g in ("74942_lg", "77103_lg") else f"2025_08_{g}.jpg")
    if f.exists() and g not in seen:
        seen.add(g)
        export(f"galerija-{g.replace('_lg', '')}", f)

# logo
(OUT / "logo-emilly.svg").write_bytes((SRC / "2025_09_Salon-Emilly_logo-1-5.svg").read_bytes())
(ROOT / "content" / "images.json").write_text(json.dumps(manifest, indent=1), encoding="utf8")
print(len(manifest), "images")
