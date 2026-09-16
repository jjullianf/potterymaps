const fs = require("fs");
const path = require("path");
const citySlug = require("./citySlug.js");
const neighborMap = require("./neighborMap.js");
const targetCities = require("./targetCities.js");
const studioImage = require("../_11ty/studioImage.js");

const STUDIOS_JSON_PATH = path.join(
  __dirname,
  "..",
  "..",
  "editor-server",
  "data",
  "studios.json"
);

const targetSlugSet = new Set(targetCities.map((c) => c.slug));

// Exakt portierte Logik aus editor-server/public/index.html (generateAutoFAQ / getCustomFaq),
// damit die FAQ auf der oeffentlichen Seite identisch zum Editor ist.
function generateAutoFAQ(s) {
  const faqs = [];
  const name = s.name || "diesem Studio";
  const city = s.city || "";
  const hasPrice =
    (s.price_mug && s.price_mug.trim()) ||
    (s.price_plate && s.price_plate.trim()) ||
    (s.studio_fee && s.studio_fee.trim());
  if (hasPrice) {
    let parts = [];
    if (s.price_mug) parts.push("Tasse ab CHF " + s.price_mug);
    if (s.price_plate) parts.push("Teller ab CHF " + s.price_plate);
    if (s.studio_fee) parts.push("Studiogebühr CHF " + s.studio_fee);
    let answer =
      "Bei " + name + (city ? " in " + city : "") + " kostet " + parts.join(", ") + ".";
    if (s.price_note) answer += " " + s.price_note;
    faqs.push({ q: "Wie viel kostet Keramik bemalen bei " + name + "?", a: answer });
  }
  if (s.pickup_time && s.pickup_time.trim()) {
    faqs.push({
      q: "Wie lange dauert es, bis ich das gebrannte Stück bei " + name + " abholen kann?",
      a:
        "Nach dem Brennen ist das bemalte Stück bei " +
        name +
        " normalerweise nach " +
        s.pickup_time +
        " abholbereit.",
    });
  }
  const tags = (s.tags || "").split(",").map((t) => t.trim());
  if (
    tags.includes("walk-in") ||
    tags.includes("reservation-empfohlen") ||
    tags.includes("reservation-only")
  ) {
    let answer;
    if (tags.includes("walk-in")) {
      answer = "Spontanes Vorbeikommen ist möglich, keine Reservation nötig.";
    } else if (tags.includes("reservation-empfohlen")) {
      answer =
        "Spontanes Vorbeikommen ist möglich, eine Reservation wird aber empfohlen, besonders an Wochenenden/zu Stosszeiten.";
    } else {
      answer = "Eine Reservation ist notwendig, spontanes Vorbeikommen ist hier nicht vorgesehen.";
    }
    faqs.push({ q: "Muss ich bei " + name + " reservieren, um Keramik zu bemalen?", a: answer });
  }
  if (tags.includes("kids-friendly")) {
    faqs.push({
      q: "Ist " + name + " für Kinder geeignet?",
      a:
        name +
        " ist für Kinder geeignet" +
        (tags.includes("birthday-parties")
          ? " und bietet auch Kindergeburtstage mit Keramik bemalen an."
          : " zum Keramik bemalen."),
    });
  }
  if (s.special_events && s.special_events.trim()) {
    faqs.push({ q: "Welche besonderen Events bietet " + name + " an?", a: s.special_events });
  }
  return faqs;
}

function getCustomFaq(s) {
  try {
    return JSON.parse(s.custom_faq || "[]");
  } catch (e) {
    return [];
  }
}

// price_mug/price_plate sind manchmal selbst Bereiche (z.B. "20-46" statt "35"),
// daher genuegt kein simples String-Zusammensetzen ("CHF 20-46–20-68" waere
// unlesbar) - stattdessen wird die niedrigste enthaltene Zahl herausgesucht.
function extractLowestNumber(str) {
  if (!str) return null;
  const matches = str.match(/\d+(?:\.\d+)?/g);
  if (!matches) return null;
  return Math.min(...matches.map(Number));
}

function computePriceRangeText(s) {
  const mug = s.price_mug && s.price_mug.trim();
  const plate = s.price_plate && s.price_plate.trim();
  const fee = s.studio_fee && s.studio_fee.trim();
  if (mug || plate) {
    const numbers = [extractLowestNumber(mug), extractLowestNumber(plate)].filter(
      (n) => n !== null
    );
    if (numbers.length) {
      const lowest = Math.min(...numbers);
      const formatted = Number.isInteger(lowest) ? lowest : lowest.toFixed(2).replace(/\.?0+$/, "");
      return `ab CHF ${formatted}`;
    }
  }
  // studio_fee ist in den Rohdaten oft ein ganzer Beschreibungssatz statt einer
  // reinen Zahl (z.B. "CHF 15 pro Person - 2 Stunden") - unveraendert uebernehmen
  // statt mit "CHF ... Studiogebühr" zu verfaelschen.
  if (fee) return fee;
  return null;
}

// "Preis auf einen Blick": liest NUR noch das feste, manuell befuellte Feld
// price_from (siehe scripts/set-price-from.js) - keine Text-/Mustersuche mehr zur
// Laufzeit, da diese wiederholt falsche Werte lieferte (Zuschlaege, Dauerangaben
// etc. wurden faelschlich als Preis erkannt).
function formatPriceFrom(s) {
  if (s.price_from === null || s.price_from === undefined || s.price_from === "") return null;
  const value = Number(s.price_from);
  if (Number.isNaN(value)) return null;
  const formatted = Number.isInteger(value) ? value : value.toFixed(2).replace(/\.?0+$/, "");
  return `ab CHF ${formatted}`;
}

// Woerter/Zeichen, die alleinstehend am Ende einer gekuerzten Kartenzeile
// wie ein Abbruch mitten im Sinn wirken (z.B. ein "CHF" ohne folgende Zahl) -
// werden nach dem Kuerzen zusaetzlich entfernt.
const DANGLING_TRAILING_WORDS = new Set(["CHF", "ab", "Ab", "bis", "für", "und", "·", "+", "-", "je", "ca.", "ca"]);

function truncate(text, maxLen) {
  if (!text || text.length <= maxLen) return text;
  const cut = text.slice(0, maxLen);
  const lastSpace = cut.lastIndexOf(" ");
  const trimmed = lastSpace > 20 ? cut.slice(0, lastSpace) : cut;
  const words = trimmed.trim().split(/\s+/);
  while (words.length > 1 && DANGLING_TRAILING_WORDS.has(words[words.length - 1])) {
    words.pop();
  }
  return words.join(" ") + "…";
}

// Fuer die kompakte Kartenansicht (Stadtseiten, Startseite) werden die
// entscheidungsrelevantesten Tags zuerst gezeigt, in dieser festen Prioritaet -
// die 3 hoechstprioren, tatsaechlich gesetzten Tags eines Studios werden gezeigt.
const TOP_TAG_PRIORITY = [
  "walk-in",
  "reservation-empfohlen",
  "reservation-only",
  "kids-friendly",
  "date-night",
  "other-crafts",
  "birthday-parties",
  "corporate-events",
  "hen-party",
  "themed-events",
  "at-home-kits",
  "pottery-wheel",
];

function computeTopTags(tags) {
  const prioritized = TOP_TAG_PRIORITY.filter((t) => tags.includes(t));
  const rest = tags.filter((t) => !prioritized.includes(t));
  return prioritized.concat(rest).slice(0, 3);
}

// Kategorie + Icon (tabler-icons) je Tag, fuer farbige Pillen statt einheitlichem Grau.
const TAG_META = {
  "kids-friendly": { category: "terracotta", icon: "ti-baby-carriage" },
  "birthday-parties": { category: "terracotta", icon: "ti-cake" },
  "walk-in": { category: "gold", icon: "ti-door-enter" },
  "reservation-empfohlen": { category: "blue", icon: "ti-calendar-check" },
  "reservation-only": { category: "blue", icon: "ti-lock" },
  "corporate-events": { category: "violet", icon: "ti-building" },
  "hen-party": { category: "violet", icon: "ti-glass-champagne" },
  "date-night": { category: "violet", icon: "ti-heart" },
  "pottery-wheel": { category: "green", icon: "ti-wheel" },
  "other-crafts": { category: "green", icon: "ti-palette" },
  "at-home-kits": { category: "green", icon: "ti-package" },
  "themed-events": { category: "green", icon: "ti-confetti" },
};

// Interner (englischer) Wert bleibt fuers Filtern/die Daten massgeblich - nur die
// Anzeige wird uebersetzt.
const TAG_LABELS = {
  "kids-friendly": "Kinderfreundlich",
  "birthday-parties": "Geburtstage",
  "hen-party": "Junggesellinnenabschied",
  "corporate-events": "Firmenevents",
  "date-night": "Date-Night",
  "walk-in": "Walk-in",
  "reservation-empfohlen": "Reservation empfohlen",
  "reservation-only": "Nur mit Reservation",
  "at-home-kits": "Kits zum Mitnehmen",
  "pottery-wheel": "Töpferscheibe",
  "other-crafts": "Weitere Kreativangebote",
  "themed-events": "Themen-Abende",
};

function toTagObjects(tags) {
  return tags.map((name) => {
    const meta = TAG_META[name] || { category: "neutral", icon: "ti-tag" };
    return { name, label: TAG_LABELS[name] || name, category: meta.category, icon: meta.icon };
  });
}

module.exports = async function () {
  const raw = JSON.parse(fs.readFileSync(STUDIOS_JSON_PATH, "utf-8"));
  const studios = raw.studios || [];

  return Promise.all(studios.map(async (s) => {
    const tags = (s.tags || "")
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean);

    const autoFaqs = generateAutoFAQ(s);
    const customFaqs = getCustomFaq(s);
    const faqs = autoFaqs.concat(customFaqs.filter((f) => f.q && f.a));

    const cityName = s.city || "";
    const cSlug = citySlug(cityName);
    // Jeder Ort mit mind. einem Studio bekommt eine eigene Seite - "targetCity"
    // ist daher immer der eigene Ort. "nearestHub" bleibt fuer Faelle relevant, in
    // denen auf die naechste der 20 garantierten Staedte verwiesen wird (z.B.
    // Fallback fuer "Aehnliche Studios" bei Orten mit nur einem Studio).
    const isHub = targetSlugSet.has(cSlug);
    const nearestHubName = isHub ? cityName : neighborMap[cityName] || cityName;
    const nearestHubSlug = citySlug(nearestHubName);

    const priceRangeText = computePriceRangeText(s);
    const priceAtAGlance = formatPriceFrom(s);
    const priceIncludes = s.price_note ? truncate(s.price_note.trim(), 60) : null;

    const topTags = computeTopTags(tags);

    // Vorberechnet statt als async Shortcode direkt im studio-card.njk-Macro
    // aufgerufen - async Shortcodes liefern innerhalb eines Nunjucks-Macros
    // keinen Output (bekannte Einschraenkung), daher wird das fertige
    // <picture>/Platzhalter-HTML hier einmalig erzeugt und mitgegeben.
    const cardThumbHtml = await studioImage(s, {
      widths: [400],
      sizes: "400px",
      loading: "lazy",
      wrapClass: "studio-card-thumb",
    });

    return Object.assign({}, s, {
      tagsArray: tags,
      tagsObjects: toTagObjects(tags),
      topTags,
      topTagsObjects: toTagObjects(topTags),
      priceRangeText,
      priceRangeShort: truncate(priceRangeText, 42),
      priceAtAGlance,
      priceIncludes,
      faqs,
      citySlug: cSlug,
      targetCityName: cityName,
      targetCitySlug: cSlug,
      isHub,
      nearestHubName,
      nearestHubSlug,
      cardThumbHtml,
    });
  }));
};
