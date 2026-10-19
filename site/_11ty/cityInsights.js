// Datengetriebene SEO-/Mehrwert-Bausteine fuer Stadtseiten (derzeit nur Deutschland,
// siehe country.richCityPages): Kennzahlen, Vergleichstabelle, FAQ und Metatexte.
// Alle Aussagen werden aus den Atelier-Daten abgeleitet, nichts wird frei erfunden.
const pluralize = require("./pluralize.js");

const eur = (n) => `${String(Number.isInteger(n) ? n : n.toFixed(2)).replace(".", ",")} €`;
const names = (list, max = 6) => {
  const n = list.slice(0, max).map((s) => s.name);
  const more = list.length - n.length;
  const txt = n.length > 1 ? `${n.slice(0, -1).join(", ")} und ${n[n.length - 1]}` : n[0] || "";
  return more > 0 ? `${txt} sowie ${more} weitere` : txt;
};
const has = (s, tag) => (s.tagsArray || []).includes(tag);
const opensSunday = (s) => /(?:^|[\s,–])So\s+\d/.test(s.opening_hours || "");
const firstSentence = (t) => String(t || "").split(" · ")[0].replace(/\s+$/, "");

function bookingLabel(s) {
  if (has(s, "reservation-only")) return "Nur mit Reservierung";
  if (has(s, "walk-in") && has(s, "reservation-empfohlen")) return "Walk-in, Reservierung empfohlen";
  if (has(s, "walk-in")) return "Walk-in möglich";
  if (has(s, "reservation-empfohlen")) return "Reservierung empfohlen";
  return "";
}

function buildCityInsights(city, otherCities) {
  const list = city.direct || [];
  const n = list.length;
  if (!n) return null;
  const name = city.name;
  const atelierWord = (k) => pluralize(k, "Atelier", "Ateliers");

  const priced = list
    .map((s) => ({ s, p: Number(s.price_from) }))
    .filter((x) => x.s.price_from !== "" && !Number.isNaN(x.p) && x.p > 0)
    .sort((a, b) => a.p - b.p);
  const walkin = list.filter((s) => has(s, "walk-in"));
  const only = list.filter((s) => has(s, "reservation-only"));
  const empf = list.filter((s) => has(s, "reservation-empfohlen"));
  const kids = list.filter((s) => has(s, "kids-friendly"));
  const birthday = list.filter((s) => has(s, "birthday-parties"));
  const hen = list.filter((s) => has(s, "hen-party"));
  const corp = list.filter((s) => has(s, "corporate-events"));
  const cafes = list.filter((s) => /café|cafe/i.test(s.description || ""));
  const sunday = list.filter(opensSunday);
  const noFee = list.filter((s) => /keine (separate )?(studio|tisch|malplatz|mal)gebühr/i.test(s.studio_fee || ""));
  const minSpend = list.filter((s) => /mindest/i.test(`${s.studio_fee || ""} ${s.price_note || ""}`));

  // Kennzahlen als Aufzaehlung "Auf einen Blick"
  const facts = [];
  facts.push(`${n} ${atelierWord(n)} in ${name}`);
  if (priced.length) facts.push(`Preise ab ${eur(priced[0].p)} (${priced[0].s.name})`);
  if (noFee.length) facts.push(`${noFee.length} von ${n} ohne separate Studiogebühr`);
  if (walkin.length) facts.push(`${walkin.length} mit Walk-in ohne Termin`);
  if (only.length) facts.push(`${only.length} nur mit Reservierung`);
  if (birthday.length) facts.push(`${birthday.length} für Kindergeburtstage`);
  if (hen.length) facts.push(`${hen.length} für Junggesellinnenabschiede`);
  if (corp.length) facts.push(`${corp.length} für Firmenevents`);
  if (sunday.length) facts.push(`${sunday.length} sonntags geöffnet`);

  // Vergleichstabelle
  const table = list.map((s) => ({
    name: s.name,
    url: `${s.countryConfig.path}/studio/${s.slug}/`,
    price: s.price_from !== "" && !Number.isNaN(Number(s.price_from)) ? `ab ${eur(Number(s.price_from))}` : "",
    booking: bookingLabel(s),
    kids: has(s, "kids-friendly") || has(s, "birthday-parties") ? "ja" : "",
    groups: [has(s, "hen-party") ? "JGA" : "", has(s, "corporate-events") ? "Firmenevent" : ""].filter(Boolean).join(", "),
  }));

  // FAQ (reiner Text, auch fuer FAQPage-JSON-LD)
  const faqs = [];
  if (priced.length) {
    let a = `Keramik bemalen kostet in ${name} ab ${eur(priced[0].p)} pro Stück (${priced[0].s.name}).`;
    if (noFee.length) a += ` ${noFee.length} von ${n} ${atelierWord(n)} berechnen keine separate Studiogebühr, bezahlt wird nur das gewählte Keramikstück.`;
    if (minSpend.length) a += ` ${minSpend.length === 1 ? "Ein Atelier verlangt" : `${minSpend.length} Ateliers verlangen`} einen Mindestumsatz pro Person.`;
    a += " Farben, Glasur und Brand sind bei den meisten Ateliers im Preis enthalten, Details stehen auf den einzelnen Atelier-Seiten.";
    faqs.push({ q: `Was kostet Keramik bemalen in ${name}?`, a });
  }
  if (walkin.length || only.length || empf.length) {
    const parts = [];
    if (walkin.length) parts.push(`Ohne Termin vorbeikommen ist laut Angabe der Ateliers möglich bei ${names(walkin, 4)}.`);
    if (empf.length) parts.push(`Eine Reservierung wird empfohlen bei ${names(empf, 4)}.`);
    if (only.length) parts.push(`Nur mit Reservierung geht es bei ${names(only, 4)}.`);
    faqs.push({ q: `Muss ich in ${name} für Keramik bemalen reservieren?`, a: parts.join(" ") });
  }
  if (birthday.length) {
    faqs.push({
      q: `Wo kann ich in ${name} einen Kindergeburtstag mit Keramik bemalen feiern?`,
      a: `Kindergeburtstage mit Keramik bemalen bieten in ${name} ${names(birthday, 6)} an. Altersgrenzen, Preise pro Kind und Gruppengrößen stehen auf den jeweiligen Atelier-Seiten.`,
    });
  }
  if (hen.length || corp.length) {
    const p = [];
    if (hen.length) p.push(`Für Junggesellinnenabschiede nennen ${names(hen, 5)} ein Angebot.`);
    if (corp.length) p.push(`Firmenevents und Teamevents bieten ${names(corp, 5)} an.`);
    faqs.push({ q: `Wo kann ich in ${name} Keramik bemalen mit einer Gruppe, zum JGA oder als Teamevent?`, a: p.join(" ") });
  }
  const withPickup = list.filter((s) => s.pickup_time);
  if (withPickup.length) {
    const ex = withPickup.slice(0, 3).map((s) => `${s.name}: ${firstSentence(s.pickup_time)}`).join("; ");
    faqs.push({
      q: `Wie lange dauert es, bis die bemalte Keramik in ${name} fertig ist?`,
      a: `Nach dem Bemalen glasiert und brennt das Atelier dein Stück. Die Wartezeit unterscheidet sich je nach Atelier, zum Beispiel ${ex}. Die genaue Abholzeit steht auf der jeweiligen Atelier-Seite.`,
    });
  }
  if (sunday.length) {
    faqs.push({ q: `Wo kann ich in ${name} am Sonntag Keramik bemalen?`, a: `Sonntags geöffnet sind laut Öffnungszeiten ${names(sunday, 6)}. Prüfe vor dem Besuch die aktuellen Zeiten auf der Atelier-Seite oder beim Atelier.` });
  }

  // Metatexte
  const title = n === 1 ? `Keramik bemalen in ${name}: Atelier, Preise & Öffnungszeiten | potterymaps` : `Keramik bemalen in ${name}: ${n} ${atelierWord(n)}, Preise & Öffnungszeiten | potterymaps`;
  const bits = [n === 1 ? "1 Atelier" : `${n} ${atelierWord(n)} im Vergleich`];
  if (priced.length) bits.push(`ab ${eur(priced[0].p)}`);
  if (walkin.length) bits.push("Walk-in");
  if (birthday.length) bits.push("Kindergeburtstag");
  let description = `Keramik bemalen in ${name}: ${bits.join(", ")} – mit Preisen, Öffnungszeiten, Karte und Tipps für Gruppen und Events.`;
  if (description.length > 158) description = `Keramik bemalen in ${name}: ${n === 1 ? "Atelier" : `${n} ${atelierWord(n)} im Vergleich`} – Preise, Öffnungszeiten, Karte und Tipps für Gruppen und Events.`;

  // Dynamischer Absatz zur Intro
  let summary = `potterymaps listet aktuell ${n} ${atelierWord(n)} zum Keramik bemalen in ${name}`;
  if (priced.length) summary += n === 1 ? `, Preise ab ${eur(priced[0].p)}` : `, die Preise beginnen bei ${eur(priced[0].p)}`;
  summary += ".";
  if (n === 1) summary += walkin.length ? " Du kannst dort ohne Termin vorbeikommen." : only.length ? " Das Atelier arbeitet nur mit Reservierung." : "";
  else if (walkin.length && only.length) summary += ` Bei ${walkin.length} ${pluralize(walkin.length, "Atelier", "Ateliers")} kannst du ohne Termin vorbeikommen, ${only.length} ${pluralize(only.length, "arbeitet", "arbeiten")} nur mit Reservierung.`;
  else if (only.length === n) summary += " Alle Ateliers arbeiten nur mit Reservierung, buche also vorab.";
  else if (walkin.length) summary += ` Bei ${walkin.length} ${pluralize(walkin.length, "Atelier", "Ateliers")} kannst du ohne Termin vorbeikommen.`;

  return {
    facts,
    table,
    faqs,
    title,
    description,
    summary,
    jsonLdFaq: faqs.length
      ? {
          "@context": "https://schema.org",
          "@type": "FAQPage",
          mainEntity: faqs.map((f) => ({ "@type": "Question", name: f.q, acceptedAnswer: { "@type": "Answer", text: f.a } })),
        }
      : null,
    otherCities: (otherCities || []).filter((o) => o.slug !== city.slug).slice(0, 12),
  };
}

module.exports = { buildCityInsights };
