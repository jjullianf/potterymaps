const studiosFn = require("./studios.js");
const citiesFn = require("./cities.js");
const nearbyTownsFn = require("./nearbyTowns.js");

// Statische Seiten, die es vor dem Laenderumzug bereits an der Wurzel gab und
// die jetzt unter /ch/ liegen - "geneva"/"lucerne" sind hier bewusst nicht
// dabei, die haben schon eigene, dauerhafte Synonym-Redirects (siehe
// redirect-geneva.njk/redirect-lucerne.njk). "grosse-anfrage" ist ebenfalls
// bewusst nicht dabei: das Formular ist laenderuebergreifend nutzbar und liegt
// deshalb weiterhin an der Wurzel, nicht unter /ch/.
const STATIC_PAGES = [
  "/alle-staedte/",
  "/karte/",
  "/events/",
  "/kontakt/",
  "/ueber-uns/",
  "/impressum/",
  "/datenschutz/",
  "/studio-eintragen/",
  "/studio-eintragen/danke/",
  "/blog/weihnachts-teamevent-ideen/",
];

// Baut fuer jede vor dem /ch/-Umzug existierende URL eine Weiterleitung auf
// ihre neue Adresse - Grundlage fuer redirect-old-urls.njk (eine generierte
// Seite pro Eintrag statt manuell gepflegter Einzeldateien).
module.exports = async function () {
  const studios = await studiosFn();
  const cities = await citiesFn();
  const nearbyTowns = await nearbyTownsFn();

  const entries = STATIC_PAGES.map((p) => ({ oldPath: p, newPath: `/ch${p}` }));

  cities.forEach((c) => {
    entries.push({ oldPath: `/staedte/${c.slug}/`, newPath: `/ch/staedte/${c.slug}/` });
  });

  studios.forEach((s) => {
    entries.push({ oldPath: `/studio/${s.slug}/`, newPath: `/ch/studio/${s.slug}/` });
  });

  nearbyTowns.forEach((t) => {
    entries.push({ oldPath: `/studios-nahe/${t.slug}/`, newPath: `/ch/studios-nahe/${t.slug}/` });
  });

  return entries;
};
