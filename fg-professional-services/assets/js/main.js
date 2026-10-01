(() => {
  const toggle = document.querySelector('[data-menu-toggle]');
  const menu = document.querySelector('[data-menu]');
  let lastFocus = null;
  function setMenu(open) {
    if (!toggle || !menu) return;
    menu.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.classList.toggle('nav-open', open);
    if (open) { lastFocus = document.activeElement; menu.querySelector('a')?.focus(); }
    else if (document.activeElement && menu.contains(document.activeElement)) toggle.focus();
  }
  toggle?.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  menu?.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') { setMenu(false); dialog?.close(); }
    if (event.key === 'Tab' && menu?.classList.contains('open')) {
      const focusable = [toggle, ...menu.querySelectorAll('a')];
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  });
  window.addEventListener('resize', () => { if (innerWidth > 820 && menu?.classList.contains('open')) setMenu(false); });
  const dialog = document.querySelector('[data-estimate-dialog]');
  const close = document.querySelector('[data-dialog-close]');
  close?.addEventListener('click', () => dialog.close());
  dialog?.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog?.addEventListener('close', () => document.body.classList.remove('modal-open'));
  // A single unobtrusive invitation per session, after meaningful page engagement.
  let engaged = false;
  function offerEstimate() {
    if (!engaged || !dialog || dialog.open || sessionStorage.getItem('fg-estimate-seen')) return;
    sessionStorage.setItem('fg-estimate-seen', '1');
    dialog.showModal();
    document.body.classList.add('modal-open');
  }
  window.addEventListener('scroll', () => {
    const scrollable = document.documentElement.scrollHeight - innerHeight;
    if (scrollable > 0 && scrollY / scrollable > .42) { engaged = true; offerEstimate(); }
  }, { passive: true });
  setTimeout(() => { if (scrollY > 250) { engaged = true; offerEstimate(); } }, 25000);
})();

// Reveal sections as they enter the viewport. Reduced-motion visitors see all content.
(() => {
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const elements = document.querySelectorAll('.section-head, .intro-copy, .intro-image, .service-card, .feature-content, .feature-visual, .process-step, .detail-section, .area-panel, .service-note-inner');
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  }, { threshold: .08, rootMargin: '0px 0px 45px 0px' });
  elements.forEach(element => { element.classList.add('reveal'); observer.observe(element); });
})();

// All three inquiry forms use the site's own PHP endpoint.
(() => {
  document.querySelectorAll('.fg-form').forEach(form => {
    const status = form.querySelector('.fg-form-message');
    const button = form.querySelector('button[type="submit"]');
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const original = button.innerHTML;
      button.disabled = true;
      button.textContent = 'Sending...';
      status.textContent = '';
      status.className = 'fg-form-message';
      try {
        const payload = new FormData(form);
        payload.append('action', 'cw_form_submit');
        const response = await fetch('/send-form.php', {
          method: 'POST', body: payload, headers: { Accept: 'application/json' }
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
          throw new Error(result.data?.message || 'Form submission failed.');
        }
        form.reset();
        status.textContent = result.data?.message || 'Thank you! Your request has been sent successfully.';
        status.classList.add('is-success');
      } catch (error) {
        status.textContent = 'Something went wrong. Please try again or contact us by phone.';
        status.classList.add('is-error');
      } finally {
        button.disabled = false;
        button.innerHTML = original;
      }
    });
  });
})();
