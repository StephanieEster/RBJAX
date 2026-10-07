/* Rio Cleaning Services — site behavior: navigation, accordions, tabs, estimate form, event tracking. */
(function () {
  'use strict';
  var doc = document;
  var root = doc.documentElement;
  root.classList.add('js');

  /* ---------------------------------------------------------- tracking */
  var T = window.RIO_TRACKING || {};
  window.dataLayer = window.dataLayer || [];
  function track(name, params) {
    params = params || {};
    window.dataLayer.push(Object.assign({ event: name }, params));
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, params);
      var label = name === 'phone_click' ? T.adsCallLabel : name === 'quote_form_submit' ? T.adsFormLabel : '';
      if (T.adsId && label) window.gtag('event', 'conversion', { send_to: T.adsId + '/' + label });
    }
    if (typeof window.fbq === 'function') {
      if (name === 'phone_click') window.fbq('track', 'Contact');
      else if (name === 'quote_form_submit') window.fbq('track', 'Lead');
      else window.fbq('trackCustom', name, params);
    }
  }
  window.rioTrack = track;

  doc.addEventListener('click', function (ev) {
    var el = ev.target.closest('[data-track]');
    if (!el) return;
    var p = { link_url: el.getAttribute('href') || '', page_path: location.pathname };
    if (el.dataset.where) p.location = el.dataset.where;
    if (el.dataset.service) p.service = el.dataset.service;
    track(el.dataset.track, p);
  });

  /* ---------------------------------------------------------- header */
  var header = doc.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var nav = doc.getElementById('site-nav');
  var menuBtn = doc.querySelector('.menu-toggle');
  function setMenu(open) {
    if (!nav || !menuBtn) return;
    menuBtn.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    doc.body.classList.toggle('menu-open', open);
  }
  if (menuBtn) menuBtn.addEventListener('click', function () { setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'); });
  if (nav) nav.addEventListener('click', function (ev) { if (ev.target.closest('a')) setMenu(false); });
  window.addEventListener('resize', function () { if (window.innerWidth > 1080) setMenu(false); });

  doc.querySelectorAll('.sub-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', String(open));
      btn.parentElement.classList.toggle('is-open', open);
    });
  });
  doc.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape') return;
    if (menuBtn && menuBtn.getAttribute('aria-expanded') === 'true') { setMenu(false); menuBtn.focus(); }
    doc.querySelectorAll('.sub-toggle[aria-expanded="true"]').forEach(function (b) {
      b.setAttribute('aria-expanded', 'false'); b.parentElement.classList.remove('is-open');
    });
  });
  doc.addEventListener('click', function (ev) {
    if (window.innerWidth <= 1080) return;
    doc.querySelectorAll('.has-sub.is-open').forEach(function (li) {
      if (!li.contains(ev.target)) { li.classList.remove('is-open'); li.querySelector('.sub-toggle').setAttribute('aria-expanded', 'false'); }
    });
  });

  /* ---------------------------------------------------------- accordion */
  doc.querySelectorAll('.acc-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', String(open));
      doc.getElementById(btn.getAttribute('aria-controls')).hidden = !open;
    });
  });

  /* ---------------------------------------------------------- tabs */
  doc.querySelectorAll('[role="tablist"]').forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        doc.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
    }
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { select(tab); });
      tab.addEventListener('keydown', function (ev) {
        var next = null;
        if (ev.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
        else if (ev.key === 'ArrowLeft') next = tabs[(i - 1 + tabs.length) % tabs.length];
        else if (ev.key === 'Home') next = tabs[0];
        else if (ev.key === 'End') next = tabs[tabs.length - 1];
        if (next) { ev.preventDefault(); select(next); next.focus(); }
      });
    });
  });

  /* ---------------------------------------------------------- reveal on scroll */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce && 'IntersectionObserver' in window) {
    var targets = doc.querySelectorAll('.sec-head, .diff-list li, .svc-feature, .svc-row, .bw-list li, .step, .inc-group, ' +
      '.story-copy, .area-copy, .acc, .hub-row, .icon-grid li, .rel-list li, .table-wrap, .state-list li, .mo-split > div');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    targets.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight) return; // already on screen: never hide it
      el.classList.add('reveal');
      io.observe(el);
    });
  }

  /* ---------------------------------------------------------- estimate form */
  var msgs = {
    name: 'Please enter your name.',
    phone: 'Please enter a valid 10-digit U.S. phone number.',
    email: 'Please enter a valid email address.',
    emailRequired: 'Please enter your email so we can reply by email.',
    zip: 'Please enter a 5-digit ZIP code.',
    service: 'Please choose the type of cleaning.'
  };
  function digits(v) { return (v || '').replace(/\D/g, ''); }
  function validPhone(v) {
    var d = digits(v);
    if (d.length === 11 && d.charAt(0) === '1') d = d.slice(1);
    return d.length === 10 && /^[2-9]\d{2}[2-9]\d{6}$/.test(d);
  }
  function validEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); }

  function setError(form, name, text) {
    var input = form.elements[name];
    if (!input) return;
    var field = input.closest('.field');
    var err = doc.getElementById('e-' + name);
    if (field) field.classList.toggle('has-error', !!text);
    input.setAttribute('aria-invalid', text ? 'true' : 'false');
    if (err) err.textContent = text || '';
  }

  function validate(form, only) {
    var f = form.elements;
    var errors = {};
    if (!f.name.value.trim() || f.name.value.trim().length < 2) errors.name = msgs.name;
    if (!validPhone(f.phone.value)) errors.phone = msgs.phone;
    var email = f.email.value.trim();
    var wantsEmail = form.querySelector('input[name="contact_method"]:checked');
    wantsEmail = wantsEmail && wantsEmail.value === 'Email';
    if (email && !validEmail(email)) errors.email = msgs.email;
    else if (!email && wantsEmail) errors.email = msgs.emailRequired;
    if (!/^\d{5}$/.test(f.zip.value.trim())) errors.zip = msgs.zip;
    if (!f.service.value) errors.service = msgs.service;
    ['name', 'phone', 'email', 'zip', 'service'].forEach(function (k) {
      if (!only || only === k) setError(form, k, errors[k]);
    });
    return errors;
  }

  function formatPhone(input) {
    var d = digits(input.value);
    if (d.length === 11 && d.charAt(0) === '1') d = d.slice(1);
    if (d.length === 10) input.value = '(' + d.slice(0, 3) + ') ' + d.slice(3, 6) + '-' + d.slice(6);
  }

  doc.querySelectorAll('.qform').forEach(function (form) {
    var started = false;
    var loadedAt = Date.now();
    var btn = form.querySelector('.btn-submit');
    var label = btn.querySelector('.btn-label');
    var status = form.querySelector('.form-status');
    var sending = false;

    form.addEventListener('focusin', function () {
      if (started) return;
      started = true;
      track('quote_form_start', { form_location: form.querySelector('[name="page"]').value });
    });
    form.elements.phone.addEventListener('blur', function () { formatPhone(this); });
    form.elements.zip.addEventListener('input', function () { this.value = digits(this.value).slice(0, 5); });
    ['name', 'phone', 'email', 'zip', 'service'].forEach(function (k) {
      var el = form.elements[k];
      el.addEventListener(el.tagName === 'SELECT' ? 'change' : 'blur', function () {
        if (el.value || el.getAttribute('aria-invalid') === 'true') validate(form, k);
      });
    });

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (sending) return;
      var errors = validate(form);
      var keys = Object.keys(errors);
      if (keys.length) {
        status.className = 'form-status is-error';
        status.textContent = 'Please check the highlighted field' + (keys.length > 1 ? 's' : '') + '.';
        form.elements[keys[0]].focus();
        return;
      }
      // Spam protection: honeypot filled or submitted faster than a person could type.
      if (form.elements.website.value || Date.now() - loadedAt < 2500) {
        status.className = 'form-status is-ok';
        status.textContent = 'Thank you! Your request was sent.';
        return;
      }
      sending = true;
      btn.disabled = true;
      btn.classList.add('is-loading');
      label.textContent = 'Sending…';
      status.className = 'form-status';
      status.textContent = '';
      form.elements.started.value = String(loadedAt);
      form.elements.page_url.value = location.href.split('#')[0];
      var body = new FormData(form);
      var info = { page: body.get('page'), name: String(body.get('name') || '').trim(), service: body.get('service'), frequency: body.get('frequency') || '' };

      function fail(message) {
        sending = false;
        btn.disabled = false;
        btn.classList.remove('is-loading');
        label.textContent = 'Request My Free Estimate';
        status.className = 'form-status is-error';
        status.innerHTML = message || 'Sorry, your request could not be sent right now. Please try again, or call us at ' +
          '<a href="tel:+12676944609">(267) 694-4609</a>.';
      }

      fetch(form.getAttribute('action'), { method: 'POST', headers: { Accept: 'application/json' }, body: body })
        .then(function (res) {
          return res.json().catch(function () { return { ok: false }; });
        })
        .then(function (json) {
          if (!json.ok) {
            var fields = Object.keys(json.errors || {});
            fields.forEach(function (k) { setError(form, k, json.errors[k]); });
            if (fields.length && form.elements[fields[0]]) form.elements[fields[0]].focus();
            fail(json.message);
            return;
          }
          track('quote_form_submit', { form_location: info.page, service: info.service, frequency: info.frequency });
          form.classList.add('is-sent');
          status.className = 'form-status is-ok';
          status.innerHTML = '<strong>Thank you, ' + escapeHtml(info.name.split(' ')[0]) + '!</strong> Your estimate request was sent. ' +
            'We\'ll get back to you soon. For anything urgent, call <a href="tel:+12676944609">(267) 694-4609</a>.';
          status.focus();
        })
        .catch(function () { fail(); });
    });
  });

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }

  /* Without JavaScript the form posts normally: /contact/?sent=1 on success, ?form_error=1 otherwise. */
  if (/[?&]sent=1/.test(location.search)) {
    var sent = doc.getElementById('sent-msg');
    if (sent) sent.hidden = false;
  }
  if (/[?&]form_error=1/.test(location.search)) {
    doc.querySelectorAll('.qform .form-status').forEach(function (s) {
      s.className = 'form-status is-error';
      s.innerHTML = 'Please check your details and try again, or call us at <a href="tel:+12676944609">(267) 694-4609</a>.';
    });
  }
  root.classList.add('js-ready');
})();
