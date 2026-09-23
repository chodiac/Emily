"""Small rendering helpers shared by all templates."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = json.loads((ROOT / "content" / "images.json").read_text(encoding="utf8"))


def esc(s):
    return html.escape(str(s), quote=True)


_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def md(text):
    """Escape text, then turn the extractor's [text](/url/) links into anchors."""
    out, pos = [], 0
    for m in _LINK.finditer(text):
        out.append(esc(text[pos:m.start()]))
        out.append(f'<a class="link-inline" href="{esc(m.group(2))}">{esc(m.group(1))}</a>')
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out).replace("\n", "<br>")


def plain(text):
    return _LINK.sub(r"\1", text)


def img(name, alt, sizes="100vw", cls="", eager=False, attrs=""):
    """Responsive <img> for an optimized asset (see tools/optimize_images.py)."""
    meta = IMAGES[name]
    ws = meta["widths"]
    srcset = ", ".join(f"/assets/img/{name}-{w}.webp {w}w" for w in ws)
    mid = ws[1] if len(ws) > 1 else ws[0]
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    return (f'<img src="/assets/img/{name}-{mid}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{meta["w"]}" height="{meta["h"]}" alt="{esc(alt)}" {load} decoding="async"'
            f'{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} {attrs}>')


def img_src(name, width=960):
    ws = IMAGES[name]["widths"]
    w = min(ws, key=lambda x: abs(x - width))
    return f"/assets/img/{name}-{w}.webp"


def price(p):
    """'4500 rsd' -> '4.500 rsd' (value unchanged, only thousands separator)."""
    m = re.match(r"\s*(\d+)\s*(.*)", p)
    if not m:
        return esc(p)
    n = f"{int(m.group(1)):,}".replace(",", ".")
    return f"{n} {esc(m.group(2) or 'rsd')}"


def num(i, width=3):
    return str(i).zfill(width)


def split_label(text):
    """Wrap words for CSS/JS line reveals while keeping the text readable without JS."""
    return esc(text)


ARROW = ('<svg class="icon-arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
         '<path d="M4 12h15m-6-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>')
