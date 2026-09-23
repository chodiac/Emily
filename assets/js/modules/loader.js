// EVER loader: mask-revealed mark, 0→100 counter + progress bar on EVER's custom curve,
// then a split exit (bar/counter drop, mark lifts, screen fades). First visit per session only.
import { gsap, $, everEase } from '../core.js';

export function runLoader() {
  const root = document.documentElement;
  const el = $('[data-loader]');
  try { sessionStorage.setItem('emilly:visited', '1'); } catch (e) { /* private mode */ }
  if (!el || !root.classList.contains('is-loading')) return Promise.resolve(false);

  return new Promise((resolve) => {
    const count = $('[data-loader-count]', el);
    const bar = $('[data-loader-bar]', el);
    const counter = { v: 0 };
    const tl = gsap.timeline({
      onComplete: () => {
        root.classList.remove('is-loading');
        el.remove();
        resolve(true);
      },
    });
    tl.to($('.loader__mask', el), { clipPath: 'inset(0% 0 0% 0)', duration: 1.1, ease: 'expo.inOut' }, 0)
      .fromTo($$('.loader__word span', el), { yPercent: 110 }, { yPercent: 0, duration: 1, ease: 'expo.out', stagger: 0.08, immediateRender: false }, 0.45)
      .to(counter, {
        v: 100, duration: 2.2, ease: everEase,
        onUpdate: () => { count.textContent = Math.round(counter.v); },
      }, 0)
      .to(bar, { width: '100%', duration: 2.2, ease: everEase }, 0)
      // exit — timings from EVER's "Hide Loader" interaction
      .to([$('.loader__bar', el), $('.loader__count', el)], { yPercent: 100, opacity: 0, duration: 0.5, ease: 'power4.in' }, 2.35)
      .to($('.loader__mark', el), { yPercent: -60, opacity: 0, duration: 0.6, ease: 'power4.in' }, 2.5)
      .to(el, { autoAlpha: 0, duration: 0.45, ease: 'power3.inOut' }, 2.85);
  });
}

function $$(s, el) { return [...el.querySelectorAll(s)]; }
