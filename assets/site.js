/* KÖV Simply Interiors — site behaviour */
(function () {
  'use strict';

  /* ---------- Navigation: mobile drawer + Locations dropdown ---------- */
  var menuBtn = document.querySelector('.menu-btn');
  var nav = document.getElementById('primary-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var dropdowns = document.querySelectorAll('.nav-item');
  Array.prototype.forEach.call(dropdowns, function (item) {
    var toggle = item.querySelector('.nav-toggle');
    if (!toggle) return;
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      var open = item.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  document.addEventListener('click', function (e) {
    Array.prototype.forEach.call(dropdowns, function (item) {
      if (!item.contains(e.target)) {
        item.classList.remove('open');
        var t = item.querySelector('.nav-toggle');
        if (t) t.setAttribute('aria-expanded', 'false');
      }
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    Array.prototype.forEach.call(dropdowns, function (item) {
      item.classList.remove('open');
      var t = item.querySelector('.nav-toggle');
      if (t) t.setAttribute('aria-expanded', 'false');
    });
    if (nav && nav.classList.contains('open')) {
      nav.classList.remove('open');
      if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
    }
  });

  /* ---------- Motion: reveal on scroll, header state, progress, parallax ---------- */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var groups = [
    ['.hero-copy > *', 90],
    ['.page-hero .shell > *', 90],
    ['.sec-head', 0],
    ['.offer', 70],
    ['.ethos-grid > div', 130],
    ['.value', 70],
    ['.step', 100],
    ['.work-item', 70],
    ['.loc-grid > div', 130],
    ['.loc-card', 110],
    ['.team-card', 80],
    ['.consult-grid > div', 130],
    ['.footer-top > *', 80]
  ];
  groups.forEach(function (g) {
    var els = document.querySelectorAll(g[0]);
    for (var i = 0; i < els.length; i++) {
      els[i].classList.add('reveal');
      if (g[1]) els[i].style.setProperty('--d', (i * g[1]) + 'ms');
    }
  });

  var items = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    for (var k = 0; k < items.length; k++) items[k].classList.add('in');
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -6% 0px' });
    for (var n = 0; n < items.length; n++) io.observe(items[n]);
  }

  var header = document.querySelector('.site-header');
  var bar = document.querySelector('.scroll-progress span');
  var media = document.querySelector('.hero-media');
  var hero = document.querySelector('.hero');
  var ticking = false;

  function frame() {
    var y = window.pageYOffset || document.documentElement.scrollTop || 0;
    if (header) header.classList.toggle('is-scrolled', y > 8);
    if (bar) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + '%';
    }
    if (media && hero && !reduce && y < hero.offsetHeight) {
      media.style.transform = 'translate3d(0,' + (y * 0.14) + 'px,0)';
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(frame); }
  }, { passive: true });
  window.addEventListener('resize', frame, { passive: true });
  frame();

  /* ---------- Lightbox for project photography ---------- */
  var shots = Array.prototype.slice.call(document.querySelectorAll('[data-shot]'));
  if (shots.length) {
    var box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Project photo');
    box.innerHTML =
      '<img alt="">' +
      '<button class="lb-btn lb-close" type="button" aria-label="Close">&#10005;</button>' +
      '<button class="lb-btn lb-prev" type="button" aria-label="Previous photo">&#8249;</button>' +
      '<button class="lb-btn lb-next" type="button" aria-label="Next photo">&#8250;</button>' +
      '<p class="lb-caption"></p>';
    document.body.appendChild(box);

    var lbImg = box.querySelector('img');
    var lbCap = box.querySelector('.lb-caption');
    var index = 0;
    var lastFocus = null;

    function show(i) {
      index = (i + shots.length) % shots.length;
      var img = shots[index].querySelector('img');
      lbImg.src = img.getAttribute('src');
      lbImg.alt = img.getAttribute('alt') || '';
      lbCap.textContent = (shots[index].getAttribute('data-caption') || '') +
        '  ·  ' + (index + 1) + ' / ' + shots.length;
    }
    function open(i) {
      lastFocus = document.activeElement;
      show(i);
      box.classList.add('open');
      document.body.style.overflow = 'hidden';
      box.querySelector('.lb-close').focus();
    }
    function close() {
      box.classList.remove('open');
      document.body.style.overflow = '';
      if (lastFocus) lastFocus.focus();
    }

    shots.forEach(function (s, i) {
      s.addEventListener('click', function () { open(i); });
    });
    box.querySelector('.lb-close').addEventListener('click', close);
    box.querySelector('.lb-prev').addEventListener('click', function () { show(index - 1); });
    box.querySelector('.lb-next').addEventListener('click', function () { show(index + 1); });
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') show(index + 1);
      if (e.key === 'ArrowLeft') show(index - 1);
    });
  }

  /* ---------- Showroom chooser popup ----------
     Any "#consult" link opens this, EXCEPT on a page that has its own form —
     there the link just scrolls to it. The popup's two links are duplicated
     in the homepage chooser section, so turning JavaScript off degrades to a
     normal page load rather than a dead button. */
  var modal = document.getElementById('showroomModal');
  var hasOwnForm = !!document.getElementById('consultForm');

  if (modal) {
    var lastTrigger = null;

    function modalOpen(trigger) {
      lastTrigger = trigger || null;
      modal.hidden = false;
      document.body.style.overflow = 'hidden';
      // next frame, so the transition has a chance to run
      requestAnimationFrame(function () { modal.classList.add('open'); });
      var first = modal.querySelector('.chooser-card');
      if (first) first.focus();
    }

    function modalClose() {
      modal.classList.remove('open');
      document.body.style.overflow = '';
      window.setTimeout(function () { modal.hidden = true; }, 200);
      if (lastTrigger && lastTrigger.focus) lastTrigger.focus();
    }

    Array.prototype.forEach.call(modal.querySelectorAll('[data-modal-close]'), function (el) {
      el.addEventListener('click', modalClose);
    });

    document.addEventListener('click', function (e) {
      var link = e.target.closest ? e.target.closest('a[href$="#consult"]') : null;
      if (!link) return;
      // Inside the popup itself, let the link do its job.
      if (modal.contains(link)) return;
      // A chooser card has already named its showroom — in the popup or in the
      // homepage section. Asking again would be a pointless extra click.
      if (link.classList.contains('chooser-card')) return;

      if (hasOwnForm) {
        // This page has a form — scroll to it instead of asking again.
        var target = document.getElementById('consult');
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
          if (history.replaceState) history.replaceState(null, '', '#consult');
        }
        return;
      }
      e.preventDefault();
      modalOpen(link);
    });

    document.addEventListener('keydown', function (e) {
      if (modal.hidden) return;
      if (e.key === 'Escape') { modalClose(); return; }
      if (e.key !== 'Tab') return;
      // Keep focus inside the dialog while it is open.
      var items = modal.querySelectorAll('a[href], button:not([disabled])');
      if (!items.length) return;
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* ---------- Consultation form -> Web3Forms ----------
     Posts as JSON so the styled confirmation stays on the page. If JavaScript
     never runs, the form still submits natively to the same endpoint. */
  var form = document.getElementById('consultForm');
  var card = document.getElementById('consultCard');
  if (form && card) {
    var errorBox = document.getElementById('formError');
    var submitBtn = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (errorBox) errorBox.hidden = true;

      var required = form.querySelectorAll('[required]');
      for (var i = 0; i < required.length; i++) {
        if (!required[i].value.trim()) { required[i].focus(); return; }
      }
      var email = form.querySelector('#email');
      if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value.trim())) { email.focus(); return; }

      var label = submitBtn ? submitBtn.innerHTML : '';
      if (submitBtn) { submitBtn.disabled = true; submitBtn.innerHTML = 'Sending&hellip;'; }

      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      data.name = ((data.first_name || '') + ' ' + (data.last_name || '')).trim();


      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (res && res.success) {
            card.classList.add('is-sent');
          } else {
            if (errorBox) errorBox.hidden = false;
          }
        })
        .catch(function () { if (errorBox) errorBox.hidden = false; })
        .then(function () {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = label; }
        });
    });
  }
})();
