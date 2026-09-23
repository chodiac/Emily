// Shared runtime: environment flags, Lenis smooth scroll wired into GSAP's ticker, small helpers.
export const gsap = window.gsap;
export const ScrollTrigger = window.ScrollTrigger;

const root = document.documentElement;
export const motionOK = root.classList.contains('motion');
export const mqDesktop = '(min-width: 901px)';
export const isDesktop = () => window.matchMedia(mqDesktop).matches;
export const finePointer = () => window.matchMedia('(hover: hover) and (pointer: fine)').matches;

export const $ = (s, el = document) => el.querySelector(s);
export const $$ = (s, el = document) => [...el.querySelectorAll(s)];

export let lenis = null;

export function initScroll() {
  gsap.registerPlugin(ScrollTrigger);
  if (motionOK && window.Lenis && !root.classList.contains('raw-scroll')) {
    // EVER: Lenis duration 1.5 with expo-out easing, native scrolling on touch devices
    lenis = new window.Lenis({
      duration: 1.35,
      easing: (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t)),
      smoothWheel: true,
      syncTouch: false,
    });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  // in-page anchors through Lenis (respecting the fixed nav)
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute('href');
    if (id === '#' || id === '#main') return;
    const target = id === '#top' ? 0 : document.querySelector(id);
    if (target === null) return;
    e.preventDefault();
    scrollTo(target, { offset: id === '#top' ? 0 : -80 });
    if (target && target.focus) {
      target.setAttribute('tabindex', '-1');
      target.focus({ preventScroll: true });
    }
  });
}

export function scrollTo(target, opts = {}) {
  if (lenis) lenis.scrollTo(target, { offset: opts.offset || 0, duration: opts.immediate ? 0 : 1.4, immediate: !!opts.immediate });
  else {
    const y = typeof target === 'number' ? target : target.getBoundingClientRect().top + window.scrollY + (opts.offset || 0);
    window.scrollTo({ top: y, behavior: motionOK && !opts.immediate ? 'smooth' : 'auto' });
  }
}

export function stopScroll() { lenis ? lenis.stop() : (document.body.style.overflow = 'hidden'); }
export function startScroll() { lenis ? lenis.start() : (document.body.style.overflow = ''); }

/** Wait for web fonts (so line measurements are right), but never longer than `max` ms. */
export function fontsReady(max = 1500) {
  return Promise.race([document.fonts ? document.fonts.ready : Promise.resolve(), new Promise((r) => setTimeout(r, max))]);
}

/**
 * EVER's loader curve (CustomEase path from their site) approximated through its knots,
 * with smoothstep inside each segment — gives the same "breathing", stepped progress.
 */
const KNOTS = [[0, 0], [0.238, 0.442], [0.396, 0.54], [0.522, 0.584], [0.714, 0.826], [1, 1]];
export function everEase(t) {
  for (let i = 1; i < KNOTS.length; i++) {
    const [x1, y1] = KNOTS[i];
    const [x0, y0] = KNOTS[i - 1];
    if (t <= x1) {
      const u = (t - x0) / (x1 - x0);
      const s = u * u * (3 - 2 * u);
      return y0 + (y1 - y0) * s;
    }
  }
  return 1;
}
