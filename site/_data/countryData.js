// Ateliers, Staedte, Umgebungsorte und Event-Zahlen pro aktiviertem Land, z.B.
// countryData.ch.studios - Grundlage der laenderweisen Seiten (siehe
// ch/ch.11tydata.js und sitemap-country.njk).
const { enabledCountries } = require("../_11ty/countries.js");
const studiosFn = require("./studios.js");
const citiesFn = require("./cities.js");
const nearbyTownsFn = require("./nearbyTowns.js");
const eventStatsFn = require("./eventStats.js");

module.exports = async function () {
  const out = {};
  for (const c of enabledCountries()) {
    out[c.code] = {
      studios: await studiosFn.forCountry(c.iso),
      cities: await citiesFn.forCountry(c.iso),
      nearbyTowns: await nearbyTownsFn.forCountry(c.iso),
      eventStats: await eventStatsFn.forCountry(c.iso),
    };
  }
  return out;
};
