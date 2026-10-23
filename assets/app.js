// CK Måleri & Golv — småsaker
document.addEventListener('DOMContentLoaded', function () {
  var y = document.getElementById('ar');
  if (y) y.textContent = new Date().getFullYear();

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
        // Scrolla till #kontakt smidigt om menyns offertknapp klickas
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

  // Pausa hero-videon när den är utanför bild (sparar batteri på mobil)
  var heroVideo = document.querySelector('.hero-bg video');
  if (heroVideo && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { heroVideo.play().catch(function () {}); }
        else { heroVideo.pause(); }
      });
    }, { threshold: 0.15 }).observe(heroVideo);
  }

  // Visa knappar i headern först när man scrollat förbi hero (minskar brus i toppen)
  var header = document.querySelector('.site-header');
  if (header) {
    var scrolled = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 380);
    };
    scrolled();
    window.addEventListener('scroll', scrolled, { passive: true });
  }
});
