/* R.A Tile Renovation — site scripts (no dependencies) */
(function () {
  'use strict';

  var doc = document.documentElement;
  var DESKTOP = 1000;

  /* ------------------------------------------------------------------
   * Header shadow on scroll + sticky mobile action bar
   * ------------------------------------------------------------------ */
  var header = document.querySelector('.site-header');
  var actionBar = document.querySelector('.action-bar');
  var ticking = false;
  function onScroll() {
    var y = window.pageYOffset || doc.scrollTop;
    if (header) header.classList.toggle('is-scrolled', y > 8);
    if (actionBar) actionBar.classList.toggle('is-visible', y > 240);
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ------------------------------------------------------------------
   * Mobile menu (off-canvas) with iOS-safe scroll lock and focus trap
   * ------------------------------------------------------------------ */
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('mobile-menu');
  var panel = menu ? menu.querySelector('.mobile-menu__panel') : null;
  var scrollY = 0;
  var lastFocus = null;

  function focusables() {
    return panel ? Array.prototype.filter.call(
      panel.querySelectorAll('a[href], button:not([disabled])'),
      function (el) { return el.offsetParent !== null; }
    ) : [];
  }

  function openMenu() {
    if (!menu || menu.classList.contains('is-open')) return;
    lastFocus = document.activeElement;
    scrollY = window.pageYOffset || doc.scrollTop;
    document.body.style.top = (-scrollY) + 'px';
    doc.classList.add('menu-open');
    menu.classList.add('is-open');
    menu.setAttribute('aria-hidden', 'false');
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Close menu');
    var f = focusables();
    if (f.length) setTimeout(function () { f[0].focus({ preventScroll: true }); }, 50);
  }

  function closeMenu(restoreFocus) {
    if (!menu || !menu.classList.contains('is-open')) return;
    menu.classList.remove('is-open');
    menu.setAttribute('aria-hidden', 'true');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    doc.classList.remove('menu-open');
    document.body.style.top = '';
    // restore scroll position without smooth animation
    var prev = doc.style.scrollBehavior;
    doc.style.scrollBehavior = 'auto';
    window.scrollTo(0, scrollY);
    doc.style.scrollBehavior = prev;
    if (restoreFocus !== false && lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }

  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      menu.classList.contains('is-open') ? closeMenu() : openMenu();
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('[data-close-menu]')) { closeMenu(); return; }
      var link = e.target.closest('a[href]');
      if (link) {
        var href = link.getAttribute('href');
        // same-page anchor: close first, then jump
        if (href.indexOf('#') !== -1 && (href.charAt(0) === '#' || link.pathname === location.pathname)) {
          e.preventDefault();
          closeMenu(false);
          var target = document.getElementById(href.split('#')[1]);
          if (target) setTimeout(function () { target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 30);
        } else {
          closeMenu(false);
        }
      }
    });
    document.addEventListener('keydown', function (e) {
      if (!menu.classList.contains('is-open')) return;
      if (e.key === 'Escape') { closeMenu(); return; }
      if (e.key === 'Tab') {
        var f = focusables();
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth >= DESKTOP) closeMenu(false);
    });
    // Sub-menu accordion
    Array.prototype.forEach.call(menu.querySelectorAll('.mobile-menu__sub-toggle'), function (btn) {
      btn.addEventListener('click', function () {
        var sub = document.getElementById(btn.getAttribute('aria-controls'));
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', open ? 'false' : 'true');
        if (sub) sub.hidden = open;
      });
    });
  }

  // Desktop dropdown: allow keyboard/touch toggling on "Services"
  Array.prototype.forEach.call(document.querySelectorAll('.has-dropdown > a'), function (a) {
    a.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') a.blur();
    });
  });

  /* ------------------------------------------------------------------
   * Images: graceful fallback if a stock photo fails to load
   * ------------------------------------------------------------------ */
  function markBroken(img) {
    img.classList.add('is-broken');
    var fig = img.closest('.media');
    if (fig) fig.classList.add('is-broken');
  }
  Array.prototype.forEach.call(document.images, function (img) {
    if (img.complete && img.naturalWidth === 0 && img.getAttribute('src')) markBroken(img);
    img.addEventListener('error', function () { markBroken(img); });
  });

  /* ------------------------------------------------------------------
   * Reveal on scroll
   * ------------------------------------------------------------------ */
  var revealSel = '.card, .feature-item, .step, .gallery__item, .faq__item, .split__media, .feature__media, .grid-3 .media, .contact-card';
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    Array.prototype.forEach.call(document.querySelectorAll(revealSel), function (el, i) {
      el.classList.add('reveal');
      el.style.transitionDelay = (i % 4) * 70 + 'ms';
      io.observe(el);
    });
  }

  /* ------------------------------------------------------------------
   * Attribution: keep first-touch UTM / click IDs for the lead e-mail
   * ------------------------------------------------------------------ */
  var UTM_KEY = 'ra_attrib';
  function getAttribution() {
    var stored = null;
    try { stored = JSON.parse(localStorage.getItem(UTM_KEY) || 'null'); } catch (e) {}
    var params = new URLSearchParams(location.search);
    var keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'gbraid', 'wbraid', 'fbclid'];
    var found = {};
    keys.forEach(function (k) { if (params.get(k)) found[k] = params.get(k).slice(0, 150); });
    if (Object.keys(found).length) {
      found.landing = location.pathname;
      found.ref = document.referrer ? document.referrer.slice(0, 150) : '';
      try { localStorage.setItem(UTM_KEY, JSON.stringify(found)); } catch (e) {}
      return found;
    }
    if (!stored && document.referrer && document.referrer.indexOf(location.host) === -1) {
      stored = { ref: document.referrer.slice(0, 150), landing: location.pathname };
      try { localStorage.setItem(UTM_KEY, JSON.stringify(stored)); } catch (e) {}
    }
    return stored || {};
  }
  var attribution = getAttribution();

  /* ------------------------------------------------------------------
   * Click tracking (only if gtag / fbq are configured)
   * ------------------------------------------------------------------ */
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-track]');
    if (!el) return;
    var name = el.getAttribute('data-track');
    try {
      if (window.gtag) gtag('event', name.indexOf('sms') === 0 ? 'sms_click' : (name.indexOf('call') === 0 ? 'phone_click' : 'cta_click'), { location: name });
      if (window.fbq && (name.indexOf('sms') === 0 || name.indexOf('call') === 0)) fbq('track', 'Contact');
    } catch (err) {}
  });

  /* ------------------------------------------------------------------
   * Lead forms: validation, phone mask, AJAX submit (with no-JS fallback)
   * ------------------------------------------------------------------ */
  function digits(v) { return (v || '').replace(/\D/g, ''); }
  function formatPhone(v) {
    var d = digits(v);
    if (d.length === 11 && d.charAt(0) === '1') d = d.slice(1);
    d = d.slice(0, 10);
    if (d.length < 4) return d;
    if (d.length < 7) return '(' + d.slice(0, 3) + ') ' + d.slice(3);
    return '(' + d.slice(0, 3) + ') ' + d.slice(3, 6) + '-' + d.slice(6);
  }
  var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function validateField(input) {
    var field = input.closest('.field');
    if (!field) return true;
    var v = (input.value || '').trim();
    var ok = true;
    if (input.required && !v) ok = false;
    if (ok && input.name === 'phone') {
      var d = digits(v);
      if (d.length === 11 && d.charAt(0) === '1') d = d.slice(1);
      ok = d.length === 10;
    }
    if (ok && input.type === 'email' && v) ok = emailRe.test(v);
    if (ok && input.name === 'name') ok = v.length >= 2;
    field.classList.toggle('has-error', !ok);
    input.setAttribute('aria-invalid', ok ? 'false' : 'true');
    var msg = field.querySelector('.field__error');
    if (msg) msg.hidden = ok;
    return ok;
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-lead-form]'), function (form) {
    var status = form.querySelector('[data-form-status]');
    var btn = form.querySelector('[data-submit]');
    var label = form.querySelector('[data-submit-label]');
    var originalLabel = label ? label.textContent : '';

    // hidden context fields
    var pageField = form.querySelector('[name="page_url"]');
    if (pageField) pageField.value = location.href.split('#')[0].slice(0, 300);
    var utmField = form.querySelector('[name="utm"]');
    if (utmField) utmField.value = JSON.stringify(attribution).slice(0, 900);

    var phone = form.querySelector('[data-phone]');
    if (phone) phone.addEventListener('input', function () {
      var pos = phone.value.length;
      phone.value = formatPhone(phone.value);
      if (document.activeElement === phone && pos === phone.value.length) {
        try { phone.setSelectionRange(pos, pos); } catch (e) {}
      }
    });

    Array.prototype.forEach.call(form.querySelectorAll('input, select, textarea'), function (el) {
      el.addEventListener('blur', function () { if (el.value) validateField(el); });
      el.addEventListener('input', function () {
        if (el.closest('.field') && el.closest('.field').classList.contains('has-error')) validateField(el);
      });
      el.addEventListener('change', function () { if (el.tagName === 'SELECT') validateField(el); });
    });

    function showStatus(msg, isError) {
      if (!status) return;
      status.hidden = false;
      status.className = 'form-alert' + (isError ? ' form-alert--error' : '');
      status.innerHTML = msg;
    }
    function setLoading(on) {
      if (!btn) return;
      btn.disabled = on;
      if (label) label.textContent = on ? 'Sending…' : originalLabel;
      var sp = btn.querySelector('.spinner');
      if (on && !sp) { sp = document.createElement('span'); sp.className = 'spinner'; sp.setAttribute('aria-hidden', 'true'); btn.appendChild(sp); }
      if (!on && sp) sp.remove();
    }

    form.addEventListener('submit', function (e) {
      var inputs = form.querySelectorAll('input:not([type=hidden]):not([name=website]), select, textarea');
      var firstBad = null;
      Array.prototype.forEach.call(inputs, function (el) {
        if (!validateField(el) && !firstBad) firstBad = el;
      });
      if (firstBad) {
        e.preventDefault();
        firstBad.focus();
        showStatus('Please fix the highlighted fields.', true);
        return;
      }
      if (!window.fetch || !window.FormData) return; // normal POST fallback

      e.preventDefault();
      setLoading(true);
      if (status) status.hidden = true;

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
        credentials: 'same-origin'
      })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (data) {
          if (data && data.ok) {
            showStatus('Thank you! Your request was sent. Redirecting…', false);
            try { if (window.gtag) gtag('event', 'form_submit', { form_id: form.id }); } catch (err) {}
            window.location.href = data.redirect || '/thank-you';
          } else {
            setLoading(false);
            if (data && data.errors) {
              Object.keys(data.errors).forEach(function (k) {
                var el = form.querySelector('[name="' + k + '"]');
                if (el) {
                  var f = el.closest('.field');
                  if (f) { f.classList.add('has-error'); var m = f.querySelector('.field__error'); if (m) { m.hidden = false; m.textContent = data.errors[k]; } }
                }
              });
            }
            showStatus((data && data.message) || 'Sorry, we could not send your request. Please text us instead.', true);
          }
        })
        .catch(function () {
          setLoading(false);
          showStatus('Connection problem. Please try again or text us directly.', true);
        });
    });
  });

  // Current year helpers, if any
  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) { el.textContent = new Date().getFullYear(); });
})();
