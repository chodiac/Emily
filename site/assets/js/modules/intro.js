// Page entrance choreography (EVER hero: image settles, huge serif lines rise from masks, UI fades in).
import { gsap, $, $$, motionOK, isDesktop } from '../core.js';

export function playIntro({ fromTransition = false } = {}) {
  if (!motionOK) return;
  const tl = gsap.timeline({ defaults: { ease: 'expo.out' } });
  const media = $$('[data-hero-media]');
  media.forEach((m) => {
    tl.to(m, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.6, ease: 'expo.inOut' }, 0)
      .to(m.querySelector('img'), { scale: 1, duration: 2.4 }, 0.1);
  });
  const lines = $$('[data-hero-line]');
  tl.to(lines, { yPercent: 0, y: 0, duration: 1.4, stagger: 0.09 }, media.length ? 0.55 : 0.1);
  tl.to($$('[data-hero-fade]'), { opacity: 1, y: 0, duration: 1.2, stagger: 0.08, ease: 'power3.out' }, media.length ? 0.9 : 0.35);
  const reveal = $('[data-svc-reveal]');
  if (reveal && !fromTransition) {
    // entrance lives on the inner wrapper; the outer [data-svc-media] clip is owned by the scroll scrub
    tl.fromTo(reveal, { clipPath: isDesktop() ? 'inset(0% 0% 0% 100%)' : 'inset(0% 0% 100% 0%)' },
      { clipPath: isDesktop() ? 'inset(0% 0% 0% 50%)' : 'inset(0% 0% 0% 0%)', duration: 1.5, ease: 'expo.inOut', onComplete: () => gsap.set(reveal, { clipPath: 'none' }) }, 0);
    tl.from(reveal.querySelector('img'), { scale: 1.2, duration: 2.2 }, 0.1);
  }
  const nav = $('[data-nav]');
  if (nav) tl.from(nav, { opacity: 0, duration: 1.2, ease: 'power2.out', clearProps: 'opacity' }, 0.5);
  return tl;
}
