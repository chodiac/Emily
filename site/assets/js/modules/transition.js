// Page transitions (new — EVER has none): a pine curtain between pages, and for treatment links an
// image hand-off — the clicked photo expands to exactly where the treatment page's hero photo sits,
// so the next page opens "inside" the image.
import { gsap, $, motionOK, isDesktop } from '../core.js';

const KEY = 'emilly:transition';
const root = document.documentElement;

function targetRect() {
  return isDesktop()
    ? { left: window.innerWidth / 2, top: 0, width: window.innerWidth / 2, height: window.innerHeight }
    : { left: 0, top: 0, width: window.innerWidth, height: Math.round(window.innerHeight * 0.58) };
}

function makeClone(src, rect) {
  const fig = document.createElement('figure');
  fig.className = 'transition-clone';
  Object.assign(fig.style, { left: `${rect.left}px`, top: `${rect.top}px`, width: `${rect.width}px`, height: `${rect.height}px` });
  const img = new Image();
  img.src = src;
  img.alt = '';
  fig.appendChild(img);
  document.body.appendChild(fig);
  return fig;
}

function isInternal(a, e) {
  if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return false;
  if (a.target && a.target !== '_self') return false;
  if (a.hasAttribute('download')) return false;
  const url = new URL(a.href, location.href);
  if (url.origin !== location.origin) return false;
  if (url.pathname === location.pathname && url.hash) return false;
  if (!/\/$|\.html$/.test(url.pathname)) return false;
  return url;
}

export function initTransitions() {
  const curtain = $('[data-curtain]');
  const panel = curtain && $('.curtain__panel', curtain);
  if (!curtain || !motionOK) {
    try { sessionStorage.removeItem(KEY); } catch (e) { /* noop */ }
    return;
  }

  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]');
    const url = isInternal(a, e);
    if (!url) return;
    e.preventDefault();
    if (root.classList.contains('is-leaving')) return;
    root.classList.add('is-leaving');
    const go = () => { window.location.href = url.href; };

    const imgEl = a.dataset.transition === 'image' && (a.querySelector('.arc__img img, .next__media img, img'));
    if (imgEl && imgEl.getBoundingClientRect().width > 0 || (a.dataset.transition === 'image' && a.dataset.transitionSrc)) {
      const src = a.dataset.transitionSrc || imgEl.currentSrc || imgEl.src;
      let from = imgEl && imgEl.getBoundingClientRect().width > 0 ? (imgEl.closest('.arc__wrap, .next__media, .stage__thumb, .folio__thumb, figure') || imgEl).getBoundingClientRect() : null;
      const sticky = a.dataset.folioItem && document.querySelector('.folio__sticky');
      if (!from && sticky && sticky.getBoundingClientRect().width > 0) from = sticky.getBoundingClientRect();
      const stageBg = a.closest('[data-stage-item]') && document.querySelector('.stage__bg.is-active');
      if (!from && stageBg && stageBg.getBoundingClientRect().width > 0) from = stageBg.getBoundingClientRect();
      const to = targetRect();
      const clone = makeClone(src, from || to);
      if (!from) gsap.set(clone, { clipPath: 'inset(0 0 100% 0)' });
      try { sessionStorage.setItem(KEY, JSON.stringify({ type: 'image', src })); } catch (err) { /* noop */ }
      gsap.set(panel, { yPercent: 100 });
      const tl = gsap.timeline({ onComplete: go });
      tl.to(panel, { yPercent: 0, duration: 0.9, ease: 'expo.inOut' }, 0)
        .to(clone, { left: to.left, top: to.top, width: to.width, height: to.height, clipPath: 'inset(0 0 0% 0)', duration: 1.05, ease: 'expo.inOut' }, 0.05);
      return;
    }
    try { sessionStorage.setItem(KEY, JSON.stringify({ type: 'curtain' })); } catch (err) { /* noop */ }
    gsap.fromTo(panel, { yPercent: 100 }, { yPercent: 0, duration: 0.8, ease: 'expo.inOut', onComplete: go });
  });

  // back/forward cache: never come back to a covered page
  window.addEventListener('pageshow', (e) => {
    if (e.persisted) {
      root.classList.remove('is-leaving', 'is-entering');
      gsap.set(panel, { yPercent: 100 });
      document.querySelectorAll('.transition-clone').forEach((n) => n.remove());
    }
  });
}

/** Called on load: reveal the page from under the curtain. Returns the entry type. */
export function enterPage() {
  let data = null;
  try { data = JSON.parse(sessionStorage.getItem(KEY) || 'null'); sessionStorage.removeItem(KEY); } catch (e) { /* noop */ }
  const curtain = $('[data-curtain]');
  if (!data || !curtain || !root.classList.contains('is-entering')) {
    root.classList.remove('is-entering');
    return Promise.resolve(null);
  }
  const panel = $('.curtain__panel', curtain);
  gsap.set(panel, { yPercent: 0 });
  const heroMedia = document.querySelector('[data-transition-target]');
  let clone = null;
  if (data.type === 'image' && heroMedia) {
    root.classList.add('from-transition');
    clone = makeClone(data.src, targetRect());
  }
  return new Promise((resolve) => {
    const tl = gsap.timeline({
      onComplete: () => {
        root.classList.remove('is-entering');
        gsap.set(panel, { yPercent: 100 });
        resolve(data.type);
      },
    });
    tl.to(panel, { yPercent: -100, duration: 0.9, ease: 'expo.inOut' }, 0.05);
    if (clone) {
      const img = heroMedia.querySelector('img');
      const loaded = !img || img.complete ? Promise.resolve() : new Promise((r) => {
        img.addEventListener('load', r, { once: true });
        img.addEventListener('error', r, { once: true });
        setTimeout(r, 2500);
      });
      const fade = () => gsap.to(clone, { autoAlpha: 0, duration: 0.4, onComplete: () => clone.remove() });
      tl.call(() => { loaded.then(fade); }, [], 0.85);
    }
  });
}
