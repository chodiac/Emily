// Salon Emilly — entry point. Boot order: scroll engine → UI that must work immediately →
// loader / page-entry → hero intro → scroll choreography.
import { gsap, ScrollTrigger, initScroll, fontsReady, motionOK } from './core.js';
import { runLoader } from './modules/loader.js';
import { initTransitions, enterPage } from './modules/transition.js';
import { playIntro } from './modules/intro.js';
import { initNav } from './modules/nav.js';
import { initReveals, initSectionThemes } from './modules/reveal.js';
import { initArcs } from './modules/arc.js';
import { initSections } from './modules/sections.js';
import { initUI } from './modules/ui.js';

async function boot() {
  if (!gsap || !ScrollTrigger) {
    document.documentElement.classList.remove('motion', 'is-loading', 'is-entering');
    return;
  }
  window.__emilly = true;
  initScroll();
  initNav();
  initUI();
  initTransitions();

  await fontsReady();
  // pinned sections first: every trigger created afterwards measures positions including pin spacing
  initArcs();
  initSections();
  initReveals();
  initSectionThemes();

  const root = document.documentElement;
  const loaded = await runLoader();
  if (!loaded) enterPage(); // curtain lifts while the intro plays underneath
  if (motionOK) playIntro({ fromTransition: root.classList.contains('from-transition') });
  root.classList.add('is-ready');
  ScrollTrigger.refresh();
  // images decoding late can shift layout; refresh pinned sections once everything is loaded
  window.addEventListener('load', () => ScrollTrigger.refresh(), { once: true });
}

boot();
