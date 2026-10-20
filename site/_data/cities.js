const fs = require("fs");
const path = require("path");
const targetCities = require("./targetCities.js");
const studiosFn = require("./studios.js");
const site = require("./site.js");
const { COUNTRIES, byIso } = require("../_11ty/countries.js");
const citySlug = require("./citySlug.js");
const pluralize = require("../_11ty/pluralize.js");
const compareStudiosForListing = require("../_11ty/sortStudios.js");
const { buildCityInsights } = require("../_11ty/cityInsights.js");
const cityLeads = require("./cityLeads.js");
const CITY_CENTERS = { DE: require("./cityCentersDe.js") };


// Garantierte Hauptstaedte (mit eigenen Texten) je Land; Deutschland startet ohne
// feste Hauptstaedte - dort entstehen Stadtseiten nur fuer Orte mit Atelier.
const HUB_CITIES = { CH: targetCities, DE: [] };

async function loadCities(iso) {
  const COUNTRY = byIso(iso) || COUNTRIES.ch;
  const hubCities = HUB_CITIES[COUNTRY.iso] || [];
  const studios = await studiosFn.forCountry(COUNTRY.iso);
  const hubNames = new Set(hubCities.map((c) => c.name));

  // Jeder Ort mit mind. einem echten Atelier bekommt eine eigene Seite - nicht nur
  // die 20 garantierten Hauptstaedte. Orte ohne eigenes Atelier bleiben unsichtbar
  // (sie tauchen nur als "Auch in der Nähe"-Verweis auf der zustaendigen
  // Hauptstadt-Seite auf, ueber studios[].nearestHubSlug).
  const studiosByCityName = {};
  studios.forEach((s) => {
    (studiosByCityName[s.city] = studiosByCityName[s.city] || []).push(s);
  });

  const allNames = new Set([...hubNames, ...Object.keys(studiosByCityName)]);

  const base = Array.from(allNames).map((name) => {
    const hubInfo = hubCities.find((c) => c.name === name);
    const isHub = !!hubInfo;
    const slug = hubInfo ? hubInfo.slug : citySlug(name);
    // Featured zuerst, danach Ateliers mit eigenen Bildern vor Ateliers ohne
    // eigene Bilder, danach alphabetisch (siehe _11ty/sortStudios.js).
    const direct = (studiosByCityName[name] || []).slice().sort(compareStudiosForListing);
    const hasAny = direct.length > 0;
    // Stadtfotos sind entfernt (Lizenzgruende): die Stadtseiten nutzen den braunen Verlauf.
    const hasPhoto = false;

    let lat = hubInfo ? hubInfo.lat : null;
    let lng = hubInfo ? hubInfo.lng : null;
    const knownCenter = (CITY_CENTERS[COUNTRY.iso] || {})[name];
    if ((lat === null || lng === null) && knownCenter) {
      lat = knownCenter.lat;
      lng = knownCenter.lng;
    }
    if (lat === null || lng === null) {
      const withCoords = direct.filter((s) => s.lat && s.lng);
      if (withCoords.length) {
        lat = withCoords.reduce((sum, s) => sum + s.lat, 0) / withCoords.length;
        lng = withCoords.reduce((sum, s) => sum + s.lng, 0) / withCoords.length;
      }
    }

    const intro = hubInfo ? hubInfo.intro : `Keramik bemalen in ${name}: Finde hier dein Atelier mit Adresse, Öffnungszeiten und Preisen.`;

    return {
      name,
      slug,
      isHub,
      intro,
      lat,
      lng,
      direct,
      hasAny,
      count: direct.length,
      hasPhoto,
      // Bei den 20 garantierten Staedten ohne eigenes Atelier gilt weiterhin
      // noindex, bis ein Atelier dazukommt. Neue Ortsseiten entstehen nur, wenn
      // bereits ein Atelier existiert, sind also nie leer.
      noindex: isHub && !hasAny,
    };
  });

  const maxCount = Math.max.apply(null, base.map((c) => c.count));

  return base.map((c) => {
    // "Auch in der Nähe": bei Hauptstaedten alle Orte, die per Nachbarschafts-
    // Tabelle dieser Hauptstadt zugeordnet sind und eine eigene Seite haben.
    const nearbyTowns = c.isHub
      ? base
          .filter((o) => !o.isHub && o.hasAny && o.direct[0] && o.direct[0].nearestHubSlug === c.slug)
          .map((o) => ({ name: o.name, slug: o.slug, count: o.count }))
          .sort((a, b) => b.count - a.count)
      : [];

    let introDynamic = "";
    if (c.count > 0 && c.count === maxCount) {
      introDynamic = `${c.name} führt das Verzeichnis aktuell mit ${c.count} gelisteten ${pluralize(c.count, "Atelier", "Ateliers")} an.`;
    } else if (c.count > 0) {
      introDynamic = `Aktuell ${c.count === 1 ? "ist" : "sind"} hier ${c.count} ${pluralize(c.count, "Atelier", "Ateliers")} gelistet.`;
    }

    const cityUrl = `${site.url}${COUNTRY.path}/staedte/${c.slug}/`;

    const jsonLdItemList = c.direct.length
      ? {
          "@context": "https://schema.org",
          "@type": "ItemList",
          itemListElement: c.direct.map((s, i) => ({
            "@type": "ListItem",
            position: i + 1,
            name: s.name,
            url: `${site.url}${COUNTRY.path}/studio/${s.slug}/`,
          })),
        }
      : null;

    const jsonLdBreadcrumb = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "Startseite", item: `${site.url}${COUNTRY.path}/` },
        { "@type": "ListItem", position: 2, name: "Alle Städte", item: `${site.url}${COUNTRY.path}/alle-staedte/` },
        { "@type": "ListItem", position: 3, name: c.name, item: cityUrl },
      ],
    };

    // Fuer die SEO-Zusatzsaetze auf den Stadtseiten: falls ein lokales Atelier
    // explizit Keramik-Cafe oder Porzellan bemalen in seiner Beschreibung erwaehnt,
    // dorthin verlinken statt eine generische, unverlinkte Floskel zu zeigen.
    // Nur Laender mit richCityPages (derzeit Deutschland): datengetriebene Zusatztexte.
    let insights = null;
    if (COUNTRY.richCityPages && c.count > 0) {
      const others = base
        .filter((o) => o.count > 0)
        .sort((x, y) => y.count - x.count || x.name.localeCompare(y.name, "de"))
        .map((o) => ({ name: o.name, slug: o.slug, count: o.count }));
      insights = buildCityInsights(c, others);
      insights.lead = cityLeads[c.name] || (c.isHub ? c.intro : "");
    }

    const cafeMatch = c.direct.find((s) => /café|cafe/i.test(s.description || ""));
    const porzellanMatch = c.direct.find((s) => /porzellan/i.test(s.description || ""));

    return Object.assign({}, c, {
      countryCode: COUNTRY.code,
      country: COUNTRY,
      nearbyTowns,
      // "Auch in der Nähe" zeigte frueher Atelier-Karten aus Nachbarorten direkt auf
      // der Hauptstadt-Seite - jetzt haben diese Orte eigene Seiten, daher zeigt
      // die Karte hier nur noch die eigenen Ateliers.
      mapStudios: c.direct.filter((s) => s.lat && s.lng),
      introDynamic,
      insights,
      cafeMatch,
      porzellanMatch,
      jsonLdItemList,
      jsonLdBreadcrumb,
    });
  });
}

module.exports = async function () {
  return loadCities("CH");
};
module.exports.forCountry = loadCities;
