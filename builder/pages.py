"""Page bodies. Each function returns (path, html)."""
import re
from urllib.parse import quote
from .util import esc, md, img, img_src, price, num, plain, ARROW
from .components import (btn, eyebrow, arc_carousel, cta_expand, faq, price_rows, marquee, reviews,
                         counters, next_service)
from .layout import page

# Salon photos that are not before/after shots — used for atmosphere compositions
SALON_PHOTOS = [
    ("tretman-para", "Tretman lica uz paru u salonu Emilly"),
    ("emilija-portret", "Emilija Bojić, kozmetičarka i vlasnica salona Emilly"),
    ("tretman-pinda", "Pinda sweda – priprema za masažu u salonu Emilly"),
    ("tretman-ultrazvuk", "Ultrazvučni tretman lica u salonu Emilly"),
    ("salon-kamenje", "Kutak za masažu vulkanskim kamenjem u salonu Emilly"),
    ("tretman-green-peel", "Green peel tretman u salonu Emilly"),
    ("emilija-lampa", "Emilija Bojić pri pripremi tretmana"),
    ("tretman-maska-lice", "Maska za lice tokom tretmana u salonu Emilly"),
    ("emilija-madero", "Emilija Bojić sa alatima za madero masažu"),
    ("tretman-maska-crna", "Maska za lice – beauty tretman u salonu Emilly"),
]


def split_title(text):
    """Split a title into word spans; JS turns them into line masks."""
    return esc(text)


# ---------------------------------------------------------------- HOME
def home(site):
    s, h = site["salon"], site["home"]
    services = site["services"]
    home_svcs = [x for x in services if x["home"]]
    intro = site["homeIntro"]

    arc = arc_carousel([{"image": x["image"], "alt": x["alt"], "title": x["name"], "url": x["url"]} for x in services],
                       "Kategorije tretmana")

    float_imgs = [("emilija-portret", "Emilija Bojić, kozmetičarka i vlasnica salona Emilly", "a"),
                  ("tretman-para", "Tretman lica uz paru", "b"),
                  ("salon-kamenje", "Enterijer salona Emilly", "c"),
                  ("emilija-salon", "Emilija Bojić u salonu Emilly", "d"),
                  ("tretman-green-peel", "Green peel tretman", "e"),
                  ("emilija-madero", "Madero masaža – alati", "f")]
    left = "".join(f'<figure class="float__fig float__fig--{k}" data-float-fig>{img(n, a, "(max-width: 800px) 45vw, 22vw")}</figure>' for n, a, k in float_imgs[:3])
    right = "".join(f'<figure class="float__fig float__fig--{k}" data-float-fig>{img(n, a, "(max-width: 800px) 45vw, 22vw")}</figure>' for n, a, k in float_imgs[3:])

    stage_bgs = "".join(f'<div class="stage__bg{" is-active" if i == 0 else ""}" data-stage-bg="{i}">{img(x["image"], "", "100vw")}</div>'
                        for i, x in enumerate(home_svcs))
    stage_items = "".join(f"""<li class="stage__item{' is-active' if i == 0 else ''}" data-stage-item="{i}">
  <a href="{x['url']}" data-transition="image" data-transition-src="{img_src(x['image'], 1600)}">
    <span class="stage__num">{num(i + 1, 2)}</span>
    <span class="stage__name">{esc(x['name'])}</span>
    <span class="stage__thumb" aria-hidden="true">{img(x['image'], '', '40vw')}</span>
    <span class="stage__desc"><span class="stage__desc-in"><span class="stage__text">{esc(x['short'])}</span><span class="stage__more">Više o tretmanu {ARROW}</span></span></span>
  </a></li>""" for i, x in enumerate(home_svcs))

    brands = site["about"]["brands"]
    wheel_items = "".join(f'<li class="wheel__item" data-wheel-item><span class="wheel__name">{esc(b["name"])}</span><span class="wheel__origin">{esc(b["origin"])}</span></li>' for b in brands)
    brand_para = next((p for p in site["aboutParas"] if "ponosni partner" in p), "")
    brand_note = brand_para.split("(SAD).", 1)[-1].strip() if "(SAD)." in brand_para else ""

    stack = SALON_PHOTOS[:6]
    stack_html = "".join(f'<figure class="stack__fig" data-stack-fig style="--i:{i}">{img(n, a, "(max-width: 800px) 80vw, 36vw")}</figure>' for i, (n, a) in enumerate(stack))

    voucher = site["voucher"]
    v_title = next((b["text"] for b in voucher if b["t"] == "h3"), "")
    v_paras = "".join(f'<p>{md(b["text"])}</p>' for b in voucher if b["t"] == "p")
    v_main, _, v_rest = v_title.partition(" - ")

    body = f"""
<section class="hero" data-bg="pine" aria-labelledby="hero-title">
  <div class="hero__media" data-hero-media>{img('hero-tretman-lica', 'Kozmetički salon Emilly Beograd – tretman lica', '100vw', eager=True)}</div>
  <div class="hero__shade" aria-hidden="true"></div>
  <div class="hero__content">
    <p class="eyebrow hero__eyebrow" data-hero-fade>{esc(s['address'])} · Beograd</p>
    <h1 class="hero__title" id="hero-title">
      <span class="hero__small"><span class="line-mask"><span data-hero-line>{esc(h['h1Small'])} –</span></span></span>
      <span class="hero__big"><span class="line-mask"><span data-hero-line>Salon</span></span> <span class="line-mask"><span data-hero-line><em>Emilly</em></span></span></span>
    </h1>
    <p class="hero__tagline" data-hero-fade>{esc(h['tagline'])}</p>
    <div class="hero__actions" data-hero-fade>{btn('/kontakt/', 'Zakažite termin', 'gold')}{btn('/usluge/', 'Pogledajte usluge', 'line')}</div>
  </div>
  <a class="hero__scroll" href="#uvod" data-hero-fade><span>Skrolujte</span><i aria-hidden="true"></i></a>
</section>

<section class="intro" id="uvod" data-bg="ivory" aria-labelledby="intro-title">
  <div class="intro__head">
    {eyebrow('Salon Emilly')}
    <h2 class="visually-hidden" id="intro-title">Kategorije tretmana</h2>
    <blockquote class="quote"><p class="display-m" data-split="lines">“{esc(h['quote'])}”</p></blockquote>
  </div>
  {arc}
</section>

<section class="float" data-float data-bg="sand" aria-labelledby="story-title">
  <div class="float__col float__col--l" data-float-col="-85">{left}</div>
  <div class="float__col float__col--r" data-float-col="-60">{right}</div>
  <div class="float__sticky"><div class="float__content">
    {eyebrow('O salonu')}
    <h2 class="display-l" id="story-title" data-split="lines">Vrata salona Emilly otvoriće vam <em>Emilija Bojić</em></h2>
    <p class="float__text">{md(intro[0])}</p>
    {btn('/o-nama/', 'Saznaj više', 'line')}
  </div></div>
</section>

<section class="stage" data-stage data-bg="pine" aria-labelledby="stage-title">
  <div class="stage__bgs" aria-hidden="true">{stage_bgs}<span class="stage__shade"></span></div>
  <div class="stage__inner">
    <div class="stage__head">{eyebrow('Usluge')}<h2 class="display-l" id="stage-title" data-split="lines">Nega lica <em>i tela</em></h2>
      <p class="stage__lead">{md(intro[2])}</p>{btn('/usluge/', 'Sve usluge i cenovnik', 'line')}</div>
    <ol class="stage__list" data-dim-group>{stage_items}</ol>
  </div>
</section>

{marquee(h['marquee'])}

<section class="personal" data-bg="ivory" aria-labelledby="personal-title">
  <div class="personal__text">
    {eyebrow('Individualni pristup')}
    <h2 class="display-xl personal__title" id="personal-title" data-split="chars" data-scrub>Personalizovani <em>tretmani</em></h2>
    <p class="lead">{md(intro[1])}</p>
    {counters(site)}
    {btn('/usluge/', 'Pogledajte sve usluge', 'dark')}
  </div>
  <figure class="personal__media media-reveal" data-media-reveal>{img('emilija-lampa', 'Emilija Bojić priprema tretman u salonu Emilly', '(max-width: 800px) 100vw, 42vw')}</figure>
</section>

<section class="wheel" data-wheel data-bg="pine" aria-labelledby="wheel-title">
  <div class="wheel__pin" data-pin>
    <div class="wheel__label">{eyebrow('Partneri')}<h2 class="wheel__title" id="wheel-title">Salon Emilly je ponosni partner renomiranih brendova</h2>
      <p class="wheel__note">{esc(brand_note)}</p></div>
    <div class="wheel__window"><ol class="wheel__track" data-wheel-track>{wheel_items}</ol></div>
  </div>
</section>

<section class="stack" data-stack data-bg="sand" aria-labelledby="stack-title">
  <div class="stack__pin" data-pin>
    <div class="stack__text">{eyebrow('Galerija')}<h2 class="display-l" id="stack-title" data-split="lines">Trenuci iz <em>salona</em></h2>
      <p class="stack__count" aria-hidden="true"><span data-stack-count>01</span> / {num(len(stack), 2)}</p>{btn('/galerija/', 'Pogledajte galeriju', 'line')}</div>
    <div class="stack__frames">{stack_html}</div>
  </div>
</section>

{reviews(site)}

<section class="voucher" data-bg="sand" aria-labelledby="voucher-title">
  <figure class="voucher__media media-reveal" data-media-reveal>{img('atmosfera-ogrtac', 'Trenutak opuštanja – poklon vaučer salona Emilly', '(max-width: 800px) 100vw, 50vw')}</figure>
  <div class="voucher__text">
    {eyebrow('Poklon vaučer')}
    <h2 class="display-m" id="voucher-title" data-split="lines">{esc(v_main)}</h2>
    <p class="voucher__sub">{esc(v_rest)}</p>
    <div class="prose">{v_paras}</div>
    {btn('/kontakt/?tretman=Poklon%20vau%C4%8Der', 'Poručite vaučer', 'dark')}
  </div>
</section>

{cta_expand(site, image='atmosfera-maska')}
"""
    return "/", page(site, title=site["homeMeta"]["title"], description=site["homeMeta"]["description"],
                     path="/", body=body, page_id="home")


# ---------------------------------------------------------------- ABOUT
def about(site):
    a = site["about"]
    paras = site["aboutParas"]
    story = [p for p in paras[:3]]
    mission = next((p for p in paras if p.startswith("Naša misija")), "")
    m1, _, m2 = mission.partition(". ")
    brands = "".join(f"""<li class="index-row">
  <span class="index-row__num">{num(i)}</span><span class="index-row__name">{esc(b['name'])}</span>
  <span class="index-row__meta">{esc(b['origin'])}</span><i class="rule" data-line aria-hidden="true"></i></li>""" for i, b in enumerate(a["brands"], 1))
    brand_para = next((p for p in paras if "ponosni partner" in p), "")
    brand_note = brand_para.split("(SAD).", 1)[-1].strip()
    awards = "".join(f"""<li class="award"><span class="award__num">{num(i, 2)}</span><p class="award__text">{esc(t)}</p>
  <i class="rule" data-line aria-hidden="true"></i></li>""" for i, t in enumerate(a["awards"], 1))
    row1 = "".join(f'<li class="img-marquee__item">{img(n, alt, "30vw")}</li>' for n, alt in SALON_PHOTOS[:5])
    row2 = "".join(f'<li class="img-marquee__item">{img(n, alt, "30vw")}</li>' for n, alt in SALON_PHOTOS[5:])

    body = f"""
<section class="statement" data-bg="ivory" aria-labelledby="about-title">
  <h1 class="eyebrow statement__h1" id="about-title" data-hero-fade>O nama</h1>
  <p class="statement__text display-xl"><span class="line-mask"><span data-hero-line>Nega kao</span></span> <span class="line-mask"><span data-hero-line><em>ritual lepote</em></span></span> <span class="line-mask"><span data-hero-line>i zdravlja</span></span></p>
  <p class="statement__sub" data-hero-fade>Salon Emilly · {esc(site['salon']['owner'])} · Voždovac, Beograd</p>
</section>

<section class="shrink" data-bg="ivory" aria-label="Salon Emilly">
  <figure class="shrink__frame" data-shrink>{img('emilija-portret', 'Emilija Bojić, kozmetičarka i vlasnica salona Emilly', '(max-width: 800px) 100vw, 80vw')}</figure>
</section>

<section class="story" data-bg="ivory" aria-labelledby="story-h">
  <div class="story__aside">{eyebrow('Priča')}<h2 class="display-l" id="story-h" data-split="lines">Salon <em>Emilly</em></h2>
    <figure class="story__img" data-parallax="-8">{img('emilija-salon', 'Emilija Bojić u salonu Emilly', '(max-width: 800px) 100vw, 30vw')}</figure></div>
  <div class="story__body prose prose--lg">{''.join(f'<p data-split="lines">{md(p)}</p>' for p in story)}</div>
</section>

<section class="brands" data-bg="pine" aria-labelledby="brands-h">
  <div class="brands__head">{eyebrow('Partneri')}<h2 class="display-l" id="brands-h" data-split="lines">Ponosni partner <em>renomiranih brendova</em></h2>
    <p class="brands__note">{esc(brand_note)}</p></div>
  <ol class="index" data-dim-group>{brands}</ol>
</section>

<section class="awards" data-bg="sand" aria-labelledby="awards-h">
  <div class="awards__head">{eyebrow('Priznanja')}<h2 class="display-m" id="awards-h" data-split="lines">Naša stručnost prepoznata je i <em>nagradama</em></h2></div>
  <ol class="awards__list">{awards}</ol>
</section>

<section class="mission" data-mission data-bg="pine" aria-labelledby="mission-h">
  <div class="mission__pin" data-pin>
    <div class="mission__content" data-mission-content>{eyebrow('Naša misija')}
      <h2 class="visually-hidden" id="mission-h">Naša misija</h2>
      <p class="mission__quote display-m">{esc(m1)}.</p><p class="mission__sub">{esc(m2)}</p></div>
    <div class="mission__frame" data-mission-frame>{img('atmosfera-masaza', 'Opuštajući tretman – nega kao ritual', '100vw')}</div>
  </div>
</section>

<section class="img-marquee" data-bg="ivory" aria-label="Fotografije iz salona">
  <ul class="img-marquee__row">{row1}{row1}</ul>
  <ul class="img-marquee__row img-marquee__row--rev">{row2}{row2}</ul>
  <div class="img-marquee__foot">{btn('/galerija/', 'Galerija', 'line')}</div>
</section>

{cta_expand(site, image='emilija-madero', alt='Emilija Bojić u salonu Emilly')}
"""
    return "/o-nama/", page(site, title="O nama – Kozmetički salon Emilly | Emilija Bojić, Beograd",
                            description=site["aboutMeta"]["description"], path="/o-nama/", body=body, page_id="about", theme="light")


# ---------------------------------------------------------------- SERVICES OVERVIEW
def services(site):
    svcs = site["services"]
    imgs = "".join(f'<div class="folio__img{" is-active" if i == 0 else ""}" data-folio-img="{x["slug"]}">{img(x["image"], x["alt"], "(max-width: 900px) 0px, 45vw")}</div>'
                   for i, x in enumerate(svcs))
    rows = "".join(f"""<li class="folio__row">
  <a href="{x['url']}" data-folio-item="{x['slug']}" data-transition="image" data-transition-src="{img_src(x['image'], 1600)}">
    <span class="folio__num">{x['number']}</span><span class="folio__name">{esc(x['name'])}</span>
    <span class="folio__thumb" aria-hidden="true">{img(x['image'], '', '30vw')}</span><span class="folio__tag">{esc(x['group'])}</span>{ARROW}</a>
  <i class="rule" data-line aria-hidden="true"></i></li>""" for x in svcs)
    lists = f'<li class="folio__group"><ul class="folio__rows">{rows}</ul></li>'

    chips = "".join(f'<li><a class="chip" href="#cena-{x["slug"]}">{esc(x["name"])}</a></li>' for x in svcs)
    blocks = ""
    for x in svcs:
        rows = "".join(f'<li><span>{esc(p["name"])}</span><i aria-hidden="true"></i><span class="tabular">{price(p["price"])}</span></li>' for p in x["prices"])
        blocks += f"""<article class="pricebook__block" id="cena-{x['slug']}">
  <header class="pricebook__head"><span class="pricebook__num">{x['number']}</span><h3 class="pricebook__title">{esc(x['name'])}</h3>
  <a class="btn-line" href="{x['url']}"><span>O tretmanu</span><i class="btn-line__fill" aria-hidden="true"></i></a></header>
  <ul class="pricebook__rows">{rows}</ul></article>"""
    total = sum(len(x["prices"]) for x in svcs)
    body = f"""
<section class="page-head" data-bg="ivory" aria-labelledby="svc-title">
  <p class="eyebrow" data-hero-fade>{len(svcs)} kategorija · {total} tretmana</p>
  <h1 class="display-xl" id="svc-title"><span class="line-mask"><span data-hero-line>Usluge</span></span> <span class="line-mask"><span data-hero-line><em>i cenovnik</em></span></span></h1>
  <p class="page-head__lead" data-hero-fade>{md(site['homeIntro'][2])}</p>
</section>

<section class="folio" data-bg="ivory" aria-label="Kategorije tretmana">
  <div class="folio__media" aria-hidden="true"><div class="folio__sticky">{imgs}</div></div>
  <ol class="folio__list" data-dim-group>{lists}</ol>
</section>

<section class="pricebook" data-bg="sand" aria-labelledby="price-title">
  <div class="pricebook__intro">{eyebrow('Cenovnik')}<h2 class="display-l" id="price-title" data-split="lines">Svi tretmani <em>na jednom mestu</em></h2>
    <p class="muted">Cene su preuzete sa stranica pojedinačnih tretmana. Za preporuku odgovarajućeg tretmana kontaktirajte salon.</p></div>
  <nav class="pricebook__nav" aria-label="Kategorije cenovnika"><ul>{chips}</ul></nav>
  <div class="pricebook__grid">{blocks}</div>
</section>

{cta_expand(site, image='tretman-para', alt='Tretman lica u salonu Emilly')}
"""
    return "/usluge/", page(site, title="Usluge i cenovnik – Kozmetički salon Emilly Beograd",
                            description="Svi tretmani lica i tela u salonu Emilly na Voždovcu: higijenski i ultrazvučni tretmani, beauty, revitalizujući, Green peel, lux tretmani, masaže, madero i anticelulit program – sa cenama.",
                            path="/usluge/", body=body, page_id="services", theme="light")


# ---------------------------------------------------------------- SERVICE DETAIL
GROUP_IMAGES = {
    "Lice": [("tretman-ultrazvuk", "Ultrazvučni tretman lica"), ("tretman-maska-lice", "Maska za lice tokom tretmana"),
             ("emilija-lampa", "Emilija Bojić priprema tretman"), ("tretman-para", "Tretman lica uz paru"),
             ("tretman-green-peel", "Green peel tretman"), ("emilija-portret", "Emilija Bojić")],
    "Telo": [("salon-kamenje", "Vulkansko kamenje za masažu"), ("tretman-pinda", "Pinda sweda"),
             ("emilija-madero", "Alati za madero masažu"), ("atmosfera-masaza", "Opuštajuća masaža"),
             ("emilija-salon", "Emilija Bojić u salonu"), ("atmosfera-kupka", "Trenutak opuštanja")],
}
GROUP_IMAGES["Lice i telo"] = GROUP_IMAGES["Lice"][:3] + GROUP_IMAGES["Telo"][:3]


def service(site, x, nxt):
    ch = x["chapters"]
    c1 = ch[0] if ch else {"title": "", "paras": []}
    c2 = ch[1] if len(ch) > 1 else None
    rest = ch[2:]
    pool = [p for p in GROUP_IMAGES[x["group"]] if p[0] != x["image"]][:5]
    figs = "".join(f'<figure class="float__fig float__fig--{k}" data-float-fig>{img(n, a, "(max-width: 800px) 45vw, 22vw")}</figure>'
                   for (n, a), k in zip(pool, "abcdef"))
    half = (len(pool) + 1) // 2
    figs_l = "".join(f'<figure class="float__fig float__fig--{k}" data-float-fig>{img(n, a, "(max-width: 800px) 45vw, 22vw")}</figure>' for (n, a), k in zip(pool[:half], "abc"))
    figs_r = "".join(f'<figure class="float__fig float__fig--{k}" data-float-fig>{img(n, a, "(max-width: 800px) 45vw, 22vw")}</figure>' for (n, a), k in zip(pool[half:], "def"))
    chapters_html = "".join(f"""<article class="chapter">
  <div class="chapter__head"><span class="chapter__num">{num(i + 3, 2)}</span><h2 class="display-m" data-split="lines">{esc(c['title'])}</h2></div>
  <div class="chapter__body prose">{''.join(f'<p>{md(p)}</p>' for p in c['paras'])}</div>
  <i class="rule rule--top" data-line aria-hidden="true"></i>
</article>""" for i, c in enumerate(rest))
    results = ""
    if x.get("results"):
        results = '<section class="results" data-bg="ivory" aria-label="Rezultati iz galerije"><div class="results__grid">' + "".join(
            f'<figure class="media-reveal" data-media-reveal>{img(r["image"], r["alt"], "(max-width: 800px) 100vw, 40vw")}<figcaption>Iz galerije salona</figcaption></figure>'
            for r in x["results"]) + '</div></section>'
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in x["faq"]]}
    display_name = x.get("altName", x["name"])
    body = f"""
<section class="svc-hero" data-svc-hero data-bg="pine" aria-labelledby="svc-h1">
  <div class="svc-hero__pin">
    <div class="svc-hero__content" data-svc-content>
      <p class="svc-hero__num" data-hero-fade>{x['number']} <span>/ {esc(x['group'])}</span></p>
      <h1 class="svc-hero__title" id="svc-h1"><span class="line-mask"><span data-hero-line>{esc(display_name)}</span></span>
        <span class="svc-hero__sub"><span class="line-mask"><span data-hero-line>{esc(x['h1Suffix'])}</span></span></span></h1>
      <div class="svc-hero__row" data-hero-fade>
        <span class="vscroll" aria-hidden="true"><span>Skroluj</span><i></i></span>
        <div><p class="svc-hero__lead">{esc(x['short'])}</p>
          <div class="svc-hero__actions">{btn('#cenovnik', 'Cene', 'line')}{btn('/kontakt/?kategorija=' + quote(x['name']), 'Zakaži termin', 'gold')}</div></div>
      </div>
    </div>
    <div class="svc-hero__media" data-svc-media data-transition-target><div class="svc-hero__reveal" data-svc-reveal>{img(x['image'], x['alt'], '100vw', eager=True)}</div></div>
  </div>
</section>

<nav class="crumbs" aria-label="Putanja" data-bg="ivory"><ol><li><a href="/">Početna</a></li><li><a href="/usluge/">Usluge</a></li><li aria-current="page">{esc(x['name'])}</li></ol></nav>

<section class="lede" data-bg="ivory" aria-labelledby="c1">
  <span class="chapter__num">01</span>
  <h2 class="display-l lede__title" id="c1" data-split="lines">{esc(c1['title'])}</h2>
  <div class="lede__body">{''.join(f'<p class="{"lead" if j == 0 else ""}" data-split="lines">{md(p)}</p>' for j, p in enumerate(c1['paras']))}</div>
</section>

{f'''<section class="float float--svc" data-float data-bg="sand" aria-labelledby="c2">
  <div class="float__col float__col--l" data-float-col="-80">{figs_l}</div>
  <div class="float__col float__col--r" data-float-col="-55">{figs_r}</div>
  <div class="float__sticky"><div class="float__content">
    <span class="chapter__num">02</span>
    <h2 class="display-l" id="c2" data-split="lines">{esc(c2['title'])}</h2>
    <div class="prose float__text">{''.join(f'<p>{md(p)}</p>' for p in c2['paras'])}</div>
  </div></div>
</section>''' if c2 else ''}

<section class="chapters" data-bg="ivory" aria-label="Više o tretmanu">{chapters_html}</section>

{results}

<section class="offer" id="cenovnik" data-bg="pine" aria-labelledby="offer-title">
  <div class="offer__head">{eyebrow('Cenovnik')}<h2 class="display-l" id="offer-title" data-split="lines">{esc(x['priceTitle'] or 'U ponudi')}</h2>
    <p class="muted-light">Izaberite tretman i zakažite termin – poruka će biti unapred popunjena.</p></div>
  {price_rows(x['prices'], x['name'])}
</section>

{faq(x['faq'], idp='faq-' + x['slug'])}

{next_service(nxt)}
"""
    return x["url"], page(site, title=x["meta"]["title"], description=x["meta"]["description"], path=x["url"],
                          body=body, page_id="service", extra_ld=faq_ld)


# ---------------------------------------------------------------- GALLERY
def gallery(site):
    items = [{"image": n, "alt": a, "title": a.replace(" u salonu Emilly", "")} for n, a in SALON_PHOTOS]
    grid = "".join(f"""<li class="grid__item" style="--d:{i % 3}">
  <button type="button" class="grid__btn" data-lightbox="{i}" data-full="{img_src('galerija-' + g, 1600)}" aria-label="Otvori fotografiju {i + 1} od {len(site['gallery'])}">
    {img('galerija-' + g, f'Rezultat tretmana u salonu Emilly – fotografija {i + 1}', '(max-width: 600px) 50vw, (max-width: 1100px) 33vw, 25vw')}
  </button></li>""" for i, g in enumerate(site["gallery"]))
    body = f"""
<section class="page-head page-head--center" data-bg="ivory" aria-labelledby="gal-title">
  <p class="eyebrow" data-hero-fade>{len(site['gallery'])} fotografija iz salona</p>
  <h1 class="display-xl" id="gal-title"><span class="line-mask"><span data-hero-line>Galerija</span></span></h1>
</section>
<section class="intro intro--tight" data-bg="ivory" aria-label="Trenuci iz salona">{arc_carousel(items, 'Trenuci iz salona')}</section>
<section class="gallery" data-bg="ivory" aria-labelledby="res-title">
  <div class="gallery__head">{eyebrow('Rezultati')}<h2 class="display-m" id="res-title" data-split="lines">Rezultati <em>nege</em></h2>
    <p class="muted">Fotografije pre i posle tretmana iz arhive salona. Kliknite na fotografiju za prikaz preko celog ekrana.</p></div>
  <ul class="grid">{grid}</ul>
</section>
<div class="lightbox" data-lightbox-root role="dialog" aria-modal="true" aria-label="Galerija" hidden>
  <div class="lightbox__stage" data-lightbox-stage><img alt="" data-lightbox-img></div>
  <p class="lightbox__count" aria-live="polite"><span data-lightbox-count>01</span> / {num(len(site['gallery']), 2)}</p>
  <button class="lightbox__close round-btn" type="button" data-lightbox-close aria-label="Zatvori">✕</button>
  <button class="lightbox__prev round-btn" type="button" data-lightbox-prev aria-label="Prethodna fotografija">←</button>
  <button class="lightbox__next round-btn" type="button" data-lightbox-next aria-label="Sledeća fotografija">→</button>
</div>
{cta_expand(site, image='tretman-maska-crna', alt='Beauty tretman u salonu Emilly')}
"""
    return "/galerija/", page(site, title="Galerija – Kozmetički salon Emilly Beograd",
                              description="Galerija salona Emilly: tretmani lica i tela, rezultati nege i atmosfera kozmetičkog salona na Voždovcu.",
                              path="/galerija/", body=body, page_id="gallery", theme="light")


# ---------------------------------------------------------------- CONTACT
def contact(site):
    s = site["salon"]
    hours = "".join(f'<li data-day="{i}"><span>{esc(d)}</span><span>{esc(h)}</span></li>' for i, (d, h) in enumerate(s["hours"]))
    options = "".join(f'<option>{esc(x["name"])}</option>' for x in site["services"])
    rows = [("Telefon", s["phoneDisplay"], f"tel:{s['phoneIntl']}", ""),
            ("WhatsApp", "Pošaljite poruku", s["whatsapp"], 'target="_blank" rel="noopener"'),
            ("Viber", "Pošaljite poruku", s["viber"], ""),
            ("E-mail", s["email"], f"mailto:{s['email']}", "")]
    contact_rows = "".join(f"""<li><a class="contact-row" href="{esc(u)}" {a}>
  <span class="contact-row__label">{esc(l)}</span><span class="contact-row__value">{esc(v)}</span>{ARROW}
  <i class="contact-row__fill" aria-hidden="true"></i></a><i class="rule" data-line aria-hidden="true"></i></li>""" for l, v, u, a in rows)
    body = f"""
<section class="page-head contact-head" data-bg="ivory" aria-labelledby="c-title">
  <p class="eyebrow" data-hero-fade>Kozmetički salon Emilly</p>
  <h1 class="display-xl" id="c-title"><span class="line-mask"><span data-hero-line>Kontakt</span></span></h1>
  <p class="page-head__lead" data-hero-fade>Zakažite termin telefonom, porukom ili e-mailom. {esc(s['address'])}, {esc(s['city'])}.</p>
</section>

<section class="contact" data-bg="ivory" aria-label="Kontakt podaci">
  <div class="contact__main">
    <h2 class="visually-hidden">Kontakt</h2>
    <ul class="contact__rows">{contact_rows}</ul>
    <div class="contact__meta">
      <div><h3 class="footer__h">Radno vreme</h3><ul class="hours hours--dark" data-hours>{hours}</ul></div>
      <div><h3 class="footer__h">Lokacija</h3><address>{esc(s['address'])},<br>{esc(s['city'])}</address>
        <p class="muted">Linije gradskog prevoza:<br>{esc(s['transit'])}</p>{btn(s['mapsLink'], 'Otvori u Google mapama', 'line', 'target="_blank" rel="noopener"')}</div>
    </div>
  </div>
  <figure class="contact__media media-reveal" data-media-reveal>{img('emilija-salon', 'Emilija Bojić na recepciji salona Emilly', '(max-width: 900px) 100vw, 38vw')}</figure>
</section>

<section class="map" data-bg="sand" aria-labelledby="map-title">
  <h2 class="visually-hidden" id="map-title">Mapa</h2>
  <div class="map__frame" data-map data-src="{esc(s['mapsEmbed'])}">
    {img('izlog-salona', 'Izlog kozmetičkog salona Emilly', '100vw')}
    <button class="btn btn--gold map__btn" type="button" data-map-load><span class="btn__label" data-label="Prikaži mapu"><span>Prikaži mapu</span></span>{ARROW}</button>
    <p class="map__note">Mapa se učitava sa Google servisa tek nakon klika.</p>
  </div>
</section>

<section class="trust" data-bg="pine" aria-labelledby="trust-title">
  <h2 class="visually-hidden" id="trust-title">Naše recenzije</h2>
  <div class="trust__badges">
    <a class="badge badge--light" href="{esc(s['reviewsGoogle'])}" target="_blank" rel="noopener"><span class="badge__big">{s['googleRating']}</span><span>Google recenzije</span></a>
    <a class="badge badge--light" href="{esc(s['reviewsSredime'])}" target="_blank" rel="noopener"><span class="badge__big">Top</span><span>salon · Sredi me</span></a>
  </div>
  {counters(site)}
</section>

<section class="form-sec" data-bg="ivory" aria-labelledby="form-title">
  <div class="form-sec__head">{eyebrow('Pošaljite nam poruku')}<h2 class="display-l" id="form-title" data-split="lines">Kontaktirajte <em>nas</em></h2>
    <p class="muted">Poruka se otvara u vašoj e-mail aplikaciji ili na WhatsApp-u, sa unapred popunjenim tekstom.</p></div>
  <form class="form" data-contact-form data-email="{esc(s['email'])}" data-wa="{esc(s['whatsapp'])}" novalidate>
    <div class="field"><label for="f-name">Vaše ime</label><input id="f-name" name="ime" autocomplete="name" required><span class="field__err" hidden>Unesite ime.</span></div>
    <div class="field"><label for="f-phone">Telefon <span class="muted">(opciono)</span></label><input id="f-phone" name="telefon" type="tel" autocomplete="tel"></div>
    <div class="field field--full"><label for="f-svc">Tretman</label><select id="f-svc" name="tretman"><option value="">Izaberite (opciono)</option><option>Poklon vaučer</option>{options}</select></div>
    <div class="field field--full"><label for="f-msg">Vaša poruka</label><textarea id="f-msg" name="poruka" rows="5" required></textarea><span class="field__err" hidden>Unesite poruku.</span></div>
    <div class="form__actions">
      <button class="btn btn--dark" type="submit" value="email"><span class="btn__label" data-label="Pošalji e-mail"><span>Pošalji e-mail</span></span>{ARROW}</button>
      <button class="btn btn--line-dark" type="submit" value="whatsapp"><span class="btn__label" data-label="Pošalji na WhatsApp"><span>Pošalji na WhatsApp</span></span>{ARROW}</button>
    </div>
    <p class="form__status" role="status" aria-live="polite" data-form-status></p>
  </form>
</section>
"""
    return "/kontakt/", page(site, title=site["contactMeta"]["title"], description=site["contactMeta"]["description"],
                             path="/kontakt/", body=body, page_id="contact", theme="light")


# ---------------------------------------------------------------- LOCATIONS
def location(site, loc):
    s = site["salon"]
    ch_html = ""
    for c in loc["chapters"]:
        cards = ""
        if c.get("cards"):
            cards = '<ul class="loc-cards" data-dim-group>' + "".join(
                f'<li><a href="{re.search(r"\((.*?)\)", k["link"]).group(1)}" class="loc-card"><span class="loc-card__name">{esc(plain(k["link"]))}</span>'
                f'<span class="loc-card__desc">{esc(k["desc"])}</span>{ARROW}</a></li>' for k in c["cards"]) + "</ul>"
        info = [p for p in c["paras"] if re.match(r"(Adresa|Tramvaji|Radno vreme):", p)]
        paras = [p for p in c["paras"] if p not in info]
        info_html = ('<dl class="loc-info">' + "".join(f'<div><dt>{esc(p.split(":", 1)[0])}</dt><dd>{esc(p.split(":", 1)[1].strip())}</dd></div>' for p in info) + "</dl>") if info else ""
        ch_html += f"""<article class="chapter">
  <div class="chapter__head"><h2 class="display-m" data-split="lines">{esc(c['title'])}</h2></div>
  <div class="chapter__body prose">{''.join(f'<p>{md(p)}</p>' for p in paras)}{info_html}</div>
  {cards}<i class="rule rule--top" data-line aria-hidden="true"></i></article>"""
    closing = "".join(f'<p class="lead">{md(p)}</p>' for p in loc["closing"])
    body = f"""
<section class="loc-hero" data-bg="pine" aria-labelledby="loc-title">
  <div class="loc-hero__media" data-hero-media>{img(loc['image'], loc['imageAlt'], '100vw', eager=True)}</div><div class="hero__shade" aria-hidden="true"></div>
  <div class="loc-hero__content">
    <p class="eyebrow" data-hero-fade>{esc(loc['tagline'])}</p>
    <h1 class="display-xl" id="loc-title"><span class="line-mask"><span data-hero-line>{esc(loc['title'])}</span></span></h1>
    <div data-hero-fade>{btn('/kontakt/', 'Zakažite termin', 'gold')}</div>
  </div>
</section>
<section class="lede" data-bg="ivory" aria-label="Uvod"><div class="lede__body lede__body--wide">{''.join(f'<p class="{"lead" if j == 0 else ""}" data-split="lines">{md(p)}</p>' for j, p in enumerate(loc['intro']))}</div></section>
<section class="chapters" data-bg="ivory">{ch_html}</section>
{faq(loc['faq'], idp='faq-loc')}
{f'<section class="lede" data-bg="ivory" aria-label="Zaključak"><div class="lede__body lede__body--wide">{closing}</div></section>' if closing else ''}
{cta_expand(site, image='salon-kamenje', alt='Salon Emilly')}
"""
    return loc["url"], page(site, title=loc["meta"]["title"], description=loc["meta"]["description"],
                            path=loc["url"], body=body, page_id="location")


def not_found(site):
    body = f"""<section class="page-head page-head--center nf" data-bg="ivory" aria-labelledby="nf">
  <p class="eyebrow">404</p><h1 class="display-xl" id="nf">Stranica nije <em>pronađena</em></h1>
  <p class="page-head__lead">Stranica koju tražite ne postoji ili je premeštena.</p>
  <div class="nf__actions">{btn('/', 'Početna', 'dark')}{btn('/usluge/', 'Usluge', 'line')}</div></section>"""
    return "/404.html", page(site, title="Stranica nije pronađena – Salon Emilly", description="", path="/404.html",
                             body=body, page_id="notfound", theme="light")
