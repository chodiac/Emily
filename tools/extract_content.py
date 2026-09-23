"""Extract the original Salon Emilly copy from the saved WordPress pages.

Run once from the project root:  python tools/extract_content.py
Reads  source-assets/original-pages/<slug>.html  (downloaded 2026-09-23)
Writes content/extracted/<slug>.json  — headings, paragraphs (internal links kept as
markdown [text](/path/)), price lists, FAQ (from the page's FAQPage schema) and SEO meta.
The hand-curated content/site.json references these files; nothing is paraphrased here.
"""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source-assets" / "original-pages"
OUT = ROOT / "content" / "extracted"
OUT.mkdir(parents=True, exist_ok=True)
DOMAIN = "https://kozmetickisalonemilly.rs"

PAGES = ["higijenski-tretmani-lica", "ultrazvucno-ciscenje-lica", "beauty-tretmani",
         "revitalizujuci-tretmani", "lux-tretmani", "green-peel-tretmani",
         "higijenski-tretmani-ledja", "dodaci-tretmanima", "masaze", "madero-masaze",
         "anticelulit-masaze", "kozmeticki-salon-vozdovac", "kozmeticki-salon-dusanovac",
         "kozmeticki-salon-sumice", "home", "o-nama", "kontakt", "galerija"]


def local(href):
    if href.startswith(DOMAIN):
        href = href[len(DOMAIN):] or "/"
    return href


class Blocks(HTMLParser):
    """Collects h1-h4 / p / li text in document order, plus price-list pairs."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.cur, self.tag, self.skip = [], None, None, 0
        self.href = None
        self.price_title = None
        self.cls_stack = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class") or ""
        self.cls_stack.append(cls)
        if tag in ("script", "style", "svg", "noscript"):
            self.skip += 1
        if "elementor-menu-list-title" in cls:
            self.tag, self.cur = "price-title", []
        elif "elementor-menu-list-price" in cls:
            self.tag, self.cur = "price", []
        elif tag in ("h1", "h2", "h3", "h4", "p") and self.cur is None:
            self.tag, self.cur = tag, []
        elif tag == "a" and self.cur is not None and a.get("href"):
            self.href = local(a["href"])
            self.cur.append("\x00")
        elif tag == "br" and self.cur is not None:
            self.cur.append("\n")

    def handle_endtag(self, tag):
        cls = self.cls_stack.pop() if self.cls_stack else ""
        if tag in ("script", "style", "svg", "noscript"):
            self.skip -= 1
        if tag == "a" and self.href is not None and self.cur is not None:
            text = "".join(self.cur)
            i = text.rfind("\x00")
            inner = text[i + 1:]
            self.cur = [text[:i] + (f"[{inner.strip()}]({self.href})" if inner.strip() else "") +
                        (" " if inner.endswith(" ") else "")]
            self.href = None
            return
        closing = (self.tag in ("price-title", "price") and tag == "div") or tag == self.tag
        if self.cur is not None and closing:
            text = re.sub(r"[ \t\r\f\v]+", " ", "".join(self.cur)).replace("\x00", "")
            text = "\n".join(s.strip() for s in text.split("\n")).strip()
            if text:
                self.blocks.append((self.tag, text))
            self.cur, self.tag = None, None

    def handle_data(self, data):
        if self.cur is not None and not self.skip:
            self.cur.append(data)


def parse(slug):
    raw = (SRC / f"{slug}.html").read_text(encoding="utf8")
    meta = {
        "title": html.unescape(re.search(r"<title>(.*?)</title>", raw, re.S).group(1).strip()),
        "description": html.unescape((re.search(r'<meta name="description" content="([^"]*)"', raw) or [None, ""])[1]),
    }
    faq = []
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', raw, re.S):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        for node in data.get("@graph", [data]):
            if node.get("@type") == "FAQPage":
                for q in node["mainEntity"]:
                    faq.append({"q": q["name"].strip(), "a": q["acceptedAnswer"]["text"].strip()})
    start = raw.find('data-elementor-type="wp-page"')
    body = raw[start:].split('data-elementor-type="footer"')[0]
    p = Blocks()
    p.feed(body)
    blocks, seen = [], set()
    for tag, text in p.blocks:
        # responsive duplicates (same widget rendered twice for mobile/desktop)
        key = (tag, text)
        if tag not in ("price", "price-title") and key in seen:
            continue
        seen.add(key)
        blocks.append({"t": tag, "text": text})
    # header template title (e.g. "Masaže u Beogradu") lives above wp-page
    h1 = re.findall(r'<h1 class="elementor-heading-title[^>]*>(.*?)</h1>', raw[:start], re.S)
    return {"slug": slug, "meta": meta, "headerTitle": html.unescape(h1[0].strip()) if h1 else None,
            "faq": faq, "blocks": blocks}


for slug in PAGES:
    data = parse(slug)
    (OUT / f"{slug}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf8")
    print(slug, len(data["blocks"]), "blocks", len(data["faq"]), "faq", data["headerTitle"])


def reviews():
    """Client reviews from the home page (name, source link, quote) — verbatim."""
    txt = (SRC / "home.txt").read_text(encoding="utf8")
    sec = txt.split("Iskustva naših klijenata", 1)[1].split("Zakažite termin već danas", 1)[0]
    out = []
    for m in re.finditer(r"\[A (https?://[^\]]+)\]([^\n]+?)\s*\n“(.*?)”", sec, re.S):
        url, name, quote = m.group(1), m.group(2).strip(), m.group(3).strip()
        source = "Sredi me" if "sredime" in url else "Google"
        out.append({"name": name, "source": source, "quote": quote})
    (OUT / "reviews.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf8")
    print(len(out), "reviews")


reviews()
