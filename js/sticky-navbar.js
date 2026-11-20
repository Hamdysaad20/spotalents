/**
 * SpotTalents Sticky & Animated Navbar Controller
 * Automatically activates frosted glass & floating elevation on scroll
 */
(function() {
  function initStickyNavbar() {
    var nav = document.querySelector('.navbar');
    if (!nav) return;
    var ticking = false;
    function onScroll() {
      if (!ticking) {
        window.requestAnimationFrame(function() {
          var y = window.pageYOffset || document.documentElement.scrollTop || 0;
          if (y > 20) {
            nav.classList.add('is-scrolled');
          } else {
            nav.classList.remove('is-scrolled');
          }
          ticking = false;
        });
        ticking = true;
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStickyNavbar);
  } else {
    initStickyNavbar();
  }
})();
