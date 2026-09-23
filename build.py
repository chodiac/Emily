"""Build the static Salon Emilly site into ./site

    python build.py            # render all pages + bundle CSS

Content:   content/site.json (curated) + content/extracted/*.json (verbatim original copy)
Templates: builder/*.py      Styles: src/css/*.css (concatenated in order)
Scripts:   site/assets/js/   (native ES modules, no bundling needed)
"""
from pathlib import Path
from builder.content import load
from builder import pages

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
CSS_ORDER = ["tokens.css", "base.css", "chrome.css", "components.css", "home.css", "pages.css", "motion.css"]


def write(path, html):
    out = SITE / (path.lstrip("/") if path.endswith(".html") else path.lstrip("/") + "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf8")
    return out


def main():
    site = load()
    svcs = site["services"]
    built = [pages.home(site), pages.about(site), pages.services(site), pages.gallery(site),
             pages.contact(site), pages.not_found(site)]
    for i, s in enumerate(svcs):
        built.append(pages.service(site, s, svcs[(i + 1) % len(svcs)]))
    for loc in site["locations"]:
        built.append(pages.location(site, loc))
    for path, html in built:
        write(path, html)
    css = "\n".join(f"/* ---- {f} ---- */\n" + (ROOT / "src" / "css" / f).read_text(encoding="utf8") for f in CSS_ORDER)
    (SITE / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (SITE / "assets" / "css" / "main.css").write_text(css, encoding="utf8")
    print(f"built {len(built)} pages, {sum(len(s['prices']) for s in svcs)} prices, css {len(css) // 1024} KB")


if __name__ == "__main__":
    main()
