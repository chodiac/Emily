// Navigation (EVER navbar19): transparent bar that hides on scroll-down and returns on scroll-up;
// full-screen menu with burger→cross morph, numbered services, sibling dimming, image on hover.
import { gsap, $, $$, motionOK, stopScroll, startScroll, lenis } from '../core.js';

export function initNav() {
  const nav = $('[data-nav]');
  const toggle = $('[data-menu-toggle]');
  const menu = $('[data-menu]');
  const label = $('[data-menu-label]');
  const media = $('.menu__media', menu);
  const root = document.documentElement;
  if (!nav || !toggle || !menu) return;
  let open = false;
  let lastFocus = null;

  const focusables = () => $$('a[href], button:not([disabled])', menu).concat(toggle).filter((el) => el.offsetParent !== null);

  function openMenu() {
    open = true;
    lastFocus = document.activeElement;
    menu.hidden = false;
    root.classList.add('menu-open');
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Zatvori meni');
    if (label) label.textContent = 'Zatvori';
    stopScroll();
    if (motionOK) {
      gsap.killTweensOf([menu, ...$$('.menu__svc, .menu__giant, .menu__social li, .menu__pages li, .menu__booking', menu)]);
      gsap.timeline()
        .fromTo(menu, { clipPath: 'inset(0% 0% 100% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 0.9, ease: 'expo.inOut' })
        .fromTo('.menu__giant', { yPercent: 100, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 1.1, ease: 'expo.out' }, 0.45)
        .fromTo($$('.menu__svc', menu), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.9, ease: 'expo.out', stagger: 0.04 }, 0.45)
        .fromTo($$('.menu__social li, .menu__pages li, .menu__booking', menu), { y: 16, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', stagger: 0.03 }, 0.6);
    } else {
      menu.style.clipPath = 'none';
    }
    setTimeout(() => { const f = $('.menu__svc', menu); f && f.focus({ preventScroll: true }); }, motionOK ? 500 : 0);
  }

  function closeMenu(returnFocus = true) {
    if (!open) return;
    open = false;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Otvori meni');
    if (label) label.textContent = 'Meni';
    root.classList.remove('menu-open');
    const done = () => { menu.hidden = true; startScroll(); };
    if (motionOK) gsap.to(menu, { clipPath: 'inset(0% 0% 100% 0%)', duration: 0.7, ease: 'expo.inOut', onComplete: done });
    else done();
    if (returnFocus) toggle.focus({ preventScroll: true });
  }

  toggle.setAttribute('aria-label', 'Otvori meni');
  toggle.addEventListener('click', () => (open ? closeMenu() : openMenu()));
  document.addEventListener('keydown', (e) => {
    if (!open) return;
    if (e.key === 'Escape') { e.preventDefault(); closeMenu(); }
    if (e.key === 'Tab') {
      const f = focusables();
      const first = f[0];
      const last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  // same-page links inside the menu just close it
  menu.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]');
    if (!a) return;
    const url = new URL(a.href, location.href);
    if (url.pathname === location.pathname) closeMenu(false);
  });

  // service image in the menu background on hover (desktop)
  $$('.menu__svc', menu).forEach((a) => {
    const src = a.dataset.img;
    if (!src || !media) return;
    a.addEventListener('mouseenter', () => { media.style.backgroundImage = `url("${src}")`; media.classList.add('is-on'); });
    a.addEventListener('mouseleave', () => media.classList.remove('is-on'));
  });

  // hide on scroll down / show on scroll up
  let lastY = window.scrollY;
  const onScroll = (y) => {
    nav.classList.toggle('is-scrolled', y > 40);
    if (!open) nav.classList.toggle('is-hidden', y > 160 && y > lastY + 2);
    if (y < lastY - 2) nav.classList.remove('is-hidden');
    lastY = y;
  };
  if (lenis) lenis.on('scroll', ({ scroll }) => onScroll(scroll));
  else window.addEventListener('scroll', () => onScroll(window.scrollY), { passive: true });
  nav.addEventListener('focusin', () => nav.classList.remove('is-hidden'));
}
