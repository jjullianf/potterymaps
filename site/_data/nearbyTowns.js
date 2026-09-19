const citySlug = require("./citySlug.js");
const townCoords = require("./townCoords.js");
const studiosFn = require("./studios.js");
const citiesFn = require("./cities.js");
const { haversineKm } = require("./geo.js");

const MAX_RESULTS = 6;
const FAR_RADIUS_KM = 60; // Studios innerhalb dieses Radius werden immer gezeigt.
const MIN_RESULTS = 3; // Falls weniger als das im Radius liegen, trotzdem die naechsten 3 zeigen.

// Baut fuer jeden der ca. 180 garantierten Schweizer Orte OHNE eigene
// Staedte-Seite (city.njk) eine eigene "Studios in der Naehe von [Ort]"-Seite
// (studios-nahe.njk) - Orte, die bereits eine Seite haben (mind. 1 eigenes
// Studio oder eine der 20 Hauptstaedte), werden hier ausgeschlossen, damit keine
// zwei Seiten um dieselbe Anfrage konkurrieren.
module.exports = async function () {
  const studios = await studiosFn();
  const cities = await citiesFn();
  const existingSlugs = new Set(cities.map((c) => c.slug));
  const studiosWithCoords = studios.filter((s) => s.lat && s.lng);
  // Nur Staedte mit mind. einem eigenen Studio kommen als "naechstgelegene
  // Hauptstadt" fuer die Rueckverlinkung infrage - reine leere Hub-Platzhalter
  // (noindex) waeren kein sinnvolles Linkziel.
  const linkableCities = cities.filter((c) => c.hasAny && c.lat && c.lng);

  const seen = new Set();

  return townCoords
    .filter((t) => {
      const slug = citySlug(t.name);
      if (existingSlugs.has(slug) || seen.has(slug)) return false;
      seen.add(slug);
      return true;
    })
    .map((t) => {
      const slug = citySlug(t.name);

      const withDistance = studiosWithCoords
        .map((s) => ({ studio: s, distanceKm: haversineKm(t.lat, t.lng, s.lat, s.lng) }))
        .sort((a, b) => a.distanceKm - b.distanceKm);

      const withinRadius = withDistance.filter((d) => d.distanceKm <= FAR_RADIUS_KM);
      const chosen = (withinRadius.length >= MIN_RESULTS ? withinRadius : withDistance).slice(
        0,
        MAX_RESULTS
      );

      const nearestStudios = chosen.map((d) => Object.assign({}, d.studio, { distanceKm: Math.round(d.distanceKm) }));

      let nearestCity = null;
      let nearestCityDistance = Infinity;
      linkableCities.forEach((c) => {
        const d = haversineKm(t.lat, t.lng, c.lat, c.lng);
        if (d < nearestCityDistance) {
          nearestCityDistance = d;
          nearestCity = c;
        }
      });

      return {
        name: t.name,
        slug,
        lat: t.lat,
        lng: t.lng,
        nearestStudios,
        nearestCityName: nearestCity ? nearestCity.name : null,
        nearestCitySlug: nearestCity ? nearestCity.slug : null,
        nearestCityDistanceKm: nearestCity ? Math.round(nearestCityDistance) : null,
      };
    });
};
