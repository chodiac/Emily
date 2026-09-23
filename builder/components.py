"""Reusable section markup. Motion is attached in assets/js via data-* hooks."""
from urllib.parse import quote
from .util import esc, md, img, price, ARROW, num


def btn(href, label, kind="solid", attrs=""):
    if kind == "line":
        return (f'<a class="btn-line" href="{esc(href)}" {attrs}><span>{esc(label)}</span>'
                f'<i class="btn-line__fill" aria-hidden="true"></i></a>')
    return (f'<a class="btn btn--{kind}" href="{esc(href)}" {attrs}><span class="btn__label" data-label="{esc(label)}">'
            f'<span>{esc(label)}</span></span>{ARROW}</a>')


def eyebrow(text, cls=""):
    return f'<p class="eyebrow {cls}">{esc(text)}</p>'


def arc_carousel(items, label):
    """EVER 'tricks-slider': draggable wrap-around cards on an arc (JS), plain scroller without JS."""
    slides = []
    for i, it in enumerate(items, 1):
        inner = (f'<span class="arc__wrap"><span class="arc__img">{img(it["image"], it["alt"], "(max-width: 700px) 80vw, 46vw")}</span></span>'
                 f'<span class="arc__meta"><span class="arc__num">{num(i, 2)}</span><span class="arc__name">{esc(it["title"])}</span></span>')
        tag = (f'<a class="arc__card" href="{it["url"]}" data-transition="image" draggable="false">{inner}</a>'
               if it.get("url") else f'<div class="arc__card">{inner}</div>')
        slides.append(f'<li class="arc__slide" data-arc-slide aria-roledescription="slide" aria-label="{i} / {len(items)}">{tag}</li>')
    return f"""<div class="arc" data-arc role="region" aria-roledescription="carousel" aria-label="{esc(label)}">
  <div class="arc__viewport" data-arc-viewport data-cursor="Prevuci"><ul class="arc__track" data-arc-track>{''.join(slides)}</ul></div>
  <div class="arc__ui">
    <button class="round-btn" type="button" data-arc-prev aria-label="Prethodno"><span aria-hidden="true">←</span></button>
    <div class="arc__progress" aria-hidden="true"><span data-arc-progress></span></div>
    <button class="round-btn" type="button" data-arc-next aria-label="Sledeće"><span aria-hidden="true">→</span></button>
  </div>
</div>"""


def cta_expand(site, image="atmosfera-maska", alt="Nega lica u salonu Emilly", title="Zakažite termin već danas",
               text=None, eyebrow_text="Salon Emilly"):
    """EVER Layout 517: pinned image grows from a small frame to full viewport, content rises in."""
    s = site["salon"]
    text = text or f"{s['address']}, {s['city']} · Pon–Pet 12–20h, Sub 9–17h"
    return f"""<section class="expand" data-expand data-bg="pine" aria-labelledby="cta-title">
  <div class="expand__pin" data-pin>
    <div class="expand__frame" data-expand-frame>{img(image, alt, "100vw")}<span class="expand__shade"></span></div>
    <div class="expand__content" data-expand-content>
      {eyebrow(eyebrow_text)}
      <h2 class="display-l" id="cta-title">{esc(title)}</h2>
      <p class="expand__text">{esc(text)}</p>
      <div class="expand__actions">
        {btn('/kontakt/', 'Zakaži termin', 'gold')}
        {btn('tel:' + s['phoneIntl'], s['phoneDisplay'], 'line')}
        {btn(s['whatsapp'], 'WhatsApp', 'line', 'target="_blank" rel="noopener"')}
      </div>
    </div>
  </div>
</section>"""


def faq(items, title="Često postavljana pitanja", idp="faq"):
    rows = []
    for i, f in enumerate(items):
        rows.append(f"""<div class="faq__item">
  <h3 class="faq__q"><button type="button" aria-expanded="false" aria-controls="{idp}-{i}" id="{idp}-b{i}" data-accordion>
    <span class="faq__num">{num(i + 1, 2)}</span><span class="faq__text">{esc(f['q'])}</span><span class="faq__icon" aria-hidden="true"></span></button></h3>
  <div class="faq__a" id="{idp}-{i}" role="region" aria-labelledby="{idp}-b{i}" hidden><div class="faq__a-inner"><p>{md(f['a'])}</p></div></div>
  <i class="rule" data-line aria-hidden="true"></i>
</div>""")
    return f"""<section class="faq" data-bg="sand" aria-labelledby="{idp}-title">
  <div class="faq__head">{eyebrow('FAQ')}<h2 class="display-m" id="{idp}-title" data-split="lines">{esc(title)}</h2>
  <p class="muted">Niste pronašli odgovor? Pišite nam ili pozovite – rado ćemo odgovoriti.</p>{btn('/kontakt/', 'Kontakt', 'line')}</div>
  <div class="faq__list">{''.join(rows)}</div>
</section>"""


def price_rows(prices, service_name):
    rows = []
    for i, p in enumerate(prices, 1):
        q = esc(p["name"])
        rows.append(f"""<li class="price-row">
  <span class="price-row__num">{num(i)}</span>
  <span class="price-row__name">{esc(p['name'])}</span>
  <span class="price-row__price">{price(p['price'])}</span>
  <a class="price-row__book" href="/kontakt/?tretman={quote(p['name'])}&amp;kategorija={quote(service_name)}" aria-label="Zakaži: {q}">Zakaži {ARROW}</a>
  <i class="rule" data-line aria-hidden="true"></i>
</li>""")
    return f'<ol class="price-list" data-dim-group>{"".join(rows)}</ol>'


def marquee(words, cls=""):
    seq = "".join(f'<span class="marquee__item">{esc(w)}</span><span class="marquee__dot" aria-hidden="true">✦</span>' for w in words)
    return f"""<div class="marquee {cls}" aria-hidden="true"><div class="marquee__track" data-marquee>
  <div class="marquee__group">{seq}</div><div class="marquee__group">{seq}</div></div></div>"""


def reviews(site):
    s = site["salon"]
    cards = "".join(f"""<li class="review" data-review>
  <blockquote><p>“{esc(r['quote'])}”</p></blockquote>
  <p class="review__by"><span class="review__name">{esc(r['name'])}</span><span class="review__src">{esc(r['source'])}</span></p>
</li>""" for r in site["reviews"])
    return f"""<section class="reviews" data-bg="ivory" aria-labelledby="rev-title">
  <div class="reviews__head">
    <div>{eyebrow('Recenzije')}<h2 class="display-l" id="rev-title" data-split="lines">Iskustva naših <em>klijenata</em></h2></div>
    <div class="reviews__badges">
      <a class="badge" href="{esc(s['reviewsGoogle'])}" target="_blank" rel="noopener"><span class="badge__big">{s['googleRating']}</span><span>Google ocena</span></a>
      <a class="badge" href="{esc(s['reviewsSredime'])}" target="_blank" rel="noopener"><span class="badge__big">Top</span><span>salon na Sredi me</span></a>
    </div>
  </div>
  <div class="reviews__rail" data-drag-scroll data-cursor="Prevuci" tabindex="0" role="region" aria-label="Recenzije klijenata – prevucite ili koristite strelice">
    <ul class="reviews__track">{cards}</ul>
  </div>
  <div class="reviews__ui">
    <button class="round-btn" type="button" data-rail-prev aria-label="Prethodne recenzije"><span aria-hidden="true">←</span></button>
    <div class="arc__progress" aria-hidden="true"><span data-rail-progress></span></div>
    <button class="round-btn" type="button" data-rail-next aria-label="Sledeće recenzije"><span aria-hidden="true">→</span></button>
  </div>
</section>"""


def counters(site):
    return '<dl class="counters">' + "".join(
        f'<div class="counter"><dt>{esc(c["label"])}</dt><dd><span data-count="{c["value"]}">{c["value"]}</span>{esc(c["suffix"])}</dd></div>'
        for c in site["salon"]["counters"]) + "</dl>"


def next_service(nxt):
    return f"""<section class="next" data-bg="pine" aria-label="Sledeći tretman">
  <a class="next__link" href="{nxt['url']}" data-transition="image">
    <span class="next__media">{img(nxt['image'], nxt['alt'], '(max-width: 800px) 100vw, 50vw')}</span>
    <span class="next__text"><span class="eyebrow">Sledeći tretman · {nxt['number']}</span>
      <span class="next__name display-l">{esc(nxt['name'])}</span>
      <span class="next__go">Pogledajte tretman {ARROW}</span></span>
  </a>
</section>"""
