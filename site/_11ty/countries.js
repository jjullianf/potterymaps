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

// Welche Laender tatsaechlich Seiten erzeugen: "enabled" oben, oder voruebergehend
// per Umgebungsvariable (z.B. POTTERYMAPS_COUNTRIES=ch,de npx eleventy), um
// einen Land-Teil lokal zu bauen, ohne ihn live zu schalten.
function enabledCountries() {
  const forced = String(process.env.POTTERYMAPS_COUNTRIES || "")
    .split(",")
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);
  return Object.values(COUNTRIES).filter((c) => (forced.length ? forced.includes(c.code) : c.enabled));
}

const byIso = (iso) => Object.values(COUNTRIES).find((c) => c.iso === String(iso || "").toUpperCase());

module.exports = { COUNTRIES, byIso, enabledCountries };
