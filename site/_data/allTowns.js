// Flache Liste ueber alle aktivierten Laender (Pagination fuer Einzelseiten).
const countryData = require("./countryData.js");

module.exports = async function () {
  const data = await countryData();
  return Object.values(data).flatMap((d) => d.nearbyTowns);
};
