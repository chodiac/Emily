// Scroll-driven reveals shared by every page:
// line-by-line text (masked words), char scrub, media clip reveals, growing rules (EVER
// "line-width-growing" 2s outQuart), parallax, counters, footer wordmark, section colour-scroll.
import { gsap, ScrollTrigger, $$, motionOK } from '../core.js';
import { split } from './split.js';

export function initReveals() {
  // Text: split everywhere (so layout is identical with/without motion), animate only with motion
  $$('[data-split]').forEach((el) => {
    const s = split(el);
    if (!motionOK) return;
    if (el.dataset.split === 'chars' && el.hasAttribute('data-scrub')) {
      gsap.fromTo(s.chars, { opacity: 0.12, yPercent: 18 }, {
        opacity: 1, yPercent: 0, ease: 'none', stagger: 0.06,
        scrollTrigger: { trigger: el, start: 'top 85%', end: 'bottom 45%', scrub: 0.6 },
      });
      return;
    }
    const inner = s.words.map((w) => w.firstChild);
    // headings rise out of word masks; body copy fades up line by line (no mask → no clipped descenders)
    const isBody = el.tagName === 'P' && !el.closest('.quote');
    if (isBody) el.classList.add('is-body-split');
    gsap.set(inner, isBody ? { yPercent: 55, opacity: 0 } : { yPercent: 115 });
    ScrollTrigger.create({
      trigger: el,
      start: 'top 88%',
      once: true,
      onEnter: () => {
        const lines = s.lineIndex();
        gsap.to(inner, {
          yPercent: 0,
          opacity: 1,
          duration: isBody ? 1.1 : 1.25,
          ease: 'expo.out',
          delay: (i) => lines[i] * (isBody ? 0.07 : 0.1),
        });
      },
    });
  });

  if (!motionOK) return;

  $$('[data-media-reveal]').forEach((el) => {
    const img = el.querySelector('img');
    gsap.timeline({ scrollTrigger: { trigger: el, start: 'top 85%', once: true } })
      .to(el, { clipPath: 'inset(0% 0 0 0)', duration: 1.4, ease: 'expo.inOut' })
      .to(img, { scale: 1, duration: 1.8, ease: 'expo.out' }, 0.1);
  });

  $$('[data-line]').forEach((el) => {
    gsap.to(el, { scaleX: 1, duration: 2, ease: 'power4.out', scrollTrigger: { trigger: el, start: 'top 95%', once: true } });
  });

  $$('[data-parallax]').forEach((el) => {
    const amt = parseFloat(el.dataset.parallax) || -10;
    const target = el.querySelector('img') || el;
    gsap.fromTo(target, { yPercent: -amt / 2 }, { yPercent: amt / 2, ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  $$('[data-count]').forEach((el) => {
    const end = parseInt(el.dataset.count, 10);
    const o = { v: 0 };
    el.textContent = '0';
    gsap.to(o, {
      v: end, duration: 2.2, ease: 'power3.out',
      scrollTrigger: { trigger: el, start: 'top 90%', once: true },
      onUpdate: () => { el.textContent = Math.round(o.v).toLocaleString('sr-Latn-RS'); },
    });
  });

  const word = document.querySelector('[data-footer-word]');
  if (word) {
    gsap.to(word, { yPercent: 0, opacity: 1, ease: 'none', scrollTrigger: { trigger: word, start: 'top bottom', end: 'bottom bottom', scrub: 0.5 } });
  }

  // Hero image slow drift out (EVER hero stays still; we add a gentle scale-out on scroll)
  $$('.hero, .loc-hero').forEach((hero) => {
    const img = hero.querySelector('[data-hero-media] img');
    if (!img) return;
    gsap.to(hero.querySelector('[data-hero-media]'), { yPercent: 18, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to(hero.querySelector('.hero__content, .loc-hero__content'), { yPercent: -12, opacity: 0.2, ease: 'none', scrollTrigger: { trigger: hero, start: '30% top', end: 'bottom top', scrub: true } });
  });
}

/** Nav theme follows the section under the bar (light/dark). Sections keep their own solid
 *  backgrounds: EVER's colour-scroll tween was tried and dropped because light text arriving over the
 *  previous section's colour was briefly unreadable. */
export function initSectionThemes() {
  const body = document.body;
  const sections = $$('main > [data-bg], main > nav[data-bg], footer[data-bg]');
  sections.forEach((sec) => {
    const theme = sec.dataset.bg === 'pine' ? 'dark' : 'light';
    ScrollTrigger.create({
      trigger: sec, start: 'top 40px', end: 'bottom 40px',
      onToggle: (self) => { if (self.isActive) body.dataset.navTheme = theme; },
    });
  });
  if (sections[0]) body.dataset.navTheme = sections[0].dataset.bg === 'pine' ? 'dark' : 'light';
}
