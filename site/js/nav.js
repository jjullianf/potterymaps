(function () {
  "use strict";

  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");
  var backdrop = document.getElementById("nav-backdrop");
  if (!toggle || !nav) return;

  function isOpen() {
    return nav.classList.contains("open");
  }

  function openMenu() {
    nav.classList.add("open");
    toggle.setAttribute("aria-expanded", "true");
    if (backdrop) backdrop.hidden = false;
  }

  function closeMenu() {
    nav.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
    if (backdrop) backdrop.hidden = true;
  }

  if (backdrop) backdrop.addEventListener("click", closeMenu);

  toggle.addEventListener("click", function () {
    if (isOpen()) closeMenu();
    else openMenu();
  });

  // Schliesst das Menu, wenn auf einen Link darin geklickt wird (Navigation
  // findet dann zwar sowieso statt, aber bei In-Page-Ankern oder falls die
  // Navigation per History-API abgefangen wuerde, bleibt es sonst offen).
  nav.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", closeMenu);
  });

  // Schliesst bei Klick ausserhalb von Nav/Toggle.
  document.addEventListener("click", function (e) {
    if (!isOpen()) return;
    if (nav.contains(e.target) || toggle.contains(e.target)) return;
    closeMenu();
  });

  // Schliesst mit Escape, Fokus zurueck auf den Toggle-Button.
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && isOpen()) {
      closeMenu();
      toggle.focus();
    }
  });

  // Falls der Viewport ueber den Mobile-Breakpoint vergroessert wird (z.B.
  // Fenster-Resize oder Tablet-Drehung), offenen Zustand zuruecksetzen, damit
  // die Desktop-Navigation nicht versehentlich "offen" (fixed-Overlay) bleibt.
  var mq = window.matchMedia("(min-width: 768px)");
  function handleBreakpointChange(e) {
    if (e.matches) closeMenu();
  }
  if (mq.addEventListener) mq.addEventListener("change", handleBreakpointChange);
  else if (mq.addListener) mq.addListener(handleBreakpointChange);
})();
