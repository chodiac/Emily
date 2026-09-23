// Interactive UI: review rail, FAQ accordion, gallery lightbox, contact form, map, hours, cursor.
import { gsap, $, $$, motionOK, finePointer, stopScroll, startScroll } from '../core.js';

export function initUI() {
  rails();
  accordions();
  lightbox();
  contactForm();
  mapLoader();
  hours();
  cursor();
  motionToggle();
  $$('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
}

/* Reviews: native horizontal scroll + mouse drag + buttons + progress */
function rails() {
  $$('[data-drag-scroll]').forEach((rail) => {
    const section = rail.parentElement;
    const fill = $('[data-rail-progress]', section);
    const card = () => (rail.querySelector('li')?.getBoundingClientRect().width || 300) + 19;
    const update = () => {
      const max = rail.scrollWidth - rail.clientWidth;
      if (fill) fill.style.width = `${max > 0 ? (rail.scrollLeft / max) * 100 : 0}%`;
    };
    rail.addEventListener('scroll', update, { passive: true });
    update();
    $('[data-rail-prev]', section)?.addEventListener('click', () => rail.scrollBy({ left: -card() * 2, behavior: motionOK ? 'smooth' : 'auto' }));
    $('[data-rail-next]', section)?.addEventListener('click', () => rail.scrollBy({ left: card() * 2, behavior: motionOK ? 'smooth' : 'auto' }));
    rail.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); rail.scrollBy({ left: card(), behavior: 'smooth' }); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); rail.scrollBy({ left: -card(), behavior: 'smooth' }); }
    });
    // mouse drag (touch uses native scrolling)
    let down = false; let sx = 0; let sl = 0; let v = 0; let lx = 0; let moved = 0;
    rail.addEventListener('pointerdown', (e) => {
      if (e.pointerType !== 'mouse' || e.button !== 0) return;
      down = true; moved = 0; sx = lx = e.clientX; sl = rail.scrollLeft; v = 0;
      rail.classList.add('is-dragging');
      $('[data-cursor-el]')?.classList.add('is-down');
    });
    window.addEventListener('pointermove', (e) => {
      if (!down) return;
      moved = Math.max(moved, Math.abs(e.clientX - sx));
      rail.scrollLeft = sl - (e.clientX - sx);
      v = e.clientX - lx; lx = e.clientX;
    });
    window.addEventListener('pointerup', () => {
      if (!down) return;
      down = false;
      rail.classList.remove('is-dragging');
      $('[data-cursor-el]')?.classList.remove('is-down');
      if (motionOK && Math.abs(v) > 2) {
        const o = { x: rail.scrollLeft };
        gsap.to(o, { x: rail.scrollLeft - v * 18, duration: 1.1, ease: 'expo.out', onUpdate: () => { rail.scrollLeft = o.x; } });
      }
    });
    rail.addEventListener('click', (e) => { if (moved > 6) e.preventDefault(); }, true);
  });
}

/* FAQ accordion (EVER FAQ 3): button + region, animated height */
function accordions() {
  $$('[data-accordion]').forEach((btn) => {
    const panel = document.getElementById(btn.getAttribute('aria-controls'));
    if (!panel) return;
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      if (!open) {
        panel.hidden = false;
        if (motionOK) gsap.fromTo(panel, { height: 0, opacity: 0 }, { height: 'auto', opacity: 1, duration: 0.7, ease: 'expo.out' });
      } else if (motionOK) {
        gsap.to(panel, { height: 0, opacity: 0, duration: 0.5, ease: 'expo.inOut', onComplete: () => { panel.hidden = true; gsap.set(panel, { clearProps: 'all' }); } });
      } else {
        panel.hidden = true;
      }
      if (window.ScrollTrigger) setTimeout(() => window.ScrollTrigger.refresh(), 750);
    });
  });
}

/* Gallery lightbox: opens from the clicked thumbnail (FLIP), arrows / swipe / Esc, focus trap */
function lightbox() {
  const box = $('[data-lightbox-root]');
  const btns = $$('[data-lightbox]');
  if (!box || !btns.length) return;
  const img = $('[data-lightbox-img]', box);
  const stage = $('[data-lightbox-stage]', box);
  const countEl = $('[data-lightbox-count]', box);
  let index = 0; let opener = null;

  const show = (i, dir = 0) => {
    index = (i + btns.length) % btns.length;
    const b = btns[index];
    const thumb = b.querySelector('img');
    img.src = b.dataset.full;
    img.alt = thumb.alt;
    countEl.textContent = String(index + 1).padStart(2, '0');
    if (motionOK && dir) gsap.fromTo(img, { xPercent: dir * 12, opacity: 0 }, { xPercent: 0, opacity: 1, duration: 0.8, ease: 'expo.out' });
  };

  const open = (i) => {
    opener = btns[i];
    box.hidden = false;
    stopScroll();
    show(i);
    if (motionOK) {
      const from = opener.getBoundingClientRect();
      const to = stage.getBoundingClientRect();
      gsap.fromTo(box, { backgroundColor: 'rgba(15,27,26,0)' }, { backgroundColor: 'rgba(15,27,26,.96)', duration: 0.6 });
      gsap.fromTo(stage, {
        x: from.left + from.width / 2 - (to.left + to.width / 2),
        y: from.top + from.height / 2 - (to.top + to.height / 2),
        scale: from.width / to.width,
      }, { x: 0, y: 0, scale: 1, duration: 0.9, ease: 'expo.inOut' });
      gsap.fromTo($$('.round-btn, .lightbox__count', box), { opacity: 0 }, { opacity: 1, duration: 0.5, delay: 0.5 });
    }
    $('[data-lightbox-close]', box).focus();
  };
  const close = () => {
    const done = () => { box.hidden = true; startScroll(); gsap.set([stage, box], { clearProps: 'all' }); opener && opener.focus(); };
    if (!motionOK) return done();
    const from = btns[index].getBoundingClientRect();
    const to = stage.getBoundingClientRect();
    gsap.to(stage, { x: from.left + from.width / 2 - (to.left + to.width / 2), y: from.top + from.height / 2 - (to.top + to.height / 2), scale: from.width / to.width, duration: 0.7, ease: 'expo.inOut' });
    gsap.to(box, { backgroundColor: 'rgba(15,27,26,0)', duration: 0.6, delay: 0.1, onComplete: done });
  };

  btns.forEach((b, i) => b.addEventListener('click', () => open(i)));
  $('[data-lightbox-close]', box).addEventListener('click', close);
  $('[data-lightbox-prev]', box).addEventListener('click', () => show(index - 1, -1));
  $('[data-lightbox-next]', box).addEventListener('click', () => show(index + 1, 1));
  box.addEventListener('click', (e) => { if (e.target === box) close(); });
  document.addEventListener('keydown', (e) => {
    if (box.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') show(index + 1, 1);
    if (e.key === 'ArrowLeft') show(index - 1, -1);
    if (e.key === 'Tab') {
      const f = $$('button', box);
      const iNow = f.indexOf(document.activeElement);
      e.preventDefault();
      f[(iNow + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
    }
  });
  let sx = null;
  stage.addEventListener('pointerdown', (e) => { sx = e.clientX; });
  stage.addEventListener('pointerup', (e) => {
    if (sx === null) return;
    const dx = e.clientX - sx; sx = null;
    if (Math.abs(dx) > 40) show(index + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1);
  });
}

/* Contact form: static site → compose e-mail or WhatsApp message with the text pre-filled */
function contactForm() {
  const form = $('[data-contact-form]');
  if (!form) return;
  const params = new URLSearchParams(location.search);
  const category = params.get('kategorija');
  const wanted = params.get('tretman') || category;
  const select = form.elements.tretman;
  const msg = form.elements.poruka;
  const opt = [...select.options].find((o) => o.text === (category || wanted));
  if (opt) select.value = opt.text;
  if (wanted) {
    msg.value = `Zdravo, zanima me termin za: ${wanted}.\nOdgovara mi: `;
  }
  select.addEventListener('change', () => {
    if (!msg.value.trim() && select.value) msg.value = `Zdravo, zanima me termin za: ${select.value}.\nOdgovara mi: `;
  });
  const status = $('[data-form-status]', form);
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    let ok = true;
    [form.elements.ime, msg].forEach((f) => {
      const bad = !f.value.trim();
      const field = f.closest('.field');
      field.classList.toggle('has-error', bad);
      field.querySelector('.field__err').hidden = !bad;
      f.setAttribute('aria-invalid', String(bad));
      if (bad && ok) { f.focus(); ok = false; }
    });
    if (!ok) { status.textContent = 'Molimo popunite označena polja.'; return; }
    const lines = [
      msg.value.trim(), '',
      `Ime: ${form.elements.ime.value.trim()}`,
      form.elements.telefon.value.trim() ? `Telefon: ${form.elements.telefon.value.trim()}` : '',
      select.value ? `Tretman: ${select.value}` : '',
    ].filter((l, i) => l || i === 1);
    const text = lines.join('\n');
    const via = e.submitter?.value || 'email';
    if (via === 'whatsapp') {
      window.open(`${form.dataset.wa}?text=${encodeURIComponent(text)}`, '_blank', 'noopener');
      status.textContent = 'Otvaramo WhatsApp sa pripremljenom porukom…';
    } else {
      const subject = select.value ? `Zakazivanje – ${select.value}` : 'Poruka sa sajta';
      window.location.href = `mailto:${form.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(text)}`;
      status.textContent = 'Otvaramo vašu e-mail aplikaciju sa pripremljenom porukom…';
    }
  });
}

/* Google map only after an explicit click (privacy + performance) */
function mapLoader() {
  const frame = $('[data-map]');
  if (!frame) return;
  $('[data-map-load]', frame).addEventListener('click', () => {
    const iframe = document.createElement('iframe');
    iframe.src = frame.dataset.src;
    iframe.title = 'Mapa – Kozmetički salon Emilly, Ustanička 84b';
    iframe.loading = 'lazy';
    iframe.referrerPolicy = 'no-referrer-when-downgrade';
    frame.appendChild(iframe);
    $$('button, .map__note', frame).forEach((n) => n.remove());
    iframe.focus();
  });
}

/* Highlight today's opening hours (Belgrade time) */
function hours() {
  let day;
  try {
    const w = new Intl.DateTimeFormat('en-US', { weekday: 'short', timeZone: 'Europe/Belgrade' }).format(new Date());
    day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].indexOf(w);
  } catch (e) { day = (new Date().getDay() + 6) % 7; }
  $$('[data-hours] li').forEach((li) => li.classList.toggle('is-today', Number(li.dataset.day) === day));
}

/* Drag label cursor on carousels / rails (desktop only) */
function cursor() {
  const c = $('[data-cursor-el]');
  if (!c || !finePointer()) return;
  const label = $('[data-cursor-label]', c);
  const xTo = gsap.quickTo(c, 'x', { duration: 0.45, ease: 'power3' });
  const yTo = gsap.quickTo(c, 'y', { duration: 0.45, ease: 'power3' });
  window.addEventListener('pointermove', (e) => { xTo(e.clientX); yTo(e.clientY); }, { passive: true });
  $$('[data-cursor]').forEach((area) => {
    area.addEventListener('pointerenter', () => { label.textContent = area.dataset.cursor; c.classList.add('is-on'); });
    area.addEventListener('pointerleave', () => c.classList.remove('is-on'));
  });
}

/* Animations are on by default; visitors who prefer less motion can switch them off (remembered) */
function motionToggle() {
  const on = document.documentElement.classList.contains('motion');
  $$('[data-motion-toggle]').forEach((btn) => {
    btn.setAttribute('aria-pressed', String(on));
    const state = btn.querySelector('[data-motion-state]');
    if (state) state.textContent = on ? 'uključene' : 'isključene';
    btn.addEventListener('click', () => {
      try { localStorage.setItem('emilly-motion', on ? 'reduce' : 'full'); } catch (e) { /* private mode */ }
      const url = new URL(location.href);
      url.searchParams.delete('motion');
      location.replace(url.href);
    });
  });
}
