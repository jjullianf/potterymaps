// Gemeinsames Hover-Verhalten fuer alle Leaflet-Karten der Seite (Startseite,
// /ch/karte/, Stadtseiten, Alle-Staedte-Uebersicht, Studios-in-der-Naehe).
// Auf Desktop (Hover verfuegbar) oeffnet sich das Popup beim Ueberfahren des
// Pins und schliesst sich wieder, sobald die Maus Pin UND Popup verlassen hat
// - kein Klick noetig. Auf Touch-Geraeten gibt es keinen Hover, dort bleibt es
// beim Standard-Leaflet-Verhalten (Popup oeffnet sich per Tap).
window.potterymapsAttachHoverPopup = function (marker) {
  var supportsHover = window.matchMedia && window.matchMedia("(hover: hover)").matches;
  if (!supportsHover) return;

  var closeTimer = null;
  function cancelClose() {
    if (closeTimer) {
      clearTimeout(closeTimer);
      closeTimer = null;
    }
  }
  function scheduleClose() {
    cancelClose();
    closeTimer = setTimeout(function () {
      marker.closePopup();
    }, 200);
  }

  marker.on("mouseover", function () {
    cancelClose();
    marker.openPopup();
  });
  marker.on("mouseout", scheduleClose);
  marker.on("popupopen", function (e) {
    var el = e.popup.getElement();
    if (!el) return;
    el.addEventListener("mouseenter", cancelClose);
    el.addEventListener("mouseleave", scheduleClose);
  });
};
