// Gemeinsame Info-Karte fuer alle Leaflet-Karten der Seite (Startseite,
// /ch/karte/, Stadtseiten, Alle-Staedte-Uebersicht, Studios-in-der-Naehe).
// Statt eines Popups ueber dem Pin erscheint beim Antippen/Anklicken eines
// Pins eine feste Karte unten mittig in der Karte; Klick auf die Karte
// oeffnet die Atelier-Seite. Klick auf die Karte (Hintergrund) oder auf das
// x schliesst sie, ein anderer Pin tauscht den Inhalt.
window.potterymapsBindCard = function (marker, map, html) {
  var container = map.getContainer();
  var card = container.querySelector(".map-card");
  if (!card) {
    card = document.createElement("div");
    card.className = "map-card";
    card.hidden = true;
    container.appendChild(card);
    L.DomEvent.disableClickPropagation(card);
    L.DomEvent.disableScrollPropagation(card);
    map.on("click", function () {
      card.hidden = true;
      card.removeAttribute("data-active");
    });
  }
  marker.on("click", function () {
    card.innerHTML = '<button type="button" class="map-card-close" aria-label="Schliessen">×</button>' + html;
    card.querySelector(".map-card-close").addEventListener("click", function () {
      card.hidden = true;
    });
    card.hidden = false;
  });
};
