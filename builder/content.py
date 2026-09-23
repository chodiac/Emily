"""Load curated site.json and merge in the verbatim text extracted from the original pages."""
import json
from .util import ROOT

C = ROOT / "content"


def _extracted(slug):
    return json.loads((C / "extracted" / f"{slug}.json").read_text(encoding="utf8"))


def _chapters(blocks, stop_h2=("Često postavljana pitanja", "Iskustva naših klijenata")):
    """Group h2 + following paragraphs. Returns (chapters, price_title, prices)."""
    chapters, prices, price_title = [], [], None
    cur = None
    pending_title = None
    for b in blocks:
        t, text = b["t"], b["text"]
        if t == "h2":
            if text in stop_h2:
                break
            cur = {"title": text, "paras": []}
            chapters.append(cur)
        elif t == "h3" and "u ponudi" in text.lower():
            price_title = text.rstrip(":").strip()
            cur = None
        elif t == "price-title":
            pending_title = text
        elif t == "price" and pending_title:
            prices.append({"name": pending_title, "price": text})
            pending_title = None
        elif t == "p" and cur is not None:
            cur["paras"].append(text)
    return chapters, price_title, prices


def load():
    site = json.loads((C / "site.json").read_text(encoding="utf8"))
    site["reviews"] = json.loads((C / "extracted" / "reviews.json").read_text(encoding="utf8"))
    for i, s in enumerate(site["services"], 1):
        ex = _extracted(s["slug"])
        chapters, price_title, prices = _chapters(ex["blocks"])
        s.update(index=i, number=str(i).zfill(3), meta=ex["meta"], faq=ex["faq"],
                 chapters=chapters, priceTitle=price_title, prices=prices,
                 url=f"/{s['slug']}/",
                 h1Suffix="u Beogradu")
    for loc in site["locations"]:
        ex = _extracted(loc["slug"])
        blocks = ex["blocks"]
        h1s = [b["text"] for b in blocks if b["t"] == "h1"]
        intro = []
        for b in blocks:
            if b["t"] == "h2":
                break
            if b["t"] == "p":
                intro.append(b["text"])
        chapters, _, _ = _chapters(blocks)
        # the "Tretmani lica i tela" chapter lists service cards (h3 + p) — keep its intro para and the
        # location-specific card descriptions
        cards = []
        it = iter(blocks)
        for b in it:
            if b["t"] == "h3" and b["text"].startswith("["):
                d = next(it)
                cards.append({"link": b["text"], "desc": d["text"]})
        for ch in chapters:
            if ch["title"] == "Tretmani lica i tela":
                card_descs = {c["desc"] for c in cards}
                ch["paras"] = [p for p in ch["paras"] if p not in card_descs]
                ch["cards"] = cards
        # closing paragraph after FAQ (e.g. "Ako tražite kozmetički salon u Beogradu…")
        faq_answers = {f["a"] for f in ex["faq"]}
        after = []
        seen_faq = False
        for b in blocks:
            if b["t"] == "h2" and b["text"] == "Često postavljana pitanja":
                seen_faq = True
                continue
            if seen_faq and b["t"] == "h4":
                break
            if seen_faq and b["t"] == "p" and b["text"] not in faq_answers:
                after.append(b["text"])
        loc.update(tagline=h1s[0] if h1s else "", title=h1s[1] if len(h1s) > 1 else loc["name"],
                   intro=intro, chapters=chapters, faq=ex["faq"], closing=after, meta=ex["meta"],
                   url=f"/{loc['slug']}/")
    home = _extracted("home")
    site["homeText"] = home
    site["homeMeta"] = home["meta"]
    paras, grab = [], False
    for b in home["blocks"]:
        if b["t"] == "h2" and b["text"] == "Salon Emilly":
            grab = True
            continue
        if grab and b["t"] == "h2":
            break
        if grab and b["t"] == "p":
            paras.append(b["text"])
    site["homeIntro"] = paras
    voucher, grab = [], False
    for b in home["blocks"]:
        if b["t"] == "h3" and b["text"] == "Poklon vaučer":
            grab = True
            continue
        if grab and b["t"] == "h2":
            break
        if grab:
            voucher.append(b)
    site["voucher"] = voucher
    about = _extracted("o-nama")
    site["aboutMeta"] = about["meta"]
    site["aboutParas"] = [b["text"] for b in about["blocks"] if b["t"] == "p"][:8]
    site["contactMeta"] = _extracted("kontakt")["meta"]
    return site
