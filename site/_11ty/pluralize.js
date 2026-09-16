module.exports = function pluralize(count, singular, plural) {
  return count === 1 ? singular : plural !== undefined ? plural : singular + "s";
};
