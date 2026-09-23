// Arc carousel — port of EVER's "tricks-slider": wrap-around cards, each rotated/offset by its
// distance from centre (rotation 6°, vertical 60%), inner image parallax (≈49%), progress bar.
// Drag with inertia (pointer), buttons, arrow keys; focus brings a card to the centre.
import { gsap, $, $$, motionOK } from '../core.js';

const ROT = 6;
const VERT = 60;
const PARALLAX = 33; // image is 150% wide → max shift one third

export function initArcs() {
  $$('[data-arc]').forEach(setup);
}

function setup(root) {
  const viewport = $('[data-arc-viewport]', root);
  const slides = $$('[data-arc-slide]', root);
  const fill = $('[data-arc-progress]', root);
  const prev = $('[data-arc-prev]', root);
  const next = $('[data-arc-next]', root);
  const n = slides.length;
  if (!n) return;

  let W = 0; let cw = 0; let gap = 0; let step = 0; let total = 0; let cardH = 0;
  let x = 0; let v = 0; let dragging = false; let startX = 0; let startOffset = 0; let lastX = 0; let lastT = 0; let moved = 0;
  let tween = null;

  function measure() {
    W = viewport.clientWidth;
    const mobile = W < 700;
    cw = mobile ? W * 0.74 : Math.min(W * 0.44, 760);
    gap = mobile ? 16 : Math.max(24, W * 0.025);
    step = cw + gap;
    total = step * n;
    cardH = cw / (16 / 10.5);
    root.style.setProperty('--arc-w', `${cw}px`);
    root.style.setProperty('--arc-h', `${cardH * (motionOK ? 1.55 : 1.2) + 70}px`);
  }

  const wrap = (val, min, max) => { const r = max - min; return ((((val - min) % r) + r) % r) + min; };

  function render() {
    const base = (W - cw) / 2;
    const top = motionOK ? cardH * 0.25 : 0;
    slides.forEach((slide, i) => {
      const pos = wrap(i * step + x, -step * 1.5, total - step * 1.5) + base - 0;
      const center = pos + cw / 2 - W / 2;
      const pc = center / (W + cw);
      let pl = (pos + cw) / (W + cw);
      pl = Math.max(0, Math.min(1, pl));
      slide.style.transform = `translate3d(${pos}px, ${top}px, 0)`;
      const wrapEl = slide._wrap || (slide._wrap = $('.arc__wrap', slide));
      const imgEl = slide._img || (slide._img = $('.arc__img', slide));
      if (motionOK) {
        wrapEl.style.transform = `translateY(${VERT * pc}%) rotate(${ROT * pc}deg)`;
        const meta = slide._meta || (slide._meta = $('.arc__meta', slide));
        meta.style.transform = `translateY(${cardH * (VERT / 100) * pc}px) rotate(${ROT * pc}deg)`;
        meta.style.transformOrigin = `50% -${cardH / 2}px`;
      }
      imgEl.style.transform = `translateX(-${PARALLAX * pl}%)`;
      const visible = Math.abs(pc) < 0.75;
      slide.setAttribute('aria-hidden', visible ? 'false' : 'true');
      slide.querySelectorAll('a').forEach((a) => (visible ? a.removeAttribute('tabindex') : a.setAttribute('tabindex', '-1')));
    });
    const p = wrap(-x, 0, total) / total;
    if (fill) fill.style.width = `${((p * n) % n) / (n - 1 || 1) * 100}%`;
  }

  function snapTo(target, dur = 1.1) {
    if (tween) tween.kill();
    const o = { x };
    tween = gsap.to(o, { x: target, duration: motionOK ? dur : 0, ease: 'expo.out', onUpdate: () => { x = o.x; render(); } });
  }
  const nearest = (val) => Math.round(val / step) * step;
  const go = (dir) => snapTo(nearest(x) - dir * step);

  // inertia loop
  function tick() {
    if (dragging || Math.abs(v) < 0.2) return;
    x += v;
    v *= 0.93;
    render();
    if (Math.abs(v) < 2) { v = 0; snapTo(nearest(x), 0.9); gsap.ticker.remove(tick); }
  }

  viewport.addEventListener('pointerdown', (e) => {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    dragging = true; moved = 0;
    if (tween) tween.kill();
    gsap.ticker.remove(tick);
    startX = lastX = e.clientX; startOffset = x; lastT = performance.now(); v = 0;
    viewport.setPointerCapture(e.pointerId);
    document.documentElement.classList.add('is-grabbing');
    $('[data-cursor-el]')?.classList.add('is-down');
  });
  viewport.addEventListener('pointermove', (e) => {
    if (!dragging) return;
    const dx = e.clientX - startX;
    moved = Math.max(moved, Math.abs(dx));
    if (moved > 6) root.classList.add('is-dragging');
    x = startOffset + dx;
    const now = performance.now();
    v = ((e.clientX - lastX) / Math.max(1, now - lastT)) * 16;
    lastX = e.clientX; lastT = now;
    render();
  });
  const end = () => {
    if (!dragging) return;
    dragging = false;
    document.documentElement.classList.remove('is-grabbing');
    $('[data-cursor-el]')?.classList.remove('is-down');
    setTimeout(() => root.classList.remove('is-dragging'), 0);
    if (Math.abs(v) > 2 && motionOK) gsap.ticker.add(tick);
    else snapTo(nearest(x), 0.9);
  };
  viewport.addEventListener('pointerup', end);
  viewport.addEventListener('pointercancel', end);
  viewport.addEventListener('click', (e) => { if (moved > 6) { e.preventDefault(); e.stopPropagation(); } }, true);
  viewport.addEventListener('dragstart', (e) => e.preventDefault());

  prev?.addEventListener('click', () => go(-1));
  next?.addEventListener('click', () => go(1));
  root.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); go(1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); }
  });
  slides.forEach((slide, i) => {
    slide.addEventListener('focusin', () => {
      // bring focused card to the centre, choosing the closest wrapped position
      const target = -i * step;
      const k = Math.round((x - target) / total);
      snapTo(target + k * total, 0.8);
    });
  });

  measure();
  root.classList.add('is-ready');
  x = 0;
  render();
  let rq;
  window.addEventListener('resize', () => { cancelAnimationFrame(rq); rq = requestAnimationFrame(() => { measure(); x = nearest(x); render(); }); });

  // gentle entrance: cards sweep in from the right
  if (motionOK) {
    const o = { x: -step * 1.5 };
    x = o.x; render();
    gsap.to(o, {
      x: 0, duration: 2, ease: 'expo.out',
      scrollTrigger: { trigger: root, start: 'top 80%', once: true },
      onUpdate: () => { if (!dragging) { x = o.x; render(); } },
    });
  }
}
