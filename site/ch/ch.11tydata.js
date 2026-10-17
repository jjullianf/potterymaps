// Gilt fuer alle Seiten in diesem Ordner - der Ordnername "ch" ist historisch, die
// Templates werden pro aktiviertem Land erzeugt (siehe "country"). Hier werden
// die laenderabhaengigen Datensaetze auf das Land der jeweiligen Seite gelegt, so
// dass die Templates weiter einfach "studios", "cities", "nearbyTowns" und
// "eventStats" verwenden koennen.
const scoped = (key) => (data) => data.countryData[data.country.code][key];

module.exports = {
  eleventyComputed: {
    studios: scoped("studios"),
    cities: scoped("cities"),
    nearbyTowns: scoped("nearbyTowns"),
    eventStats: scoped("eventStats"),
  },
};
