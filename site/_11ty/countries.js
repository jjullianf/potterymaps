// Laender-Konfiguration fuer potterymaps. Templates bekommen das aktive Land
// als Variable "country" (siehe _data/country.js; fuer den /de/-Teil spaeter
// per Pagination-Alias), Daten-Module nutzen COUNTRIES direkt.
const COUNTRIES = {
  ch: {
    code: "ch",
    iso: "CH",
    path: "/ch",
    name: "Schweiz",
    nameIn: "in der Schweiz",
    currency: "CHF",
    lang: "de-CH",
    hreflang: "de-CH",
    hasBlog: true,
    enabled: true,
  },
  de: {
    code: "de",
    iso: "DE",
    path: "/de",
    name: "Deutschland",
    nameIn: "in Deutschland",
    currency: "EUR",
    lang: "de-DE",
    hreflang: "de-DE",
    hasBlog: false,
    enabled: false,
  },
};

const byIso = (iso) => Object.values(COUNTRIES).find((c) => c.iso === String(iso || "").toUpperCase());

module.exports = { COUNTRIES, byIso };
