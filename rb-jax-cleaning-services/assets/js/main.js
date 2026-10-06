(function () {
  'use strict';

  const toggle = document.querySelector('[data-nav-toggle]');
  const menu = document.querySelector('[data-nav-menu]');

  function closeMenu() {
    if (!toggle || !menu) return;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    menu.classList.remove('is-open');
    document.body.classList.remove('menu-open');
  }

  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
      menu.classList.toggle('is-open', !open);
      document.body.classList.toggle('menu-open', !open);
    });
    menu.querySelectorAll('a').forEach(function (link) { link.addEventListener('click', closeMenu); });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 820) closeMenu();
    });
  }

  const currentFile = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('[data-nav-menu] a[data-page]').forEach(function (link) {
    const page = link.getAttribute('data-page');
    const servicePages = ['services.html', 'residential-cleaning.html', 'commercial-cleaning.html', 'deep-cleaning.html'];
    if (page === currentFile || (page === 'services.html' && servicePages.includes(currentFile))) link.setAttribute('aria-current', 'page');
  });

  document.querySelectorAll('[data-year]').forEach(function (item) { item.textContent = new Date().getFullYear(); });

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    document.querySelectorAll('[data-reveal]').forEach(function (item) { observer.observe(item); });
  } else {
    document.querySelectorAll('[data-reveal]').forEach(function (item) { item.classList.add('is-visible'); });
  }

  function bindForm(form) {
    if (!form || form.dataset.bound === 'true') return;
    form.dataset.bound = 'true';
    const message = form.querySelector('.form-message');
    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      const button = form.querySelector('button[type="submit"]');
      const originalText = button.textContent;
      button.disabled = true;
      button.textContent = 'Sending...';
      message.textContent = '';
      message.className = 'form-message';
      try {
        const formData = new FormData(form);
        formData.append('action', 'cw_form_submit');
        const response = await fetch('/send-form.php', { method: 'POST', body: formData, headers: { Accept: 'application/json' } });
        const result = await response.json();
        if (!response.ok || !result.success) throw new Error(result.data && result.data.message ? result.data.message : 'Form submission failed.');
        form.reset();
        message.textContent = result.data && result.data.message ? result.data.message : 'Thank you! Your request has been sent successfully.';
        message.classList.add('success');
      } catch (error) {
        message.textContent = error.message || 'Something went wrong. Please try again.';
        message.classList.add('error');
      } finally {
        button.disabled = false;
        button.textContent = originalText;
      }
    });
  }

  document.querySelectorAll('.js-contact-form').forEach(bindForm);

  function createEstimatePopup() {
    if (document.querySelector('[data-estimate-popup]')) return;
    const popup = document.createElement('div');
    popup.className = 'estimate-popup';
    popup.setAttribute('data-estimate-popup', '');
    popup.setAttribute('aria-hidden', 'true');
    popup.innerHTML = `
      <div class="estimate-popup-backdrop" data-popup-close></div>
      <section class="estimate-popup-panel" role="dialog" aria-modal="true" aria-labelledby="estimatePopupTitle">
        <button class="popup-close" type="button" aria-label="Close estimate form" data-popup-close><svg class="icon" aria-hidden="true"><use href="assets/icons.svg#close"></use></svg></button>
        <div class="popup-visual">
          <img src="assets/images/gallery-bright-kitchen.webp" alt="Bright kitchen after professional cleaning">
          <div><span>Personal service</span><strong>Where clean feels like home.</strong></div>
        </div>
        <div class="popup-content">
          <span class="eyebrow">In-person estimate</span>
          <h2 id="estimatePopupTitle">Let’s see what your space needs.</h2>
          <p>Send your details and we will text you your cleaning quote.</p>
          <form class="popup-form js-contact-form" id="popupEstimateForm">
            <input type="hidden" name="_to" value="rbcleaningfl@gmail.com">
            <input type="hidden" name="subject" value="New cleaning estimate request">
            <input type="hidden" name="from_name" value="RB Jax Cleaning Services Website">
            <input type="hidden" name="form_context" value="Scroll popup estimate form">
            <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" style="display:none">
            <div class="field"><label for="popupName">Full name</label><input id="popupName" name="name" type="text" autocomplete="name" required></div>
            <div class="field"><label for="popupPhone">Phone number</label><input id="popupPhone" name="phone" type="tel" autocomplete="tel" required></div>
            <div class="field field-full"><label for="popupEmail">Email address</label><input id="popupEmail" name="email" type="email" autocomplete="email" required></div>
            <div class="field field-full"><label for="popupService">Service needed</label><select id="popupService" name="service" required><option value="">Select a service</option><option>Regular cleaning</option><option>Deep cleaning</option><option>Commercial cleaning</option><option>Recurring cleaning</option><option>Exterior window cleaning</option><option>Not sure yet</option></select></div>
            <input type="hidden" name="preferred_contact" value="Text message">
            <label class="consent" for="popupConsentCare"><input id="popupConsentCare" type="checkbox" name="consent_care" value="agreed"><span>I agree to receive customer care text messages from RB Jax Cleaning Services LLC about my quote, appointments and reminders at the phone number provided. Message frequency varies. Message and data rates may apply. Reply STOP to opt out or HELP for help. Consent is not a condition of purchase. See our <a href="terms.html">Terms</a> and <a href="privacy.html">Privacy Policy</a>.</span></label>
            <label class="consent" for="popupConsentMarketing"><input id="popupConsentMarketing" type="checkbox" name="consent_marketing" value="agreed"><span>I agree to receive marketing text messages from RB Jax Cleaning Services LLC, including offers and seasonal reminders, at the phone number provided. Message frequency varies. Message and data rates may apply. Reply STOP to opt out or HELP for help. Consent is not a condition of purchase. See our <a href="terms.html">Terms</a> and <a href="privacy.html">Privacy Policy</a>.</span></label>
            <div class="form-actions"><button class="button" type="submit">Request my estimate</button><p class="form-message" aria-live="polite"></p><p class="form-legal"><a href="privacy.html">Privacy Policy</a> · <a href="terms.html">Terms of Service</a></p></div>
          </form>
        </div>
      </section>`;
    document.body.appendChild(popup);
    bindForm(popup.querySelector('form'));

    const trigger = document.createElement('button');
    trigger.className = 'estimate-trigger';
    trigger.type = 'button';
    trigger.innerHTML = '<svg class="icon" aria-hidden="true"><use href="assets/icons.svg#sparkle"></use></svg><span>Free estimate</span>';
    trigger.setAttribute('aria-label', 'Open estimate form');
    document.body.appendChild(trigger);

    let lastFocus = null;
    function openPopup() {
      lastFocus = document.activeElement;
      popup.classList.add('is-open');
      popup.setAttribute('aria-hidden', 'false');
      document.body.classList.add('popup-open');
      sessionStorage.setItem('rbjaxEstimatePopupSeen', '1');
      window.setTimeout(function () { popup.querySelector('.popup-close').focus(); }, 100);
    }
    function closePopup() {
      popup.classList.remove('is-open');
      popup.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('popup-open');
      if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
    }
    popup.querySelectorAll('[data-popup-close]').forEach(function (item) { item.addEventListener('click', closePopup); });
    trigger.addEventListener('click', openPopup);
    document.addEventListener('keydown', function (event) { if (event.key === 'Escape' && popup.classList.contains('is-open')) closePopup(); });

    if (!sessionStorage.getItem('rbjaxEstimatePopupSeen')) {
      let opened = false;
      function checkScroll() {
        const scrollable = document.documentElement.scrollHeight - window.innerHeight;
        const progress = scrollable > 0 ? window.scrollY / scrollable : 0;
        if (!opened && progress >= 0.28) {
          opened = true;
          window.removeEventListener('scroll', checkScroll);
          openPopup();
        }
      }
      window.addEventListener('scroll', checkScroll, { passive: true });
    }
  }

  createEstimatePopup();

  const lightbox = document.querySelector('[data-lightbox]');
  if (lightbox) {
    const lightboxImage = lightbox.querySelector('img');
    const lightboxCaption = lightbox.querySelector('[data-lightbox-caption]');
    function closeLightbox() {
      lightbox.classList.remove('is-open');
      lightbox.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('popup-open');
    }
    document.querySelectorAll('[data-gallery-item]').forEach(function (item) {
      item.addEventListener('click', function () {
        const image = item.querySelector('img');
        lightboxImage.src = image.src;
        lightboxImage.alt = image.alt;
        lightboxCaption.textContent = image.alt;
        lightbox.classList.add('is-open');
        lightbox.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        lightbox.querySelector('button').focus();
      });
    });
    lightbox.querySelectorAll('[data-lightbox-close]').forEach(function (item) { item.addEventListener('click', closeLightbox); });
    document.addEventListener('keydown', function (event) { if (event.key === 'Escape' && lightbox.classList.contains('is-open')) closeLightbox(); });
  }

  document.addEventListener('keydown', function (event) { if (event.key === 'Escape') closeMenu(); });
})();
