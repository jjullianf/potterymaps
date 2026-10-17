// Standard-Land fuer alle Seiten, die nicht pro Land erzeugt werden (heute: alles
// ist Schweiz). Seiten mit Pagination ueber Laender ueberschreiben "country"
// per Alias.
const { COUNTRIES } = require("../_11ty/countries.js");

module.exports = COUNTRIES.ch;
