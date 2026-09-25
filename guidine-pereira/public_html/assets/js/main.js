(function () {
  'use strict';

  var doc = document.documentElement;
  var body = document.body;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------
   * Header shadow on scroll
   * ---------------------------------------------------------------- */
  var header = document.querySelector('.header');
  function onScroll() {
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 10);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ------------------------------------------------------------------
   * Scroll lock that also works on iOS Safari
   * ---------------------------------------------------------------- */
  var lockCount = 0;
  var savedY = 0;
  function lockScroll() {
    if (lockCount++ > 0) return;
    savedY = window.scrollY;
    body.style.position = 'fixed';
    body.style.top = -savedY + 'px';
    body.style.left = '0';
    body.style.right = '0';
    body.style.width = '100%';
    body.classList.add('is-locked');
  }
  function unlockScroll() {
    if (--lockCount > 0) return;
    lockCount = 0;
    body.style.position = '';
    body.style.top = '';
    body.style.left = '';
    body.style.right = '';
    body.style.width = '';
    body.classList.remove('is-locked');
    doc.style.scrollBehavior = 'auto';
    window.scrollTo(0, savedY);
    doc.style.scrollBehavior = '';
  }

  /* ------------------------------------------------------------------
   * Mobile navigation
   * ---------------------------------------------------------------- */
  var nav = document.getElementById('site-nav');
  var burger = document.querySelector('[data-nav-open]');
  var mobileQuery = window.matchMedia('(max-width: 1180px)');
  var navOpen = false;

  function focusables(root) {
    return Array.prototype.filter.call(
      root.querySelectorAll('a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])'),
      function (el) { return el.offsetParent !== null; }
    );
  }

  function openNav() {
    if (navOpen || !nav) return;
    navOpen = true;
    doc.classList.add('nav-open');
    burger.setAttribute('aria-expanded', 'true');
    burger.setAttribute('aria-label', 'Close menu');
    lockScroll();
    var closeBtn = nav.querySelector('.nav__close');
    setTimeout(function () { if (closeBtn) closeBtn.focus({ preventScroll: true }); }, 60);
  }

  function closeNav(returnFocus) {
    if (!navOpen) return;
    navOpen = false;
    doc.classList.remove('nav-open');
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', 'Open menu');
    unlockScroll();
    if (returnFocus) burger.focus({ preventScroll: true });
  }

  if (nav && burger) {
    burger.addEventListener('click', function () { navOpen ? closeNav(true) : openNav(); });
    document.querySelectorAll('[data-nav-close]').forEach(function (el) {
      el.addEventListener('click', function () { closeNav(true); });
    });

    // Close after choosing a link (including #anchors on the same page)
    nav.addEventListener('click', function (e) {
      var link = e.target.closest('a');
      if (link && navOpen) closeNav(false);
    });

    document.addEventListener('keydown', function (e) {
      if (!navOpen) return;
      if (e.key === 'Escape') { closeNav(true); return; }
      if (e.key === 'Tab') {
        var items = focusables(nav);
        if (!items.length) return;
        var first = items[0], last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });

    var onBreakpoint = function (mq) { if (!mq.matches) closeNav(false); };
    if (mobileQuery.addEventListener) mobileQuery.addEventListener('change', onBreakpoint);
    else if (mobileQuery.addListener) mobileQuery.addListener(onBreakpoint);

    // Sub-menu toggles
    nav.querySelectorAll('.sub-toggle').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var li = btn.closest('.has-sub');
        var open = !li.classList.contains('is-open');
        li.classList.toggle('is-open', open);
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
    // Open the services list by default in the drawer when on a service page
    var active = nav.querySelector('.has-sub.is-active');
    if (active && mobileQuery.matches) {
      active.classList.add('is-open');
      active.querySelector('.sub-toggle').setAttribute('aria-expanded', 'true');
    }
    // Close desktop dropdown when clicking elsewhere
    document.addEventListener('click', function (e) {
      if (mobileQuery.matches) return;
      nav.querySelectorAll('.has-sub.is-open').forEach(function (li) {
        if (!li.contains(e.target)) {
          li.classList.remove('is-open');
          li.querySelector('.sub-toggle').setAttribute('aria-expanded', 'false');
        }
      });
    });
  }

  /* ------------------------------------------------------------------
   * Reveal on scroll
   * ---------------------------------------------------------------- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var siblings = el.parentElement ? Array.prototype.filter.call(el.parentElement.children, function (c) { return c.classList.contains('reveal'); }) : [];
        var index = Math.max(0, siblings.indexOf(el));
        el.style.transitionDelay = Math.min(index, 6) * 70 + 'ms';
        el.classList.add('is-in');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ------------------------------------------------------------------
   * Number counters
   * ---------------------------------------------------------------- */
  var counters = document.querySelectorAll('[data-count]');
  function runCounter(el) {
    var target = parseInt(el.getAttribute('data-count'), 10) || 0;
    if (reduceMotion || target < 20) { el.textContent = target; return; }
    var start = null, duration = 1400;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { runCounter(entry.target); cio.unobserve(entry.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ------------------------------------------------------------------
   * Gallery filters
   * ---------------------------------------------------------------- */
  var filters = document.querySelectorAll('[data-filter]');
  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var cat = btn.getAttribute('data-filter');
      filters.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      document.querySelectorAll('[data-gallery] [data-cat]').forEach(function (item) {
        item.classList.toggle('is-hidden', cat !== 'all' && item.getAttribute('data-cat') !== cat);
      });
    });
  });

  /* ------------------------------------------------------------------
   * Lightbox
   * ---------------------------------------------------------------- */
  var lb = document.getElementById('lightbox');
  if (lb) {
    var lbImg = lb.querySelector('.lightbox__img');
    var lbCap = lb.querySelector('.lightbox__caption');
    var set = [], current = 0, lastFocus = null;

    function show(i) {
      current = (i + set.length) % set.length;
      var a = set[current];
      var img = a.querySelector('img');
      lbImg.src = a.getAttribute('href');
      lbImg.alt = img ? img.alt : '';
      lbCap.textContent = a.getAttribute('data-caption') || '';
      [current + 1, current - 1].forEach(function (n) {
        var pre = set[(n + set.length) % set.length];
        if (pre) (new Image()).src = pre.getAttribute('href');
      });
    }
    function openLb(link) {
      var gallery = link.closest('[data-gallery]') || document;
      set = Array.prototype.filter.call(gallery.querySelectorAll('[data-lightbox]'), function (a) { return !a.classList.contains('is-hidden'); });
      lastFocus = link;
      show(set.indexOf(link));
      lb.hidden = false;
      lockScroll();
      requestAnimationFrame(function () { lb.classList.add('is-open'); });
      lb.querySelector('[data-lb-close]').focus({ preventScroll: true });
    }
    function closeLb() {
      lb.classList.remove('is-open');
      setTimeout(function () { lb.hidden = true; lbImg.removeAttribute('src'); }, 200);
      unlockScroll();
      if (lastFocus) lastFocus.focus({ preventScroll: true });
    }

    document.addEventListener('click', function (e) {
      var link = e.target.closest('[data-lightbox]');
      if (!link) return;
      e.preventDefault();
      openLb(link);
    });
    lb.querySelector('[data-lb-close]').addEventListener('click', closeLb);
    lb.querySelector('[data-lb-prev]').addEventListener('click', function () { show(current - 1); });
    lb.querySelector('[data-lb-next]').addEventListener('click', function () { show(current + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lightbox__figure')) closeLb(); });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') closeLb();
      else if (e.key === 'ArrowLeft') show(current - 1);
      else if (e.key === 'ArrowRight') show(current + 1);
      else if (e.key === 'Tab') {
        var items = focusables(lb), first = items[0], last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    var touchX = null;
    lb.addEventListener('touchstart', function (e) { touchX = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (touchX === null) return;
      var dx = e.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
      touchX = null;
    });
  }

  /* ------------------------------------------------------------------
   * Campaign parameters (kept for the session, sent with the form)
   * ---------------------------------------------------------------- */
  var params = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'gclid', 'fbclid'];
  var store = {};
  try { store = JSON.parse(sessionStorage.getItem('gp_attr') || '{}'); } catch (err) { store = {}; }
  var qs = new URLSearchParams(window.location.search);
  var changed = false;
  params.forEach(function (p) { if (qs.get(p)) { store[p] = qs.get(p).slice(0, 200); changed = true; } });
  if (!store.utm_source && document.referrer && document.referrer.indexOf(location.host) === -1) {
    try { store.utm_source = new URL(document.referrer).hostname; changed = true; } catch (err) { /* ignore */ }
  }
  if (changed) { try { sessionStorage.setItem('gp_attr', JSON.stringify(store)); } catch (err) { /* ignore */ } }

  /* ------------------------------------------------------------------
   * Click tracking (call, text, email)
   * ---------------------------------------------------------------- */
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-track]');
    if (!el) return;
    var type = el.getAttribute('data-track');
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: 'contact_click', contact_method: type });
    if (typeof window.gtag === 'function') window.gtag('event', 'contact_click', { method: type });
    if (typeof window.fbq === 'function') window.fbq('track', 'Contact', { method: type });
  });

  /* ------------------------------------------------------------------
   * Estimate forms
   * ---------------------------------------------------------------- */
  function formatPhone(v) {
    var d = v.replace(/\D/g, '');
    if (d.length === 11 && d.charAt(0) === '1') d = d.slice(1);
    if (d.length > 10) return v;
    if (d.length > 6) return '(' + d.slice(0, 3) + ') ' + d.slice(3, 6) + '-' + d.slice(6);
    if (d.length > 3) return '(' + d.slice(0, 3) + ') ' + d.slice(3);
    return d;
  }

  var validators = {
    name: function (v) { return v.trim().length >= 2; },
    phone: function (v) { var d = v.replace(/\D/g, ''); return d.length >= 10 && d.length <= 15; },
    email: function (v) { return v.trim() === '' || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); },
    city: function (v) { return v.trim().length >= 2; },
    service: function (v) { return v !== ''; }
  };

  function setInvalid(form, name, invalid) {
    var input = form.elements[name];
    if (!input) return;
    var field = input.closest('.field');
    if (field) field.classList.toggle('is-invalid', invalid);
    input.setAttribute('aria-invalid', invalid ? 'true' : 'false');
    var err = field && field.querySelector('.field__error');
    if (err) {
      if (!err.id) err.id = input.id + '-error';
      if (invalid) input.setAttribute('aria-describedby', err.id);
      else input.removeAttribute('aria-describedby');
    }
  }

  document.querySelectorAll('[data-estimate-form]').forEach(function (form) {
    params.forEach(function (p) { if (form.elements[p] && store[p]) form.elements[p].value = store[p]; });

    var phone = form.elements.phone;
    if (phone) {
      phone.addEventListener('input', function () {
        var pos = phone.selectionStart === phone.value.length;
        phone.value = formatPhone(phone.value);
        if (pos) phone.setSelectionRange(phone.value.length, phone.value.length);
      });
    }

    Object.keys(validators).forEach(function (name) {
      var input = form.elements[name];
      if (!input) return;
      var evt = input.tagName === 'SELECT' ? 'change' : 'blur';
      input.addEventListener(evt, function () { setInvalid(form, name, !validators[name](input.value)); });
      input.addEventListener('input', function () {
        if (input.closest('.field').classList.contains('is-invalid') && validators[name](input.value)) setInvalid(form, name, false);
      });
    });

    var status = form.querySelector('.form__status');
    var label = form.querySelector('.form__label');
    var labelText = label ? label.textContent : '';

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.classList.contains('is-sending')) return;

      var firstBad = null;
      Object.keys(validators).forEach(function (name) {
        var input = form.elements[name];
        if (!input) return;
        var bad = !validators[name](input.value);
        setInvalid(form, name, bad);
        if (bad && !firstBad) firstBad = input;
      });
      if (firstBad) {
        status.className = 'form__status is-error';
        status.textContent = 'Please check the highlighted fields.';
        firstBad.focus();
        return;
      }

      if (!window.fetch || !window.FormData) { form.submit(); return; }

      form.classList.add('is-sending');
      status.className = 'form__status';
      status.textContent = '';
      if (label) label.textContent = 'Sending...';

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
        credentials: 'same-origin'
      })
        .then(function (res) {
          return res.json().catch(function () { throw new Error('bad response'); });
        })
        .then(function (data) {
          if (data && data.ok) {
            status.className = 'form__status is-success';
            status.textContent = 'Thank you. Your request was sent. Redirecting...';
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({ event: 'estimate_form_success' });
            setTimeout(function () { window.location.href = data.redirect || (window.GP && window.GP.thanks) || '/thank-you'; }, 400);
            return;
          }
          if (data && data.errors) {
            Object.keys(data.errors).forEach(function (name) { setInvalid(form, name, true); });
          }
          throw new Error((data && data.message) || 'error');
        })
        .catch(function (err) {
          form.classList.remove('is-sending');
          if (label) label.textContent = labelText;
          status.className = 'form__status is-error';
          var msg = err && err.message && err.message !== 'error' && err.message !== 'bad response' && err.message.indexOf('fetch') === -1
            ? err.message
            : 'We could not send your request right now. Please call or text us at (843) 492-8374.';
          status.textContent = msg;
        });
    });
  });
})();
