/* Mountain Weather — progressive enhancements. The site is fully usable without this file. */
(function () {
  'use strict';

  var PHONE = '+18622708862';
  var PHONE_DISPLAY = '(862) 270-8862';
  var EMAIL = 'mountainweather63@gmail.com';
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Header shadow on scroll ---------- */
  var header = document.querySelector('[data-header]');
  if (header) {
    var onScroll = function () {
      if (window.scrollY > 8) header.setAttribute('data-scrolled', '');
      else header.removeAttribute('data-scrolled');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Mobile menu ---------- */
  var toggle = document.querySelector('[data-menu-toggle]');
  var menu = document.querySelector('[data-menu]');
  var quickBar = document.querySelector('.mobile-cta');

  function openMenu() {
    menu.hidden = false;
    requestAnimationFrame(function () { menu.classList.add('is-open'); });
    toggle.setAttribute('aria-expanded', 'true');
    toggle.querySelector('.sr-only').textContent = 'Close menu';
    document.body.classList.add('menu-open');
    if (quickBar) quickBar.classList.add('is-hidden');
    var first = menu.querySelector('a');
    if (first) first.focus();
  }
  function closeMenu(returnFocus) {
    menu.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.querySelector('.sr-only').textContent = 'Open menu';
    document.body.classList.remove('menu-open');
    if (quickBar) quickBar.classList.remove('is-hidden');
    window.setTimeout(function () { if (toggle.getAttribute('aria-expanded') === 'false') menu.hidden = true; }, reduceMotion ? 0 : 300);
    if (returnFocus) toggle.focus();
  }
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      if (toggle.getAttribute('aria-expanded') === 'true') closeMenu(false);
      else openMenu();
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') closeMenu(true);
      // Keep focus inside the open menu (menu + toggle button).
      if (e.key === 'Tab' && toggle.getAttribute('aria-expanded') === 'true') {
        var items = [toggle].concat(Array.prototype.slice.call(menu.querySelectorAll('a, button')));
        var firstEl = items[0];
        var lastEl = items[items.length - 1];
        if (e.shiftKey && document.activeElement === firstEl) { e.preventDefault(); lastEl.focus(); }
        else if (!e.shiftKey && document.activeElement === lastEl) { e.preventDefault(); firstEl.focus(); }
      }
    });
    window.matchMedia('(min-width: 1120px)').addEventListener('change', function (mq) {
      if (mq.matches && toggle.getAttribute('aria-expanded') === 'true') closeMenu(false);
    });
  }

  /* ---------- Scroll reveal ---------- */
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- FAQ accordion animation (native <details> underneath) ---------- */
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var summary = item.querySelector('summary');
    var panel = item.querySelector('.faq-answer');
    if (!summary || !panel || reduceMotion || !panel.animate) return;
    var anim = null;
    summary.addEventListener('click', function (e) {
      e.preventDefault();
      if (anim) anim.cancel();
      if (item.open) {
        var h = panel.offsetHeight;
        anim = panel.animate([{ height: h + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 280, easing: 'cubic-bezier(.2,.7,.2,1)' });
        anim.onfinish = function () { item.open = false; anim = null; };
      } else {
        item.open = true;
        var target = panel.offsetHeight;
        anim = panel.animate([{ height: '0px', opacity: 0 }, { height: target + 'px', opacity: 1 }], { duration: 340, easing: 'cubic-bezier(.2,.7,.2,1)' });
        anim.onfinish = function () { anim = null; };
      }
    });
  });

  /* ---------- Cooling / heating dial ---------- */
  document.querySelectorAll('[data-dial]').forEach(function (dial) {
    var tabs = Array.prototype.slice.call(dial.querySelectorAll('[role="tab"]'));
    var panels = dial.querySelectorAll('[role="tabpanel"]');
    function select(kind, focus) {
      dial.setAttribute('data-mode', kind);
      tabs.forEach(function (t) {
        var on = t.getAttribute('data-tab') === kind;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        if (on && focus) t.focus();
      });
      panels.forEach(function (p) { p.hidden = p.getAttribute('data-panel') !== kind; });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t.getAttribute('data-tab'), false); });
      t.addEventListener('keydown', function (e) {
        var dir = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (e.key === 'Home') dir = -i;
        if (e.key === 'End') dir = tabs.length - 1 - i;
        if (!dir) return;
        e.preventDefault();
        var next = tabs[(i + dir + tabs.length) % tabs.length];
        select(next.getAttribute('data-tab'), true);
      });
    });
    // Start with the season that fits the calendar: heating October–April, cooling May–September.
    var month = new Date().getMonth();
    var initial = month >= 4 && month <= 8 ? 'cooling' : 'heating';
    // Hide panels immediately, then sweep the needle once the dial is on screen.
    panels.forEach(function (p) { p.hidden = p.getAttribute('data-panel') !== initial; });
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-tab') === initial;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
    });
    if ('IntersectionObserver' in window && !reduceMotion) {
      var dio = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) {
          select(dial.getAttribute('data-mode') === 'neutral' ? initial : dial.getAttribute('data-mode'), false);
          dio.disconnect();
        }
      }, { threshold: 0.35 });
      dio.observe(dial);
    } else {
      select(initial, false);
    }
  });

  /* ---------- Contact message composer ---------- */
  var form = document.querySelector('[data-composer]');
  if (form) {
    form.hidden = false;
    var errorsBox = form.querySelector('[data-errors]');
    var status = form.querySelector('[data-status]');
    var lastSubmitter = null;
    form.querySelectorAll('button[type="submit"]').forEach(function (b) {
      b.addEventListener('click', function () { lastSubmitter = b; });
    });

    function setError(field, show) {
      var err = document.getElementById(field.id + '-err');
      field.setAttribute('aria-invalid', show ? 'true' : 'false');
      if (err) err.hidden = !show;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var channel = (e.submitter || lastSubmitter || {}).value || 'sms';
      var topic = form.elements.topic;
      var message = form.elements.message;
      var name = form.elements.name.value.trim();
      var town = form.elements.town.value.trim();
      var text = message.value.trim();

      var topicBad = !topic.value;
      var msgBad = text.length < 10;
      setError(topic, topicBad);
      setError(message, msgBad);
      if (topicBad || msgBad) {
        errorsBox.hidden = false;
        errorsBox.textContent = 'Please fix ' + (topicBad && msgBad ? '2 fields' : '1 field') + ' below before continuing.';
        (topicBad ? topic : message).focus();
        return;
      }
      errorsBox.hidden = true;

      var lines = ['Hi Mountain Weather!', 'Topic: ' + topic.value, text];
      if (name) lines.push('Name: ' + name);
      if (town) lines.push('Town/ZIP: ' + town);
      var body = lines.join('\n');
      var url;
      if (channel === 'whatsapp') {
        url = 'https://wa.me/' + PHONE.replace('+', '') + '?text=' + encodeURIComponent(body);
        window.open(url, '_blank', 'noopener');
        status.textContent = 'WhatsApp is opening in a new tab with your message. Review it and tap send.';
        return;
      }
      if (channel === 'email') {
        url = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(topic.value + ' — website message') + '&body=' + encodeURIComponent(body);
        status.textContent = 'Opening your email app with your message. If nothing happens, email ' + EMAIL + ' directly.';
      } else {
        url = 'sms:' + PHONE + '?&body=' + encodeURIComponent(body);
        status.textContent = 'Opening your texting app with your message. If nothing happens on this device, text ' + PHONE_DISPLAY + ' from your phone.';
      }
      window.location.href = url;
    });

    ['topic', 'message'].forEach(function (n) {
      var el = form.elements[n];
      el.addEventListener(n === 'topic' ? 'change' : 'input', function () {
        if (el.getAttribute('aria-invalid') === 'true') {
          var ok = n === 'topic' ? !!el.value : el.value.trim().length >= 10;
          if (ok) setError(el, false);
        }
      });
    });
  }
})();
