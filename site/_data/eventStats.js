const studiosFn = require("./studios.js");

async function loadEventStats(iso) {
  const studios = await studiosFn.forCountry(iso);

  function countTag(tag) {
    return studios.filter((s) => s.tagsArray.includes(tag)).length;
  }

  return {
    corporateEvents: countTag("corporate-events"),
    birthdayParties: countTag("birthday-parties"),
    henParty: countTag("hen-party"),
    themedEvents: countTag("themed-events"),
    total: studios.length,
  };
}

module.exports = async function () {
  return loadEventStats("CH");
};
module.exports.forCountry = loadEventStats;
