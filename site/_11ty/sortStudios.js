// Gemeinsame Sortierlogik fuer Studio-Listings (Homepage "Studios entdecken",
// Studio-Liste je Staedte-Seite): Featured zuerst (Grundlage fuer kuenftige
// kostenpflichtige Featured-Listings), danach Studios mit eigenen Bildern vor
// Studios ohne eigene Bilder (reine Stockfoto-/Platzhalter-Eintraege), danach
// alphabetisch innerhalb jeder Gruppe.
function compareBasic(a, b) {
  const featuredA = a.featured ? 1 : 0;
  const featuredB = b.featured ? 1 : 0;
  if (featuredA !== featuredB) return featuredB - featuredA;

  const imageA = a.images && a.images.length ? 1 : 0;
  const imageB = b.images && b.images.length ? 1 : 0;
  if (imageA !== imageB) return imageB - imageA;

  return (a.name || "").localeCompare(b.name || "", "de");
}

// Wie vollstaendig ein Eintrag ist (Preis, Termin, Oeffnungszeiten, Abholzeit
// auf einen Blick + Telefon + eigenes Foto). Fuer die Auswahl der empfohlenen
// Ateliers auf der Startseite: nur Eintraege mit moeglichst allen Angaben.
function completeness(s) {
  const g = s.glance || {};
  return (g.price ? 1 : 0) + (g.termin ? 1 : 0) + (g.hours ? 1 : 0) + (g.pickup ? 1 : 0) + (s.phone ? 1 : 0) + (s.images && s.images.length ? 1 : 0);
}

function compareByCompleteness(a, b) {
  const featuredA = a.featured ? 1 : 0;
  const featuredB = b.featured ? 1 : 0;
  if (featuredA !== featuredB) return featuredB - featuredA;
  const diff = completeness(b) - completeness(a);
  if (diff) return diff;
  return compareBasic(a, b);
}

// Deutsche Ateliers: vollstaendigere Eintraege zuerst (auch in den Stadtlisten).
// Schweizer Ateliers behalten die bisherige Reihenfolge.
function compareStudiosForListing(a, b) {
  if (a.country === "DE" && b.country === "DE") return compareByCompleteness(a, b);
  return compareBasic(a, b);
}

compareStudiosForListing.byCompleteness = compareByCompleteness;
module.exports = compareStudiosForListing;
