document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.attention-timeline .timeline-item .toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.timeline-item');
      const details = item ? item.querySelector('.details') : null;
      if (!details) return;
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      if (expanded) {
        details.setAttribute('hidden', '');
        btn.setAttribute('aria-expanded', 'false');
        btn.textContent = 'Details';
      } else {
        details.removeAttribute('hidden');
        btn.setAttribute('aria-expanded', 'true');
        btn.textContent = 'Hide';
      }
    });
  });

  // Hover summary tooltip-like behavior on dots
  document.querySelectorAll('.attention-timeline .timeline-item .dot').forEach(dot => {
    const content = dot.closest('.timeline-item').querySelector('.summary');
    dot.addEventListener('mouseenter', () => {
      content.classList.add('highlight');
    });
    dot.addEventListener('mouseleave', () => {
      content.classList.remove('highlight');
    });
  });

  // Checklist popover: open on click, keep open on hover, close on outside click
  document.querySelectorAll('.attention-timeline .timeline-item').forEach(item => {
    const trigger = item.querySelector('.checklist-trigger');
    const pop = item.querySelector('.checklist-popover');
    if (!trigger || !pop) return;

    let hideTimer = null;
    const open = () => {
      const rect = trigger.getBoundingClientRect();
      // Position popover relative to trigger
      pop.style.top = (trigger.offsetTop + trigger.offsetHeight + 8) + 'px';
      pop.style.left = (trigger.offsetLeft) + 'px';
      pop.removeAttribute('hidden');
      trigger.setAttribute('aria-expanded', 'true');
    };
    const close = () => {
      pop.setAttribute('hidden', '');
      trigger.setAttribute('aria-expanded', 'false');
    };

    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      if (pop.hasAttribute('hidden')) open(); else close();
    });
    trigger.addEventListener('mouseenter', open);
    trigger.addEventListener('mouseleave', () => {
      hideTimer = setTimeout(close, 200);
    });
    pop.addEventListener('mouseenter', () => {
      if (hideTimer) { clearTimeout(hideTimer); hideTimer = null; }
    });
    pop.addEventListener('mouseleave', () => {
      hideTimer = setTimeout(close, 200);
    });
    document.addEventListener('click', (e) => {
      if (!item.contains(e.target)) close();
    });
  });
});
