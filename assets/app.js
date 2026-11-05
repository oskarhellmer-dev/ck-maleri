// CK Måleri & Golv — småsaker
document.addEventListener('DOMContentLoaded', function () {
  var y = document.getElementById('ar');
  if (y) y.textContent = new Date().getFullYear();

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Språkmedvetna meddelanden (sajten har både svenska och norska sidor)
  var isNb = (document.documentElement.lang || '').indexOf('nb') === 0;
  var MSG = isNb
    ? { req: 'Fyll ut dette feltet.', email: 'Skriv inn en gyldig e-postadresse.', sending: 'Sender…' }
    : { req: 'Fyll i detta fält.', email: 'Ange en giltig e-postadress.', sending: 'Skickar…' };

  // --- Mobilmeny ---
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    var closeMenu = function () {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = 'Meny';
      document.body.classList.remove('menu-open');
    };
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? 'Stäng' : 'Meny';
      document.body.classList.toggle('menu-open', open);
    });
    nav.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (a && nav.classList.contains('open')) {
        var href = a.getAttribute('href') || '';
        closeMenu();
        if (href === '#kontakt') {
          e.preventDefault();
          var target = document.getElementById('kontakt');
          if (target) { target.scrollIntoView({ behavior: 'smooth' }); }
          else { window.location.hash = '#kontakt'; }
        }
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) closeMenu();
    });
  }

  // --- Pausa hero-videon när den är utanför bild (sparar batteri på mobil) ---
  var heroVideo = document.querySelector('.hero-bg video');
  if (heroVideo && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { heroVideo.play().catch(function () {}); }
        else { heroVideo.pause(); }
      });
    }, { threshold: 0.15 }).observe(heroVideo);
  }

  // --- Header: visa knappar först när man scrollat förbi hero.
  //     rAF-throttlad så den aldrig körs en gång per frame.
  var header = document.querySelector('.site-header');
  if (header) {
    var ticking = false;
    var updateHeader = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 380);
      ticking = false;
    };
    updateHeader();
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(updateHeader); }
    }, { passive: true });
  }

  // --- Scroll-reveal: stig upp + tona in en gång när sektionen når bilden.
  //     Läggs bara på element som redan är under folden, så inget blinkar i toppen.
  if (!reduce && 'IntersectionObserver' in window) {
    var targets = document.querySelectorAll('main .section, main > section, .svc, .review, .steps li, figure.fig, .cta-band');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
    targets.forEach(function (el) {
      if (el.getBoundingClientRect().top > window.innerHeight - 80) {
        el.classList.add('reveal');
        io.observe(el);
      }
    });
  }

  // --- Formulär: klientvalidering + laddningsläge (formsubmit.co postar som vanligt) ---
  var form = document.querySelector('form.form-card');
  if (form) {
    var clearErr = function (field) {
      field.removeAttribute('aria-invalid');
      var e = field.parentNode.querySelector('.field-error');
      if (e) e.remove();
    };
    var setErr = function (field, msg) {
      field.setAttribute('aria-invalid', 'true');
      var e = field.parentNode.querySelector('.field-error');
      if (!e) { e = document.createElement('p'); e.className = 'field-error'; field.parentNode.appendChild(e); }
      e.textContent = msg;
    };
    var validate = function () {
      var firstBad = null;
      form.querySelectorAll('input,select,textarea').forEach(function (f) {
        if (f.type === 'hidden' || f.name === '_honey') return;
        clearErr(f);
        var val = (f.value || '').trim();
        if (f.hasAttribute('required') && !val) {
          setErr(f, MSG.req); firstBad = firstBad || f;
        } else if (f.type === 'email' && val && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) {
          setErr(f, MSG.email); firstBad = firstBad || f;
        }
      });
      return firstBad;
    };
    form.addEventListener('submit', function (e) {
      var bad = validate();
      if (bad) { e.preventDefault(); bad.focus(); return; }
      var btn = form.querySelector('button[type="submit"], button');
      if (btn) { btn.disabled = true; btn.textContent = MSG.sending; }
    });
    form.addEventListener('input', function (e) {
      if (e.target && e.target.getAttribute('aria-invalid')) clearErr(e.target);
    });
  }

  // --- Tagline: ord tennes ett og ett i leserekkefølge mens seksjonen passerer.
  //     rAF-throttlet, og faller tilbake til full farge ved redusert bevegelse.
  var tl = document.querySelector('[data-tagline]');
  if (tl) {
    var words = tl.textContent.trim().split(/\s+/);
    tl.textContent = '';
    var spans = words.map(function (w) {
      var s = document.createElement('span');
      s.className = 'word'; s.textContent = w;
      tl.appendChild(s); tl.appendChild(document.createTextNode(' '));
      return s;
    });
    if (reduce) {
      spans.forEach(function (s) { s.classList.add('on'); });
    } else {
      var tlTick = false;
      var revealTagline = function () {
        var r = tl.getBoundingClientRect();
        var vh = window.innerHeight || 800;
        var p = (vh - r.top) / (r.height + vh * 0.5);
        p = Math.max(0, Math.min(1, p));
        var n = Math.round(p * spans.length);
        spans.forEach(function (s, i) { s.classList.toggle('on', i < n); });
        tlTick = false;
      };
      revealTagline();
      window.addEventListener('scroll', function () {
        if (!tlTick) { tlTick = true; requestAnimationFrame(revealTagline); }
      }, { passive: true });
      window.addEventListener('resize', revealTagline, { passive: true });
    }
  }
});


// --- Cookieinfo (GDPR) — visas en gång, valsparas. Ingen spårning. ---
function initCookieNotice() {
  var STORAGE_KEY = 'ck-cookie-ok';
  var prev;
  try { prev = localStorage.getItem(STORAGE_KEY); } catch (e) { prev = null; }
  if (prev) return;

  var isNb = (document.documentElement.lang || '').indexOf('nb') === 0;
  var msg = isNb
    ? 'Vi bruker ingen sporingskapsler. Siden lagrer bare det du sender i skjemaet – og ingenting utover det.'
    : 'Vi använder inga spårningskakor. Sajten sparar bara det du skickar i formuläret — och inget mer.';
  var okText = isNb ? 'Skjønner' : 'Jag förstår';
  var policyLabel = isNb ? 'Personvern' : 'Integritetspolicy';
  var policyHref = 'integritetspolicy.html';

  var box = document.createElement('div');
  box.id = 'cookie-notice';
  box.setAttribute('role', 'region');
  box.setAttribute('aria-label', isNb ? 'Informasjon om informasjonskapsler' : 'Information om kakor');

  var txt = document.createElement('p');
  txt.textContent = msg + ' ';
  var link = document.createElement('a');
  link.href = policyHref;
  link.textContent = policyLabel;
  txt.appendChild(link);

  var actions = document.createElement('div');
  actions.className = 'cn-actions';
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'cn-ok';
  btn.textContent = okText;
  btn.addEventListener('click', function () {
    try { localStorage.setItem(STORAGE_KEY, '1'); } catch (e) {}
    box.classList.add('cn-hidden');
  });
  actions.appendChild(btn);

  var wrap = document.createElement('div');
  wrap.className = 'cn-actions';
  wrap.appendChild(txt);
  wrap.appendChild(actions);

  box.appendChild(wrap);
  document.body.appendChild(box);

  // Stäng med Escape (tillgänglighet)
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !box.classList.contains('cn-hidden')) {
      btn.click();
    }
  });
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initCookieNotice);
} else {
  initCookieNotice();
}
