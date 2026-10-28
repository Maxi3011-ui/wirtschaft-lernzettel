(() => {
  'use strict';
  const select = document.getElementById('chapter-select');
  const nav = document.querySelector('.jump-nav');
  const chapters = Array.from(document.querySelectorAll('.chapter'));
  if (!select || !nav || !chapters.length) return;
  const updateHeight = () => document.documentElement.style.setProperty('--nav-height', `${Math.ceil(nav.getBoundingClientRect().height)}px`);
  updateHeight();
  if ('ResizeObserver' in window) new ResizeObserver(updateHeight).observe(nav);
  else window.addEventListener('resize', updateHeight);
  const jump = (id, focus = false) => {
    const target = document.getElementById(id);
    if (!target) return;
    const chapter = target.closest('.chapter');
    if (chapter) select.value = chapter.id;
    if (focus && target.classList.contains('chapter')) target.focus({ preventScroll: true });
    target.scrollIntoView({ block: 'start', behavior: 'auto' });
  };
  select.addEventListener('change', () => {
    const id = select.value;
    if (location.hash !== `#${id}`) history.pushState(null, '', `#${id}`);
    jump(id, true);
  });
  let scheduled = false;
  const sync = () => {
    const threshold = nav.getBoundingClientRect().bottom + 15;
    let current = chapters[0];
    for (const chapter of chapters) {
      if (chapter.getBoundingClientRect().top <= threshold) current = chapter;
      else break;
    }
    if (window.scrollY > 0 && window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 3) current = chapters[chapters.length - 1];
    select.value = current.id;
    scheduled = false;
  };
  window.addEventListener('scroll', () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(sync); }
  }, { passive: true });
  window.addEventListener('hashchange', () => jump(decodeURIComponent(location.hash.slice(1))));
  window.addEventListener('popstate', () => jump(decodeURIComponent(location.hash.slice(1)) || chapters[0].id));
  if (location.hash) requestAnimationFrame(() => jump(decodeURIComponent(location.hash.slice(1))));
  const sources = document.getElementById('sources');
  let sourcesOpen = false;
  window.addEventListener('beforeprint', () => { sourcesOpen = sources.open; sources.open = true; });
  window.addEventListener('afterprint', () => { sources.open = sourcesOpen; });
})();
