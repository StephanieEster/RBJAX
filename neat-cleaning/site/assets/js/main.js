'use strict';
(() => {
  const root = document.documentElement;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const mobileQuery = window.matchMedia('(max-width: 1020px)');

  /* Navigation */
  const nav = document.getElementById('primary-nav');
  const menuButton = document.querySelector('.menu-toggle');
  const dropdown = document.querySelector('.dd');
  const dropdownButton = document.querySelector('.dd-toggle');
  const menuIcon = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18"/></svg>';
  const closeIcon = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="m6 6 12 12M6 18 18 6"/></svg>';

  const setDropdown = (open) => {
    if (!dropdown || !dropdownButton) return;
    dropdown.classList.toggle('is-open', open);
    dropdownButton.setAttribute('aria-expanded', String(open));
  };
  const setMenu = (open, returnFocus = false) => {
    if (!nav || !menuButton) return;
    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open && mobileQuery.matches);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    menuButton.innerHTML = open ? closeIcon : menuIcon;
    if (!open) { setDropdown(false); if (returnFocus) menuButton.focus(); }
  };

  menuButton?.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
  dropdownButton?.addEventListener('click', (event) => {
    event.stopPropagation();
    setDropdown(dropdownButton.getAttribute('aria-expanded') !== 'true');
  });
  if (dropdown) {
    let hoverTimer;
    dropdown.addEventListener('mouseenter', () => { if (!mobileQuery.matches) { clearTimeout(hoverTimer); setDropdown(true); } });
    dropdown.addEventListener('mouseleave', () => { if (!mobileQuery.matches) hoverTimer = setTimeout(() => setDropdown(false), 160); });
  }
  nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenu(false)));
  document.addEventListener('click', (event) => { if (dropdown && !dropdown.contains(event.target)) setDropdown(false); });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      if (menuButton?.getAttribute('aria-expanded') === 'true') setMenu(false, true);
      else if (dropdownButton?.getAttribute('aria-expanded') === 'true') { setDropdown(false); dropdownButton.focus(); }
    }
    if (event.key === 'Tab' && mobileQuery.matches && nav?.classList.contains('is-open')) {
      const focusable = [menuButton, ...nav.querySelectorAll('a,button')].filter((el) => el && el.getClientRects().length);
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
    }
  });
  mobileQuery.addEventListener('change', () => setMenu(false));

  /* Service index: swap preview image on hover/focus */
  const preview = document.querySelector('.svc-preview');
  if (preview) {
    const images = [...preview.querySelectorAll('img')];
    const caption = preview.querySelector('figcaption');
    document.querySelectorAll('.svc-row[data-index]').forEach((row) => {
      const show = () => {
        const index = Number(row.dataset.index);
        images.forEach((img, i) => img.classList.toggle('is-active', i === index));
        if (caption) caption.textContent = row.dataset.caption || '';
      };
      row.addEventListener('mouseenter', show);
      row.addEventListener('focus', show);
    });
  }

  /* Reveal on scroll */
  const revealItems = document.querySelectorAll('.reveal');
  if (!reduceMotion && 'IntersectionObserver' in window && revealItems.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { entry.target.classList.add('is-in'); observer.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add('is-in'));
  }

  /* Mobile text bar appears after the hero */
  const bar = document.querySelector('.mobile-bar');
  const hero = document.querySelector('.hero, .center-hero');
  if (bar && hero && 'IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => bar.classList.toggle('is-visible', !entry.isIntersecting))
      .observe(hero);
  } else if (bar) {
    bar.classList.add('is-visible');
  }

  /* Quote forms */
  document.querySelectorAll('.quote-form').forEach((form) => {
    const message = form.querySelector('.form-message');
    let pending = false;
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (pending || !form.reportValidity()) return;
      const phone = form.elements.namedItem('phone');
      const digits = phone.value.replace(/\D/g, '');
      if (digits.length < 10 || digits.length > 15) {
        message.className = 'form-message error';
        message.textContent = 'Please enter a valid phone number, including the area code.';
        phone.focus();
        return;
      }
      const button = form.querySelector('button[type="submit"]');
      const originalContent = button.innerHTML;
      pending = true;
      button.disabled = true;
      button.textContent = 'Sending…';
      message.textContent = '';
      message.className = 'form-message';
      const controller = new AbortController();
      const timeout = window.setTimeout(() => controller.abort(), 30000);
      try {
        const formData = new FormData(form);
        formData.append('action', 'cw_form_submit');
        const response = await fetch('/send-form.php', {
          method: 'POST', body: formData, headers: { Accept: 'application/json' }, signal: controller.signal,
        });
        let result;
        try { result = await response.json(); }
        catch (_) { throw new Error('We could not send your request right now. Please try again or text (508) 202-8132.'); }
        if (!response.ok || !result.success) throw new Error(result.data?.message || 'Form submission failed.');
        form.reset();
        message.textContent = result.data?.message || 'Thank you! Your request has been sent successfully.';
        message.classList.add('success');
        // Redirect only after the PHP endpoint confirms mail() accepted the request.
        window.setTimeout(() => { window.location.assign('/thank-you.html'); }, 1400);
      } catch (error) {
        message.textContent = error.name === 'AbortError'
          ? 'The request took too long. It may have been sent. Please text (508) 202-8132 to confirm before trying again.'
          : error.message || 'Something went wrong. Please try again.';
        message.classList.add('error');
      } finally {
        clearTimeout(timeout);
        pending = false;
        button.disabled = false;
        button.innerHTML = originalContent;
      }
    });
  });

  root.classList.add('js-ready');
})();
