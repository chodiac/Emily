"""Build the static Salon Emilly site into the project root (GitHub Pages friendly)

    python build.py            # render all pages + bundle CSS

Content:   content/site.json (curated) + content/extracted/*.json (verbatim original copy)
Templates: builder/*.py      Styles: src/css/*.css (concatenated in order)
Scripts:   assets/js/   (native ES modules, no bundling needed)
"""
import re
from pathlib import Path
from builder.content import load
from builder import pages

ROOT = Path(__file__).resolve().parent
SITE = ROOT
CSS_ORDER = ["tokens.css", "base.css", "chrome.css", "components.css", "home.css", "pages.css", "motion.css"]


ATTR = re.compile(r'((?:href|src|srcset|data-img|data-full|data-transition-src)=")([^"]*)"')


def relativize(html, path):
    """Turn root-absolute URLs ("/kontakt/") into page-relative ones ("../kontakt/") so the site works
    from any base path (GitHub Pages project sites live under /<repo>/)."""
    depth = 0 if path.endswith(".html") or path == "/" else path.strip("/").count("/") + 1
    prefix = "../" * depth

    def fix(url):
        if url.startswith("/") and not url.startswith("//"):
            rel = prefix + url[1:]
            return rel or "./"
        return url

    def attr(m):
        name, val = m.group(1), m.group(2)
        if name.startswith("srcset"):
            val = ", ".join(" ".join([fix(part.split()[0])] + part.split()[1:]) for part in val.split(", "))
        else:
            val = fix(val)
        return f'{name}{val}"'
    return ATTR.sub(attr, html)


def write(path, html):
    html = relativize(html, path)
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
    (SITE / ".nojekyll").write_text("", encoding="utf8")
    (SITE / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (SITE / "assets" / "css" / "main.css").write_text(css, encoding="utf8")
    print(f"built {len(built)} pages, {sum(len(s['prices']) for s in svcs)} prices, css {len(css) // 1024} KB")


if __name__ == "__main__":
    main()
