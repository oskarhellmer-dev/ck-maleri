// CK Måleri & Golv — småsaker
document.addEventListener('DOMContentLoaded', function () {
  var y = document.getElementById('ar');
  if (y) y.textContent = new Date().getFullYear();

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? 'Stäng' : 'Meny';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.textContent = 'Meny';
      }
    });
  }

  // Pausa hero-videon när den är utanför bild (sparar batteri på mobil)
  var heroVideo = document.querySelector('.hero-media video');
  if (heroVideo && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { heroVideo.play().catch(function () {}); }
        else { heroVideo.pause(); }
      });
    }, { threshold: 0.15 }).observe(heroVideo);
  }
});
