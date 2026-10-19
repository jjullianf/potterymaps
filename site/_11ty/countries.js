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
    nameInAll: "in der ganzen Schweiz",
    mapOf: "einer Karte der Schweiz",
    regionsPhrase: "Regionen der Schweiz",
    // Textbausteine fuer die Startseiten-FAQ (Preise/Beispielstaedte)
    faqPriceLead: " und liegen meist zwischen CHF 15 und 50,",
    faqExampleCities: ", u. a. in Zürich, Basel, Bern, Genf, Luzern und vielen weiteren Städten",
    eventFormPath: "/grosse-anfrage/",
    currency: "CHF",
    mapView: { lat: 46.9, lng: 8.2, zoom: 8 },
    richCityPages: false,
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
    nameInAll: "in ganz Deutschland",
    mapOf: "einer Karte von Deutschland",
    regionsPhrase: "Orten in Deutschland",
    faqPriceLead: ",",
    faqExampleCities: "",
    eventFormPath: "/de/event-anfrage/",
    currency: "EUR",
    mapView: { lat: 51.1, lng: 10.4, zoom: 6 },
    mapFit: true,
    richCityPages: true,
    lang: "de-DE",
    hreflang: "de-DE",
    hasBlog: false,
    enabled: true,
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

// Fuellt Platzhalter wie {{NAME_IN}} in landesneutral geschriebenen Texten.
function fillCountryText(country, str) {
  return String(str)
    .replace("{{NAME_IN_ALL}}", country.nameInAll)
    .replace("{{NAME_IN}}", country.nameIn)
    .replace("{{EXAMPLE_CITIES}}", country.faqExampleCities)
    .replace("{{PRICE_LEAD}}", country.faqPriceLead);
}

module.exports = { COUNTRIES, byIso, enabledCountries, fillCountryText };
