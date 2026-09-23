// Pinned / scroll-linked set pieces adapted from EVER's IX2 interactions.
// Desktop gets the pinned choreography; small screens get lighter, unpinned versions.
import { gsap, ScrollTrigger, $, $$, motionOK, mqDesktop, finePointer } from '../core.js';

/** Sticky "pin": the section gets extra scroll length, its [data-pin] child sticks for the duration. */
function stickyPin(sec, lenVh, undo) {
  sec.classList.add('is-sticky');
  sec.style.height = `calc(100vh + ${lenVh}vh)`;
  undo.push(() => { sec.classList.remove('is-sticky'); sec.style.height = ''; });
  return { trigger: sec, start: 'top top', end: 'bottom bottom' };
}

export function initSections() {
  initStage();
  initFolio();
  initPricebookNav();
  if (!motionOK) return;
  const mm = gsap.matchMedia();

  mm.add(mqDesktop, () => {
    const undo = [];
    floatingImages();
    wheel(undo);
    stack(undo);
    expandCTA(true, undo);
    mission(undo);
    svcHero();
    return () => undo.forEach((fn) => fn());
  });
  mm.add('(max-width: 900px)', () => {
    expandCTA(false);
    $$('[data-float-fig]').forEach((f) => gsap.from(f, { yPercent: 12, opacity: 0, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: f, start: 'top 90%', once: true } }));
  });

  // About: image "shrinks into place" — EVER Layout 413 (width 200% → 100%, 1400ms outQuart)
  $$('[data-shrink]').forEach((frame) => {
    const img = frame.querySelector('img');
    gsap.fromTo(img, { scale: 1.9 }, { scale: 1, duration: 1.6, ease: 'power4.out', scrollTrigger: { trigger: frame, start: 'top 80%', once: true } });
    gsap.fromTo(frame, { clipPath: 'inset(0% 12% 0% 12%)' }, { clipPath: 'inset(0% 0% 0% 0%)', ease: 'none', scrollTrigger: { trigger: frame, start: 'top 90%', end: 'center 55%', scrub: true } });
  });
}

/* EVER Header 80: sticky heading, two image columns rising at different speeds, images brighten as they rise */
function floatingImages() {
  $$('[data-float]').forEach((sec) => {
    $$('[data-float-col]', sec).forEach((col) => {
      const amt = parseFloat(col.dataset.floatCol) || -60;
      gsap.fromTo(col, { y: 0 }, { y: () => (amt / 100) * window.innerHeight * 0.9, ease: 'none', scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: true, invalidateOnRefresh: true } });
    });
    $$('[data-float-fig]', sec).forEach((fig) => {
      gsap.fromTo(fig, { opacity: 0.25, scale: 0.94 }, { opacity: 1, scale: 1, ease: 'none', scrollTrigger: { trigger: fig, start: 'top bottom', end: 'top 35%', scrub: true } });
    });
    const content = $('.float__content', sec);
    gsap.fromTo(content, { opacity: 0.001, y: 40 }, { opacity: 1, y: 0, ease: 'none', scrollTrigger: { trigger: sec, start: 'top 70%', end: 'top 10%', scrub: true } });
    gsap.to(content, { opacity: 0, y: -40, ease: 'none', immediateRender: false, scrollTrigger: { trigger: sec, start: 'bottom 90%', end: 'bottom 45%', scrub: true } });
  });
}

/* EVER Layout 468: numbered services over one full-bleed image; hover/focus swaps image + card */
function initStage() {
  $$('[data-stage]').forEach((stage) => {
    const items = $$('[data-stage-item]', stage);
    const bgs = $$('[data-stage-bg]', stage);
    const set = (i) => {
      items.forEach((it, k) => it.classList.toggle('is-active', k === i));
      bgs.forEach((bg, k) => bg.classList.toggle('is-active', k === i));
    };
    items.forEach((it, i) => {
      const a = it.querySelector('a');
      if (finePointer()) a.addEventListener('mouseenter', () => set(i));
      a.addEventListener('focus', () => set(i));
    });
  });
}

/* EVER Portfolio 22 (services page): sticky image swaps with the hovered row */
function initFolio() {
  const imgs = $$('[data-folio-img]');
  if (!imgs.length) return;
  const set = (slug) => imgs.forEach((im) => im.classList.toggle('is-active', im.dataset.folioImg === slug));
  $$('[data-folio-item]').forEach((a) => {
    a.addEventListener('mouseenter', () => set(a.dataset.folioItem));
    a.addEventListener('focus', () => set(a.dataset.folioItem));
  });
}

function initPricebookNav() {
  const chips = $$('.pricebook__nav .chip');
  if (!chips.length) return;
  chips.forEach((chip) => {
    const block = document.querySelector(chip.getAttribute('href'));
    if (!block) return;
    ScrollTrigger.create({
      trigger: block, start: 'top 45%', end: 'bottom 45%',
      onToggle: (self) => {
        if (!self.isActive) return;
        chips.forEach((c) => c.classList.toggle('is-active', c === chip));
        const bar = chip.closest('ul');
        bar.scrollTo({ left: chip.offsetLeft - bar.clientWidth / 2 + chip.clientWidth / 2, behavior: 'smooth' });
      },
    });
  });
}

/* EVER "EVERLASH" text wheel: scroll-linked vertical list, active 1 / neighbours .5 / others ~0 */
function wheel(undo) {
  $$('[data-wheel]').forEach((sec) => {
    const track = $('[data-wheel-track]', sec);
    const items = $$('[data-wheel-item]', sec);
    if (!track || items.length < 2) return;
    sec.classList.add('is-pinned');
    const step = () => items[0].getBoundingClientRect().height;
    const apply = (p) => {
      const f = p * (items.length - 1);
      gsap.set(track, { y: -f * step() });
      items.forEach((it, i) => {
        const d = Math.abs(i - f);
        it.style.opacity = Math.max(0.06, 1 - d * 0.55).toFixed(3);
        it.style.transform = `translateX(${Math.min(d, 1.5) * 14}px)`;
      });
    };
    apply(0);
    ScrollTrigger.create({ ...stickyPin(sec, items.length * 38, undo), scrub: 0.6, onUpdate: (self) => apply(self.progress) });
    undo.push(() => { sec.classList.remove('is-pinned'); gsap.set(track, { clearProps: 'all' }); items.forEach((it) => { it.style.opacity = ''; it.style.transform = ''; }); });
  });
}

/* EVER header115 centre images: photos slide in (x +10%) and stack one after another on scroll */
function stack(undo) {
  $$('[data-stack]').forEach((sec) => {
    const figs = $$('[data-stack-fig]', sec);
    const count = $('[data-stack-count]', sec);
    if (figs.length < 2) return;
    sec.classList.add('is-pinned');
    figs.forEach((f, i) => gsap.set(f, { xPercent: -50, yPercent: -50, x: (i - (figs.length - 1) / 2) * 26, rotation: (i - (figs.length - 1) / 2) * 1.8 }));
    const tl = gsap.timeline({
      scrollTrigger: {
        ...stickyPin(sec, figs.length * 45, undo), scrub: 0.6,
        onUpdate: (self) => { if (count) count.textContent = String(Math.min(figs.length, 1 + Math.floor(self.progress * figs.length * 0.999))).padStart(2, '0'); },
      },
    });
    figs.slice(1).forEach((f, i) => {
      tl.fromTo(f, { xPercent: -50 + 60, opacity: 0, rotation: 8 }, { xPercent: -50, opacity: 1, rotation: (i + 1 - (figs.length - 1) / 2) * 1.8, duration: 1, ease: 'power2.out' }, i);
      tl.to(figs.slice(0, i + 1), { scale: '-=0.03', filter: 'brightness(0.85)', duration: 1, ease: 'none' }, i);
    });
    undo.push(() => { sec.classList.remove('is-pinned'); gsap.set(figs, { clearProps: 'all' }); });
  });
}

/* EVER Layout 517: image grows from a 20%×40% frame to full viewport; content rises + scales in */
function expandCTA(desktop, undo) {
  $$('[data-expand]').forEach((sec) => {
    const frame = $('[data-expand-frame]', sec);
    const content = $('[data-expand-content]', sec);
    const img = frame.querySelector('img');
    if (desktop) {
      const tl = gsap.timeline({ scrollTrigger: { ...stickyPin(sec, 120, undo), scrub: 0.8 } });
      tl.fromTo(frame, { clipPath: 'inset(30% 40% 30% 40% round 2px)' }, { clipPath: 'inset(0% 0% 0% 0% round 0px)', duration: 1, ease: 'power2.inOut' }, 0)
        .fromTo(img, { scale: 1.12 }, { scale: 1, duration: 1, ease: 'power2.inOut' }, 0)
        .fromTo(content, { yPercent: 40, scale: 0.8, opacity: 0 }, { yPercent: 0, scale: 1, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.35);
    } else {
      gsap.fromTo(frame, { clipPath: 'inset(12% 8% 12% 8%)' }, { clipPath: 'inset(0% 0% 0% 0%)', ease: 'none', scrollTrigger: { trigger: sec, start: 'top 85%', end: 'top 15%', scrub: true } });
      gsap.from(content, { y: 40, opacity: 0, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: sec, start: 'top 55%', once: true } });
    }
  });
}

/* EVER Header 75/82: pinned headline scales to .95 and fades while the media frame grows to 100vh */
function mission(undo) {
  $$('[data-mission]').forEach((sec) => {
    const content = $('[data-mission-content]', sec);
    const frame = $('[data-mission-frame]', sec);
    sec.classList.add('is-pinned');
    gsap.set(frame, { xPercent: -50, yPercent: -50, y: () => window.innerHeight * 0.75 });
    const tl = gsap.timeline({ scrollTrigger: { ...stickyPin(sec, 160, undo), scrub: 0.8, invalidateOnRefresh: true } });
    tl.to(frame, { y: 0, duration: 0.45, ease: 'none' }, 0)
      .to(content, { scale: 0.95, opacity: 0, duration: 0.2, ease: 'none' }, 0.25)
      .to(frame, { width: '100%', height: '100vh', borderRadius: 0, duration: 0.4, ease: 'power1.inOut' }, 0.45)
      .fromTo(frame.querySelector('img'), { scale: 1.15 }, { scale: 1, duration: 0.85, ease: 'none' }, 0);
    undo.push(() => { sec.classList.remove('is-pinned'); gsap.set([frame, content], { clearProps: 'all' }); });
  });
}

/* EVER Header 81: service hero — image widens from 50% to full width while the text recedes */
function svcHero() {
  const sec = $('[data-svc-hero]');
  if (!sec) return;
  const media = $('[data-svc-media]', sec);
  const content = $('[data-svc-content]', sec);
  const tl = gsap.timeline({ scrollTrigger: { trigger: sec, start: 'top top', end: 'bottom bottom', scrub: 0.6 } });
  tl.fromTo(media, { clipPath: 'inset(0% 0% 0% 50%)' }, { clipPath: 'inset(0% 0% 0% 0%)', ease: 'power1.inOut', duration: 0.6, immediateRender: false }, 0)
    .to(content, { xPercent: -8, opacity: 0, ease: 'none', duration: 0.45 }, 0.05)
    .to({}, { duration: 0.4 });
}
