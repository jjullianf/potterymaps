// Daten fuer die Stadt-Ratgeber "Keramik bemalen in [Stadt]" (ch/blog/city-guide.njk).
// Alles Zahlenmaessige und Studio-bezogene (Namen, Preise, Reservation, Umgebung,
// FAQ-Antworten) wird hier live aus studios.json abgeleitet, damit die Artikel nach
// Aenderungen im Editor ohne manuelle Pflege stimmen. Nur die kurze Stadt-
// Charakterisierung (FLAVOR) ist redaktioneller Text.
const studiosFn = require("./studios.js");
const targetCities = require("./targetCities.js");
const { haversineKm } = require("./geo.js");
const compareStudiosForListing = require("../_11ty/sortStudios.js");

const GUIDE_CITIES = ["Zürich", "Basel", "Bern", "Luzern", "Winterthur", "St. Gallen"];
const NEARBY_RADIUS_KM = 30;
const MAX_NEARBY = 8;

const FLAVOR = {
  "Zürich": "Zürich bietet als grösste Stadt der Schweiz die breiteste Auswahl an Studios.",
  "Basel": "Basel hat eine überschaubare, aber vielfältige Auswahl an Keramik-Studios.",
  "Bern": "In der Bundesstadt Bern und ihrer Agglomeration gibt es mehrere Studios zum Keramik bemalen.",
  "Luzern": "Luzern verbindet die Altstadt am See mit mehreren Studios zum Keramik bemalen.",
  "Winterthur": "Winterthur, die Kunststadt im Zürcher Umland, hat eigene Studios zum Keramik bemalen.",
  "St. Gallen": "In St. Gallen und der Ostschweiz ist die Auswahl kleiner, aber es gibt gute Studios in Reichweite.",
};

const SUITABLE_LABELS = [
  ["kids-friendly", "Kinder"],
  ["birthday-parties", "Geburtstage"],
  ["hen-party", "Junggesellinnenabschiede"],
  ["corporate-events", "Firmenevents"],
  ["date-night", "Date-Night"],
];

function slugFor(name) {
  return targetCities.find((c) => c.name === name).slug;
}

function joinList(items) {
  if (items.length <= 1) return items.join("");
  return items.slice(0, -1).join(", ") + " und " + items[items.length - 1];
}

function shortName(name) {
  return String(name || "").split(/\s[|–—]\s|\s-\s/)[0].trim();
}

function lowestNumber(str) {
  const m = String(str || "").match(/\d+(?:[.,]\d+)?/g);
  return m ? Math.min(...m.map((x) => Number(x.replace(",", ".")))) : null;
}

function fmt(v) {
  return Number.isInteger(v) ? String(v) : v.toFixed(2);
}

function median(nums) {
  const a = nums.slice().sort((x, y) => x - y);
  return a[Math.floor(a.length / 2)];
}

function isCafe(s) {
  return /caf[eé]/i.test(String(s.name || "")) || /(Creative|Keramik-?|Ceramic-?|Mal-?)\s?Caf[eé]/i.test(String(s.description || ""));
}

function reservationLabel(tags) {
  const walk = tags.includes("walk-in");
  const only = tags.includes("reservation-only");
  const rec = tags.includes("reservation-empfohlen");
  if (walk && rec) return "Walk-in, Reservation empfohlen";
  if (walk) return "Walk-in";
  if (only) return "Nur mit Reservation";
  if (rec) return "Reservation empfohlen";
  return "–";
}

function suitableFor(tags) {
  return SUITABLE_LABELS.filter(([t]) => tags.includes(t)).map(([, l]) => l);
}

// Kurzbeschreibung aus strukturierten Feldern (nicht aus dem Freitext kopiert).
function blurb(s) {
  const tags = s.tagsArray || [];
  const parts = [];
  const kind = isCafe(s) ? "Keramik-Café" : "Malstudio";
  const extras = [];
  if (tags.includes("pottery-wheel")) extras.push("Töpferscheibe");
  if (/porzellan/i.test(s.description || "")) extras.push("Porzellanmalerei");
  parts.push(
    `${shortName(s.name)} ist ein ${kind}${extras.length ? " mit " + joinList(extras) : ""}. Adresse: ${s.address}.`
  );

  const price = [];
  if (s.price_from) price.push(`Einstieg ab CHF ${s.price_from}`);
  const mug = lowestNumber(s.price_mug);
  const plate = lowestNumber(s.price_plate);
  if (mug) price.push(`Tasse ab CHF ${mug}`);
  if (plate) price.push(`Teller ab CHF ${plate}`);
  if (price.length) parts.push(`Preise: ${price.join(", ")}.`);

  const res = reservationLabel(tags);
  const resText = {
    "Walk-in": "Du kannst spontan ohne Reservation vorbeikommen.",
    "Walk-in, Reservation empfohlen": "Spontan vorbeikommen ist möglich, eine Reservation wird empfohlen.",
    "Nur mit Reservation": "Ein Besuch ist nur mit Reservation möglich.",
    "Reservation empfohlen": "Eine Reservation wird empfohlen.",
  }[res];
  if (resText) parts.push(resText);

  const suit = suitableFor(tags);
  if (suit.length) parts.push(`Geeignet für ${joinList(suit)}.`);

  const pickup = String(s.pickup_time || "").trim().replace(/\.$/, "");
  if (pickup && pickup.length <= 45) parts.push(`Abholzeit: ${pickup}.`);
  return parts.join(" ");
}

function toEntry(s) {
  const tags = s.tagsArray || [];
  return {
    name: s.name,
    shortName: shortName(s.name),
    slug: s.slug,
    city: s.city,
    address: s.address,
    priceFrom: s.price_from || "",
    reservationLabel: reservationLabel(tags),
    suitable: suitableFor(tags).join(", ") || "–",
    isCafe: isCafe(s),
    blurb: blurb(s),
  };
}

module.exports = async function () {
  const studios = await studiosFn();

  return GUIDE_CITIES.map((name, index) => {
    const slug = slugFor(name);
    const hub = targetCities.find((c) => c.name === name);
    const inCity = studios.filter((s) => s.city === name).sort(compareStudiosForListing);
    const entries = inCity.map(toEntry);
    const cafes = entries.filter((e) => e.isCafe);

    const nearby = studios
      .filter((s) => !GUIDE_CITIES.includes(s.city) && s.lat && s.lng)
      .map((s) => ({ s, km: haversineKm(hub.lat, hub.lng, s.lat, s.lng) }))
      .filter((x) => x.km <= NEARBY_RADIUS_KM)
      .sort((a, b) => a.km - b.km)
      .slice(0, MAX_NEARBY)
      .map(({ s, km }) => Object.assign(toEntry(s), { km: Math.max(1, Math.round(km)) }));

    const n = inCity.length;
    const withTag = (t) => inCity.filter((s) => (s.tagsArray || []).includes(t));
    const walkIn = withTag("walk-in");
    const onlyRes = withTag("reservation-only");
    const recommended = withTag("reservation-empfohlen").filter((s) => !s.tagsArray.includes("walk-in"));
    const kids = withTag("kids-friendly");
    const birthdays = withTag("birthday-parties");
    const corporate = withTag("corporate-events");
    const hen = withTag("hen-party");

    const prices = inCity.map((s) => Number(s.price_from)).filter((v) => v > 0);
    const minP = prices.length ? Math.min(...prices) : null;
    const maxP = prices.length ? Math.max(...prices) : null;
    const medP = prices.length ? median(prices) : null;
    const mugs = inCity.map((s) => lowestNumber(s.price_mug)).filter(Boolean);

    const weeks = [];
    inCity.forEach((s) => {
      const m = String(s.pickup_time || "").match(/(\d+)(?:\s*[-–]\s*(\d+))?\s*Woche/i);
      if (m) weeks.push(Number(m[1]), Number(m[2] || m[1]));
    });
    const weeksMin = weeks.length ? Math.min(...weeks) : 1;
    const weeksMax = weeks.length ? Math.max(...weeks) : 3;

    const names = (arr) => joinList(arr.map((s) => shortName(s.name)));
    const priceRange = prices.length
      ? `zwischen CHF ${fmt(minP)} und CHF ${fmt(maxP)}` + (prices.length >= 3 ? ` (mittlerer Wert CHF ${fmt(medP)})` : "")
      : "je nach Studio unterschiedlich";
    const nearbyNames = Array.from(new Set(nearby.map((e) => e.city)));

    const intro =
      `In ${name} gibt es aktuell ${n} ${n === 1 ? "Studio" : "Studios"} zum Keramik bemalen` +
      (cafes.length ? `, davon ${cafes.length === 1 ? "eines" : cafes.length} mit Café-Betrieb` : "") +
      (nearby.length ? `, dazu weitere Studios in der Umgebung (bis ca. ${NEARBY_RADIUS_KM} km)` : "") +
      `. ${prices.length ? `Der günstigste Einstiegspreis liegt in ${name} ${priceRange}. ` : ""}` +
      `Beim Keramik bemalen wählst du ein fertig geformtes Stück, bemalst es in rund 2 bis 2,5 Stunden, und das Studio glasiert und brennt es für dich.`;

    const faqs = [];
    faqs.push({
      q: `Was kostet Keramik bemalen in ${name}?`,
      a:
        (prices.length
          ? `Bei den ${n} Studios in ${name} liegt der günstigste Einstiegspreis ${priceRange}. `
          : `Die Preise unterscheiden sich je nach Studio. `) +
        (mugs.length >= 2 ? `Eine Tasse kostet ab ca. CHF ${Math.min(...mugs)} bis CHF ${Math.max(...mugs)}. ` : "") +
        `Farben, Glasur und Brennen sind bei den meisten Studios im Preis inbegriffen, dazu kommt teils eine Studiogebühr pro Person.`,
    });

    let resAnswer;
    if (walkIn.length) {
      resAnswer = `Das hängt vom Studio ab. In ${name} sind ${walkIn.length} von ${n} Studios Walk-in (${names(walkIn)}), dort kannst du spontan ohne Reservation vorbeikommen.`;
    } else {
      resAnswer = `Das hängt vom Studio ab. In ${name} ist aktuell kein Studio als Walk-in gelistet.`;
    }
    if (onlyRes.length) resAnswer += ` ${onlyRes.length} ${onlyRes.length === 1 ? "Studio arbeitet" : "Studios arbeiten"} nur mit Reservation.`;
    if (recommended.length) resAnswer += ` Bei ${recommended.length} ${recommended.length === 1 ? "weiteren Studio wird" : "weiteren Studios wird"} eine Reservation empfohlen.`;
    resAnswer += ` Für Gruppen und an Wochenenden lohnt sich immer eine Reservation.`;
    faqs.push({ q: `Muss man in ${name} reservieren?`, a: resAnswer });

    const groupBits = [];
    if (corporate.length) groupBits.push(`${corporate.length} nennen Firmenevents oder Teamevents`);
    if (hen.length) groupBits.push(`${hen.length} Junggesellinnenabschiede`);
    if (birthdays.length) groupBits.push(`${birthdays.length} Geburtstage`);
    faqs.push({
      q: `Eignet sich Keramik bemalen in ${name} für Gruppen und Firmenevents?`,
      a:
        (groupBits.length
          ? `Ja. Von den ${n} Studios in ${name} ${joinList(groupBits)}. `
          : `Gruppen sind in ${name} nach Absprache mit dem Studio möglich. `) +
        `Fragt früh an, vor allem bei mehr als 6 bis 8 Personen. Über die Event-Anfrage von potterymaps vermitteln wir dich kostenlos an ein passendes Studio.`,
    });

    faqs.push({
      q: `Ist Keramik bemalen in ${name} für Kinder geeignet?`,
      a: kids.length
        ? `Ja. ${kids.length} von ${n} Studios in ${name} sind als kinderfreundlich gekennzeichnet (${names(kids)}), ${birthdays.length ? `${birthdays.length} bieten Geburtstage an. ` : ""}Mindestalter und Begleitpflicht unterscheiden sich je nach Studio, frag bei der Buchung nach.`
        : `Kinder sind je nach Studio willkommen, aktuell ist in ${name} aber kein Studio ausdrücklich als kinderfreundlich gekennzeichnet. Frag beim Studio nach Mindestalter und Begleitpflicht.`,
    });

    if (cafes.length) {
      faqs.push({
        q: `Gibt es Keramik-Cafés in ${name}?`,
        a: `Ja: ${joinList(cafes.map((c) => c.shortName))}. In einem Keramik-Café bemalst du dein Stück und kannst dabei etwas trinken oder essen. Ob Getränke inklusive sind, unterscheidet sich je nach Café.`,
      });
    } else {
      faqs.push({
        q: `Welche Studios gibt es in ${name} und Umgebung?`,
        a:
          `In ${name} selbst: ${n ? joinList(entries.map((e) => e.shortName)) : "aktuell keine gelisteten Studios"}.` +
          (nearby.length ? ` In der Umgebung (bis ca. ${NEARBY_RADIUS_KM} km): ${joinList(nearby.map((e) => `${e.shortName} in ${e.city}`))}.` : ""),
      });
    }

    faqs.push({
      q: "Wann kann ich das bemalte Stück abholen?",
      a: `Nach dem Bemalen wird das Stück glasiert und gebrannt. In ${name} sind laut den Studios rund ${weeksMin === weeksMax ? weeksMin + " Woche" + (weeksMin > 1 ? "n" : "") : weeksMin + " bis " + weeksMax + " Wochen"} üblich. Vor Weihnachten und in den Ferien kann es länger dauern.`,
    });

    return {
      index,
      name,
      slug,
      heroImage: `./images/cities/${slug}.jpg`,
      heroAlt: `Stadtansicht von ${name}`,
      flavor: FLAVOR[name],
      title: `Keramik bemalen in ${name}: Studios, Preise & Tipps | potterymaps`,
      headline: `Keramik bemalen in ${name}: Die Studios im Überblick`,
      description: `Keramik bemalen in ${name}: ${n} Studios im Vergleich${minP ? ` mit Preisen ab CHF ${fmt(minP)}` : ""}, Reservation, Gruppenangebote und Studios in der Umgebung.`,
      teaser: `Alle ${n} Studios in ${name} im Überblick: Preise, Reservation, Gruppenangebote und Studios in der Umgebung.`,
      intro,
      studios: entries,
      cafes,
      nearby,
      nearbyNames,
      radiusKm: NEARBY_RADIUS_KM,
      count: n,
      priceRange,
      faqs,
      otherGuides: GUIDE_CITIES.filter((c) => c !== name).map((c) => ({ name: c, slug: slugFor(c) })),
    };
  });
};
