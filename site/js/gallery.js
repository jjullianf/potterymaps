(function () {
  "use strict";

  // Leichtgewichtiger Swipe-Slider fuer die Studio-Bildergalerie (siehe
  // .eleventy.js studioGallery() fuer das erzeugte Markup) - kein externes
  // Slider-Framework, nur Flexbox + CSS-Transform in Prozent (resize-sicher,
  // kein Neuberechnen von Pixelbreiten noetig).
  function initGallery(root) {
    var track = root.querySelector(".studio-gallery-track");
    var slides = root.querySelectorAll(".studio-gallery-slide");
    var dots = root.querySelectorAll(".studio-gallery-dot");
    var prevBtn = root.querySelector(".studio-gallery-prev");
    var nextBtn = root.querySelector(".studio-gallery-next");
    if (!track || slides.length < 2) return; // nur 1 Bild: kein Slider-Verhalten noetig

    var index = 0;

    function goTo(i) {
      index = (i + slides.length) % slides.length;
      track.style.transform = "translateX(-" + index * 100 + "%)";
      dots.forEach(function (dot, di) { dot.classList.toggle("is-active", di === index); });
    }

    if (prevBtn) prevBtn.addEventListener("click", function () { goTo(index - 1); });
    if (nextBtn) nextBtn.addEventListener("click", function () { goTo(index + 1); });
    dots.forEach(function (dot) {
      dot.addEventListener("click", function () { goTo(parseInt(dot.dataset.index, 10)); });
    });

    // Touch-Swipe: horizontale Wischgeste ueber einen Mindestabstand loest
    // Bildwechsel aus, ohne dabei vertikales Scrollen der Seite zu blockieren.
    var touchStartX = null;
    var touchStartY = null;
    track.addEventListener("touchstart", function (e) {
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
    }, { passive: true });
    track.addEventListener("touchend", function (e) {
      if (touchStartX === null) return;
      var dx = e.changedTouches[0].clientX - touchStartX;
      var dy = e.changedTouches[0].clientY - touchStartY;
      touchStartX = null;
      if (Math.abs(dx) < 40 || Math.abs(dx) < Math.abs(dy)) return;
      goTo(dx < 0 ? index + 1 : index - 1);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-studio-gallery]").forEach(initGallery);
  });
})();
