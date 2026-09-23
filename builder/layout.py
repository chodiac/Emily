"""Page shell: <head>, loader, navigation, full-screen menu, transition curtain, footer."""
import json
from .util import esc, ARROW, img_src

LOGO = "/assets/img/logo-emilly.svg"
SITE_URL = "https://kozmetickisalonemilly.rs"
# Runs before paint: sets js/motion flags, first-visit loader and page-entry state, with a safety timeout.
BOOT = """<script>(function(d){var h=d.documentElement;h.classList.replace('no-js','js');
var q=location.search,m=null;try{m=(q.match(/[?&]motion=(full|reduce)/)||[])[1]||null;if(m)localStorage.setItem('emilly-motion',m);else m=localStorage.getItem('emilly-motion');}catch(e){}
if(m!=='reduce'){h.classList.add('motion');}
if(/[?&]raw(&|$)/.test(q))h.classList.add('raw-scroll');
try{if(!sessionStorage.getItem('emilly:visited')&&h.classList.contains('motion'))h.classList.add('is-loading');
if(sessionStorage.getItem('emilly:transition'))h.classList.add('is-entering');}catch(e){}
setTimeout(function(){if(!window.__emilly){h.classList.remove('motion','is-loading','is-entering');}},5000);})(document);</script>"""


def head(title, description, path, extra_ld=None):
    ld = [{
        "@context": "https://schema.org", "@type": "BeautySalon",
        "name": "Kozmetički salon Emilly", "url": SITE_URL + "/",
        "telephone": "+381641162333", "email": "salonemilly7@gmail.com",
        "address": {"@type": "PostalAddress", "streetAddress": "Ustanička 84b",
                    "addressLocality": "Beograd", "postalCode": "11000", "addressCountry": "RS"},
        "geo": {"@type": "GeoCoordinates", "latitude": 44.80128175605488, "longitude": 20.483160981930194},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "12:00", "closes": "20:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "17:00"}],
    }]
    if extra_ld:
        ld.append(extra_ld)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f"""<!doctype html>
<html lang="sr-Latn" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{SITE_URL}/assets/img/hero-tretman-lica-1600.webp">
<meta name="theme-color" content="#1a2c2b">
<link rel="icon" href="{LOGO}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Manrope:wght@300;400;500;600&display=swap&subset=latin-ext" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/main.css">
{BOOT}
{ld_html}
</head>"""


def loader():
    return f"""<div class="loader" data-loader aria-hidden="true">
  <div class="loader__mark"><span class="loader__mask"><img src="{LOGO}" alt="" width="120" height="102"></span>
    <span class="loader__word"><span>Salon</span> <span>Emilly</span></span></div>
  <div class="loader__count"><span data-loader-count>0</span></div>
  <div class="loader__bar"><span data-loader-bar></span></div>
</div>
<div class="curtain" data-curtain aria-hidden="true"><div class="curtain__panel"><img src="{LOGO}" alt="" width="84" height="72"></div></div>"""


def nav(site, current):
    s = site["salon"]
    services = site["services"]
    items = "".join(
        f'<li><a class="menu__svc" href="{x["url"]}" data-img="{img_src(x["image"], 960)}"{" aria-current=page" if current == x["url"] else ""}>'
        f'<span class="menu__num">{x["number"]}</span><span class="menu__label">{esc(x["name"])}</span>{ARROW}</a></li>'
        for x in services)
    pages = [("/", "Početna"), ("/o-nama/", "O nama"), ("/usluge/", "Usluge"), ("/galerija/", "Galerija"), ("/kontakt/", "Kontakt")]
    secondary = "".join(f'<li><a href="{u}"{" aria-current=page" if current == u else ""}>/ {esc(t)}</a></li>' for u, t in pages)
    social = "".join(f'<li><a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["name"])}</a></li>' for x in s["social"])
    return f"""<a class="skip-link" href="#main">Preskoči na sadržaj</a>
<header class="nav" data-nav>
  <button class="nav__burger" type="button" aria-expanded="false" aria-controls="menu" data-menu-toggle>
    <span class="burger" aria-hidden="true"><i class="burger__top"></i><i class="burger__mid"></i><i class="burger__mid2"></i><i class="burger__bot"></i></span>
    <span class="nav__burger-label"><span data-menu-label>Meni</span></span>
  </button>
  <a class="nav__logo" href="/" aria-label="Salon Emilly – početna"><img src="{LOGO}" alt="" width="46" height="39"><span>Emilly</span></a>
  <a class="nav__cta btn-line" href="/kontakt/"><span>Zakaži termin</span><i class="btn-line__fill" aria-hidden="true"></i></a>
</header>
<div class="menu" id="menu" data-menu hidden>
  <div class="menu__inner">
    <div class="menu__col menu__col--left">
      <p class="menu__giant" aria-hidden="true">Meni</p>
      <ul class="menu__social">{social}</ul>
      <nav aria-label="Stranice"><ul class="menu__pages">{secondary}</ul></nav>
      <div class="menu__booking">
        <p class="eyebrow">Za zakazivanje</p>
        <ul>
          <li><a href="tel:{s['phoneIntl']}">/ Pozovite {esc(s['phoneDisplay'])}</a></li>
          <li><a href="{s['whatsapp']}" target="_blank" rel="noopener">/ Zakažite putem WhatsApp-a</a></li>
          <li><a href="{s['viber']}">/ Zakažite putem Vibera</a></li>
        </ul>
      </div>
    </div>
    <nav class="menu__col menu__col--right" aria-label="Usluge">
      <p class="eyebrow">Usluge</p>
      <ul class="menu__list" data-dim-group>{items}</ul>
    </nav>
  </div>
  <div class="menu__media" aria-hidden="true"></div>
</div>"""


def footer(site):
    s = site["salon"]
    svc = "".join(f'<li><a href="{x["url"]}">{esc(x["name"])}</a></li>' for x in site["services"])
    locs = "".join(f'<li><a href="{x["url"]}">Kozmetički salon {esc(x["name"])}</a></li>' for x in site["locations"])
    hours = "".join(f'<li data-day="{i}"><span>{esc(d)}</span><span>{esc(h)}</span></li>' for i, (d, h) in enumerate(s["hours"]))
    social = "".join(f'<li><a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["name"])}</a></li>' for x in s["social"])
    return f"""<footer class="footer" data-bg="pine">
  <div class="footer__cta">
    <p class="eyebrow">Zakažite termin već danas</p>
    <a class="footer__big-link" href="/kontakt/" data-magnet><span class="footer__big-text">Zakaži termin</span>{ARROW}</a>
    <div class="footer__quick">
      <a class="btn-line" href="tel:{s['phoneIntl']}"><span>{esc(s['phoneDisplay'])}</span><i class="btn-line__fill" aria-hidden="true"></i></a>
      <a class="btn-line" href="{s['whatsapp']}" target="_blank" rel="noopener"><span>WhatsApp</span><i class="btn-line__fill" aria-hidden="true"></i></a>
      <a class="btn-line" href="{s['viber']}"><span>Viber</span><i class="btn-line__fill" aria-hidden="true"></i></a>
    </div>
  </div>
  <div class="footer__grid">
    <div><h2 class="footer__h">Naše usluge</h2><ul class="footer__list">{svc}</ul></div>
    <div><h2 class="footer__h">Navigacija</h2><ul class="footer__list">
      <li><a href="/">Početna</a></li><li><a href="/o-nama/">O nama</a></li><li><a href="/usluge/">Usluge i cenovnik</a></li>
      <li><a href="/galerija/">Galerija</a></li><li><a href="/kontakt/">Kontakt</a></li></ul>
      <h2 class="footer__h footer__h--gap">Lokacija</h2><ul class="footer__list">{locs}</ul></div>
    <div><h2 class="footer__h">Kontakt</h2>
      <address class="footer__address">{esc(s['address'])},<br>{esc(s['city'])}<br><span class="muted">Linije: {esc(s['transit'])}</span></address>
      <ul class="footer__list"><li><a href="tel:{s['phoneIntl']}">{esc(s['phoneDisplay'])}</a></li><li><a href="mailto:{s['email']}">{esc(s['email'])}</a></li></ul>
      <ul class="footer__social">{social}</ul></div>
    <div><h2 class="footer__h">Radno vreme</h2><ul class="hours" data-hours>{hours}</ul></div>
  </div>
  <div class="footer__word" aria-hidden="true"><span data-footer-word>Emilly</span></div>
  <div class="footer__legal"><p>© <span data-year>2026</span> Kozmetički salon Emilly – Sva prava zadržana</p>
    <button class="motion-toggle" type="button" data-motion-toggle aria-pressed="true">Animacije: <span data-motion-state>uključene</span></button>
    <a href="#top" data-scroll-top>Nazad na vrh ↑</a></div>
</footer>"""


def scripts():
    return """<div class="cursor" data-cursor-el aria-hidden="true"><span data-cursor-label>Prevuci</span></div>
<script src="/assets/vendor/gsap.min.js" defer></script>
<script src="/assets/vendor/ScrollTrigger.min.js" defer></script>
<script src="/assets/vendor/lenis.min.js" defer></script>
<script type="module" src="/assets/js/main.js"></script>"""


def page(site, *, title, description, path, body, page_id, extra_ld=None, theme="dark"):
    return f"""{head(title, description, path, extra_ld)}
<body id="top" data-page="{page_id}" data-nav-theme="{theme}">
{loader()}
{nav(site, path)}
<main id="main" class="main">
{body}
</main>
{footer(site)}
{scripts()}
</body>
</html>
"""
