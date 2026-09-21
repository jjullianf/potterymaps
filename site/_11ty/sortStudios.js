// Gemeinsame Sortierlogik fuer Studio-Listings (Homepage "Studios entdecken",
// Studio-Liste je Staedte-Seite): Featured zuerst (Grundlage fuer kuenftige
// kostenpflichtige Featured-Listings), danach Studios mit eigenen Bildern vor
// Studios ohne eigene Bilder (reine Stockfoto-/Platzhalter-Eintraege), danach
// alphabetisch innerhalb jeder Gruppe.
function compareStudiosForListing(a, b) {
  const featuredA = a.featured ? 1 : 0;
  const featuredB = b.featured ? 1 : 0;
  if (featuredA !== featuredB) return featuredB - featuredA;

  const imageA = a.images && a.images.length ? 1 : 0;
  const imageB = b.images && b.images.length ? 1 : 0;
  if (imageA !== imageB) return imageB - imageA;

  return (a.name || "").localeCompare(b.name || "", "de");
}

module.exports = compareStudiosForListing;
