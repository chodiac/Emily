// Lightweight text splitter (replaces SplitType). Wraps words (and optionally chars) of text nodes
// while preserving inline markup such as <em> and <a>. Lines are derived from word offsets so the
// reveal can stagger line by line, like EVER's line reveals.

function wrapTextNodes(el, mode) {
  const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  const words = [];
  nodes.forEach((node) => {
    const parts = node.textContent.split(/(\s+)/);
    const frag = document.createDocumentFragment();
    parts.forEach((part) => {
      if (!part) return;
      if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
      const mask = document.createElement('span');
      mask.className = 'split-word';
      const inner = document.createElement('span');
      inner.className = 'split-word__in';
      if (mode === 'chars') {
        [...part].forEach((ch) => {
          const c = document.createElement('span');
          c.className = 'split-char';
          c.textContent = ch;
          inner.appendChild(c);
        });
      } else {
        inner.textContent = part;
      }
      mask.appendChild(inner);
      frag.appendChild(mask);
      words.push(mask);
    });
    node.parentNode.replaceChild(frag, node);
  });
  return words;
}

export function split(el) {
  if (el.classList.contains('is-split')) return el._split;
  const mode = el.dataset.split || 'lines';
  if (mode === 'chars' && !el.querySelector('a')) {
    // per-letter spans can be read letter by letter by some screen readers: expose the text once
    const label = document.createElement('span');
    label.className = 'visually-hidden';
    label.textContent = el.textContent.replace(/\s+/g, ' ').trim();
    const words = wrapTextNodes(el, mode);
    [...el.childNodes].forEach((c) => c.nodeType === 1 && c.setAttribute('aria-hidden', 'true'));
    el.prepend(label);
    el.classList.add('is-split');
    const res = { words, chars: [...el.querySelectorAll('.split-char')], lineIndex: () => lineIndex(words) };
    el._split = res;
    return res;
  }
  const words = wrapTextNodes(el, mode);
  el.classList.add('is-split');
  const res = { words, chars: [...el.querySelectorAll('.split-char')], lineIndex: () => lineIndex(words) };
  el._split = res;
  return res;
}

export function lineIndex(words) {
  let top = null;
  let line = -1;
  return words.map((w) => {
    const t = Math.round(w.offsetTop);
    if (top === null || Math.abs(t - top) > 4) { line += 1; top = t; }
    return line;
  });
}
