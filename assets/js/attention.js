document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.attention-timeline .timeline-item .toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const details = btn.parentElement.querySelector('.details');
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
});

