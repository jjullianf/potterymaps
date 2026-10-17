// Laender, die Seiten erzeugen (Pagination-Quelle fuer alle laenderweisen Seiten).
const { enabledCountries } = require("../_11ty/countries.js");

module.exports = enabledCountries();
