document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.querySelector('.attention-overlay');
  const overlayContent = overlay?.querySelector('.overlay-content');
  const overlayClose = overlay?.querySelector('.overlay-close');

  const openOverlay = (html) => {
    if (!overlay || !overlayContent) return;
    overlayContent.innerHTML = html;
    overlay.removeAttribute('hidden');
    document.documentElement.classList.add('no-scroll');
  };
  const closeOverlay = () => {
    if (!overlay) return;
    overlay.setAttribute('hidden', '');
    document.documentElement.classList.remove('no-scroll');
    if (overlayContent) overlayContent.innerHTML = '';
  };

  overlayClose?.addEventListener('click', closeOverlay);
  overlay?.addEventListener('click', (e) => {
    if (e.target === overlay || e.target.classList.contains('overlay-backdrop')) closeOverlay();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeOverlay();
  });

  // Click on content card or dot to open overlay with details
  document.querySelectorAll('.attention-timeline .timeline-item').forEach(item => {
    const card = item.querySelector('.content');
    const dot = item.querySelector('.dot');
    const tpl = item.querySelector('.overlay-template');
    const makeHTML = () => tpl ? tpl.innerHTML : '<p>No details</p>';
    const open = (e) => { e?.preventDefault?.(); openOverlay(makeHTML()); };
    card?.addEventListener('click', open);
    dot?.addEventListener('click', open);
    // Keyboard support
    card?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });

    // Subtle hover highlight
    dot?.addEventListener('mouseenter', () => card?.classList.add('hover')); 
    dot?.addEventListener('mouseleave', () => card?.classList.remove('hover'));
  });

  // Intersection Observer to animate items in view
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('in-view'); });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
  document.querySelectorAll('.attention-timeline .timeline-item .content').forEach(el => io.observe(el));
});
