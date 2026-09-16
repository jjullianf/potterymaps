const studiosFn = require("./studios.js");

module.exports = async function () {
  const studios = await studiosFn();

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
};
