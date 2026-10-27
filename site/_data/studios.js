const fs = require("fs");
const path = require("path");
const citySlug = require("./citySlug.js");
const { COUNTRIES, byIso } = require("../_11ty/countries.js");
const neighborMap = require("./neighborMap.js");
const targetCities = require("./targetCities.js");
const studioImage = require("../_11ty/studioImage.js");
const { getImageList } = require("../_11ty/studioImages.js");

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
// CHF wird wie bisher vorangestellt ("CHF 20"), Euro nachgestellt mit Komma ("20,50 €").
function money(currency, amount) {
  return currency === "EUR" ? `${String(amount).replace(/(\d)\.(\d)/g, "$1,$2")} €` : `${currency} ${amount}`;
}

// Nur reine Zahlen/Bereiche ("20", "25-35") bekommen die Waehrung; Freitexte wie
// "CHF 40 bis 2 Stunden" oder "ab 20" bleiben unveraendert, sonst entstehen
// Doppelungen ("CHF CHF 40", "ab CHF ab 20").
const PLAIN_NUMBER = /^\d+(?:[.,]\d+)?(?:\s*[-–]\s*\d+(?:[.,]\d+)?)?$/;
function priceFrom(label, currency, value) {
  const v = String(value).trim();
  if (PLAIN_NUMBER.test(v)) return `${label} ab ${money(currency, v)}`;
  const m = v.match(/^ab\s+(.+)$/i);
  if (m && PLAIN_NUMBER.test(m[1])) return `${label} ab ${money(currency, m[1])}`;
  return `${label} ${v}`;
}
function feeText(currency, value) {
  const v = String(value).trim();
  return PLAIN_NUMBER.test(v) ? `Ateliergebühr ${money(currency, v)}` : `Ateliergebühr: ${v}`;
}

function generateAutoFAQ(s) {
  const faqs = [];
  const name = s.name || "diesem Atelier";
  const city = s.city || "";
  const currency = s.currency || "CHF";
  const hasPrice =
    (s.price_mug && s.price_mug.trim()) ||
    (s.price_plate && s.price_plate.trim()) ||
    (s.studio_fee && s.studio_fee.trim());
  if (hasPrice) {
    let parts = [];
    if (s.price_mug) parts.push(priceFrom("Tasse", currency, s.price_mug));
    if (s.price_plate) parts.push(priceFrom("Teller", currency, s.price_plate));
    if (s.studio_fee) parts.push(feeText(currency, s.studio_fee));
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
    if (tags.includes("walk-in") && !tags.includes("reservation-empfohlen")) {
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
      return `ab ${money(s.currency || "CHF", formatted)}`;
    }
  }
  // studio_fee ist in den Rohdaten oft ein ganzer Beschreibungssatz statt einer
  // reinen Zahl (z.B. "CHF 15 pro Person - 2 Stunden") - unveraendert uebernehmen
  // statt mit "CHF ... Ateliergebühr" zu verfaelschen.
  // Nur echte Gebuehren mit Betrag anzeigen, keine reinen Dauer-/Hinweistexte
  // ("ca. 2 Stunden"); bei mehreren Teilen mit " · " nur den ersten (den Betrag).
  if (s.country !== "DE") return fee || null;
  // Deutschland: nur ein Mindestumsatz ist ein Preis auf einen Blick, reine
  // Studiogebuehren (Pauschale, Malgebuehr, Anmeldegebuehr) nicht. Gruppen- und
  // Eventbetraege ("ab 5 Personen", "Kindergeburtstag") ebenfalls nicht.
  if (fee) {
    for (const part of fee.split(" · ")) {
      if (/(Kindergeburtstag|Event|Gruppe|\bab \d+ Personen)/i.test(part)) continue;
      const m = part.match(/(Mindest\w*umsatz|Mindestabnahme)[^,.(;]*?(?:€|Euro)[^,.(;]*/i);
      if (m && /\d/.test(m[0])) return m[0].trim();
    }
  }
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
  const formatted = Number.isInteger(value) ? value : value.toFixed(2);
  return `ab ${money(s.currency || "CHF", formatted)}`;
}


// ---------- "Auf einen Blick"-Karte der Atelier-Seite ----------
// Vier gleich aufgebaute Felder (Preis, Termin, Öffnungszeiten, Abholzeit) mit je
// einem kurzen Wert und einer kurzen Zusatzzeile. Lange Texte stehen unten in
// "Weitere Infos"; hier wird nur eine gekuerzte Fassung gezeigt.
const DAYS = "(?:Mo|Di|Mi|Do|Fr|Sa|So)";
const HOURS_RE = new RegExp(
  `(${DAYS}(?:\\s*[–-]\\s*${DAYS})?(?:,\\s*${DAYS})*)\\s+(\\d{1,2}[.:]?\\d{0,2}\\s*(?:Uhr)?\\s*[–-]\\s*\\d{1,2}[.:]?\\d{0,2}(?:\\s*Uhr)?(?:\\s*(?:und|,)\\s*\\d{1,2}[.:]?\\d{0,2}\\s*(?:Uhr)?\\s*[–-]\\s*\\d{1,2}[.:]?\\d{0,2})?)`,
  "g"
);
const BY_APPOINTMENT = /(nach|auf)\s+(Terminvereinbarung|Vereinbarung|Absprache|Termin|Anfrage)|nur (zu|nach|mit) Termin|Kurszeiten|Termine?\s+(nach|per|über)/i;

function glanceHours(hours, tags) {
  const h = String(hours || "").trim();
  if (!h) return tags.includes("reservation-only") ? { value: "Nach Buchung", sub: "freie Termine online" } : null;
  const found = [];
  let m;
  HOURS_RE.lastIndex = 0;
  while ((m = HOURS_RE.exec(h)) && found.length < 3) {
    found.push(`${m[1].replace(/\s+/g, " ")} ${m[2].replace(/\s*Uhr/g, "").replace(/\s+/g, " ").trim()}`);
  }
  if (found.length) {
    const more = found.length > 2 || h.length > found.slice(0, 2).join(" ").length + 25;
    const sub = [found[1] || "", more ? "weitere Zeiten unten" : ""].filter(Boolean).join(" · ");
    return { value: found[0], sub };
  }
  if (BY_APPOINTMENT.test(h)) return { value: "Nach Termin", sub: "Zeiten nach Absprache" };
  return null;
}

function glancePickup(pickup) {
  const first = String(pickup || "").split(" · ")[0].trim();
  if (!first) return null;
  const WORDS = { ein: "1", eine: "1", einer: "1", einem: "1", zwei: "2", drei: "3", vier: "4", fünf: "5" };
  const m = first.match(/((?:ca\.?\s*)?(?:\d+(?:\s*[–-]\s*\d+)?|ein(?:e|er|em)?|zwei|drei|vier|fünf)\s*(?:Werktage?|Tage?|Wochen?|Stunden?))/i);
  if (m) {
    const value = m[1].replace(/\s+/g, " ").replace(/^(ca\.?\s*)?(ein(?:e|er|em)?|zwei|drei|vier|fünf)\b/i, (_, ca, w) => `${ca || ""}${WORDS[w.toLowerCase()]}`);
    return { value, sub: "" };
  }
  return null;
}

function glancePrice(s, priceAtAGlance, priceRangeText) {
  const note = String(s.price_note || "").replace(/\b(inkl|ca|bzw|ggf|max|min|zzgl|evtl|ab)\./gi, "$1§");
  const pieces = note.split(/(?<=[.!?])\s+|\s·\s/).map((x) => x.replace(/§/g, ".").trim());
  let sub = (pieces.find((x) => /inkl|enthalten|all[- ]?inclusive/i.test(x) && x.length <= 110) || "").replace(/[.!?]$/, "");
  if (sub.length > 60) sub = sub.split(", ")[0];
  if (sub.length > 70) sub = "";
  if (priceAtAGlance) return { value: priceAtAGlance, sub };
  if (priceRangeText && priceRangeText.length <= 42) return { value: priceRangeText, sub };
  return null;
}

function glanceTermin(tags) {
  if (tags.includes("walk-in")) {
    return { value: "Walk-in möglich", sub: tags.includes("reservation-empfohlen") ? "Reservierung empfohlen" : "ohne Reservierung", green: true };
  }
  if (tags.includes("reservation-empfohlen")) return { value: "Reservierung empfohlen", sub: "Platz vorab sichern", green: false };
  if (tags.includes("reservation-only")) return { value: "Nur mit Reservierung", sub: "Platz vorab buchen", green: false };
  return null;
}

function buildGlance(s, tags, priceAtAGlance, priceRangeText) {
  return {
    price: glancePrice(s, priceAtAGlance, priceRangeText),
    termin: glanceTermin(tags),
    hours: glanceHours(s.opening_hours, tags),
    pickup: glancePickup(s.pickup_time),
  };
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
// die 3 hoechstprioren, tatsaechlich gesetzten Tags eines Ateliers werden gezeigt.
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

// Walk-in-Badge fuers Karten-Popup und die Studio-Detailseite - gleiche
// Prioritaet wie TOP_TAG_PRIORITY: ein Atelier hat immer nur einen dieser
// drei Reservation-Tags gleichzeitig. Icons passend zu TAG_META oben.
const RESERVATION_TAGS = ["walk-in", "reservation-empfohlen", "reservation-only"];
const WALKIN_BADGE = {
  "walk-in": { label: "Walk-in möglich", cls: "walkin", icon: "ti-door-enter" },
  "reservation-empfohlen": { label: "Reservation empfohlen", cls: "empfohlen", icon: "ti-calendar-check" },
  "reservation-only": { label: "Nur Reservation", cls: "only", icon: "ti-lock" },
};

function computeWalkinBadge(tags) {
  if (tags.includes("walk-in")) return WALKIN_BADGE["walk-in"];
  if (tags.includes("reservation-empfohlen")) return WALKIN_BADGE["reservation-empfohlen"];
  if (tags.includes("reservation-only")) return WALKIN_BADGE["reservation-only"];
  return null;
}

function escapeHtml(str) {
  return String(str || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// Fertiges HTML fuer die feste Info-Karte unten auf allen Kartenseiten
// (Startseite, Karte, Stadtseiten, Umgebungs-Seiten) - hier einmal zentral
// gebaut, damit sie ueberall gleich aussieht. Wird als JSON in die Karten-
// Templates eingebettet (siehe js/map-popup.js), daher rohes HTML. Die ganze
// Karte ist ueber den Namenslink anklickbar (::after deckt sie ab), Anrufen
// und Route liegen darueber.
function mapCardBadge(tags) {
  if (tags.includes("walk-in") && tags.includes("reservation-empfohlen")) return { label: "Walk-in & Reservation empfohlen", cls: "mix" };
  if (tags.includes("walk-in")) return { label: "Walk-in", cls: "walkin" };
  if (tags.includes("reservation-empfohlen")) return { label: "Reservation empfohlen", cls: "empfohlen" };
  if (tags.includes("reservation-only")) return { label: "Reservation Pflicht", cls: "only" };
  return null;
}

function buildMapCardHtml(s, { price, tags }) {
  const badge = mapCardBadge(tags);
  const route = "https://www.google.com/maps/dir/?api=1&destination=" + encodeURIComponent((s.address || "") + " " + (s.city || ""));
  const tel = String(s.phone || "").replace(/[^\d+]/g, "");
  return (
    '<div class="map-card-inner">' +
    '<a class="map-card-name" href="' + s.pagePath + '">' + escapeHtml(s.name) + "</a>" +
    '<div class="map-card-meta"><span class="map-card-city">' + escapeHtml(s.city) + "</span>" +
    (price ? '<span class="map-card-price">' + escapeHtml(price) + "</span>" : "") +
    (badge ? '<span class="map-card-badge map-card-badge-' + badge.cls + '">' + badge.label + "</span>" : "") +
    "</div>" +
    '<div class="map-card-actions"><span class="map-card-btn map-card-btn-primary">Details</span>' +
    (tel ? '<a class="map-card-btn" href="tel:' + tel + '">Anrufen</a>' : "") +
    '<a class="map-card-btn" href="' + route + '" target="_blank" rel="noopener">Route</a></div>' +
    "</div>"
  );
}

// Land pro Atelier (studios.json, Feld "country"); fehlt es, gilt "CH" - so
// bleiben alle bisherigen Eintraege automatisch Schweizer Ateliers.
const DEFAULT_COUNTRY = "CH";

function normalizeCountry(s) {
  return String(s.country || DEFAULT_COUNTRY).trim().toUpperCase();
}

// Liefert nur die Ateliers des angegebenen Landes. Ohne Argument (so ruft
// Eleventy die globale Datei "studios" auf) bleibt es bei der Schweiz, damit
// ein deutsches Atelier in studios.json nie auf Schweizer Seiten, in Karten,
// Zaehlern, Sitemap oder "in der Naehe"-Seiten auftaucht. Fuer den /de/-Teil
// spaeter: require("./studios.js").forCountry("DE").
const studiosCache = new Map();

function loadStudios(country) {
  // Mehrere Daten-Module (Staedte, Umgebung, Statistik, Laender-Daten) brauchen
  // dieselben Ateliers - pro Land und Dateistand nur einmal berechnen.
  const mtime = fs.statSync(STUDIOS_JSON_PATH).mtimeMs;
  const hit = studiosCache.get(country);
  if (hit && hit.mtime === mtime) return hit.promise;
  const promise = buildStudios(country);
  studiosCache.set(country, { mtime, promise });
  return promise;
}

async function buildStudios(country) {
  const raw = JSON.parse(fs.readFileSync(STUDIOS_JSON_PATH, "utf-8"));
  const studios = (raw.studios || [])
    .map((s) => {
      const c = normalizeCountry(s);
      const cfg = byIso(c) || COUNTRIES.ch;
      return Object.assign({}, s, {
        country: c,
        currency: s.currency || cfg.currency,
        pagePath: `${cfg.path}/studio/${s.slug}/`,
        countryConfig: cfg,
      });
    })
    .filter((s) => s.country === country);

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
    // Jeder Ort mit mind. einem Atelier bekommt eine eigene Seite - "targetCity"
    // ist daher immer der eigene Ort. "nearestHub" bleibt fuer Faelle relevant, in
    // denen auf die naechste der 20 garantierten Staedte verwiesen wird (z.B.
    // Fallback fuer "Aehnliche Ateliers" bei Orten mit nur einem Atelier).
    const isHub = targetSlugSet.has(cSlug);
    const nearestHubName = isHub ? cityName : neighborMap[cityName] || cityName;
    const nearestHubSlug = citySlug(nearestHubName);

    const priceRangeText = computePriceRangeText(s);
    const priceAtAGlance = formatPriceFrom(s);
    const priceIncludes = s.price_note ? truncate(s.price_note.trim(), 60) : null;

    const topTags = computeTopTags(tags);

    // Bilderliste (siehe _11ty/studioImages.js) - erstes Element ist das
    // Hauptbild und ersetzt/normalisiert das alte einzelne "image"-Feld ueberall
    // unten (Karten, Sortierung nach "hat Bild", og:image etc.), auch fuer
    // Ateliers, die noch das alte Format haben.
    const imageList = getImageList(s);
    const mainImage = imageList[0] || "";
    const galleryImages = imageList.slice(1);
    const studioForImage = Object.assign({}, s, { image: mainImage });

    // Vorberechnet statt als async Shortcode direkt im studio-card.njk-Macro
    // aufgerufen - async Shortcodes liefern innerhalb eines Nunjucks-Macros
    // keinen Output (bekannte Einschraenkung), daher wird das fertige
    // <picture>/Platzhalter-HTML hier einmalig erzeugt und mitgegeben.
    const cardThumbHtml = await studioImage(studioForImage, {
      widths: [400],
      sizes: "400px",
      loading: "lazy",
      wrapClass: "studio-card-thumb",
    });

    const mapPopupHtml = buildMapCardHtml(s, { price: priceAtAGlance, tags });
    const mapPopupHtmlCompact = mapPopupHtml;

    // hat_instagram steht als "ja, https://www.instagram.com/<handle>/" (oder
    // "nein"/leer) - daraus Link und @handle fuer die Detailseite ziehen.
    const igMatch = String(s.hat_instagram || "").match(/https?:\/\/(?:www\.)?instagram\.com\/([A-Za-z0-9._]+)/i);
    const instagramHandle = igMatch ? igMatch[1] : null;
    const instagramUrl = instagramHandle ? `https://www.instagram.com/${instagramHandle}/` : null;

    return Object.assign({}, s, {
      instagramHandle,
      instagramUrl,
      tagsArray: tags,
      tagsObjects: toTagObjects(tags),
      // Fuer die Detailseite: Walk-in/Reservation als eigene hervorgehobene
      // Zeile statt normalem Tag, daher hier aus der uebrigen Tag-Liste
      // entfernt (siehe .studio-walkin-badge in ch/studio.njk).
      tagsObjectsNoWalkin: toTagObjects(tags.filter((t) => !RESERVATION_TAGS.includes(t))),
      walkinBadge: computeWalkinBadge(tags),
      topTags,
      topTagsObjects: toTagObjects(topTags),
      priceRangeText,
      priceRangeShort: truncate(priceRangeText, 42),
      priceAtAGlance,
      priceIncludes,
      glance: buildGlance(s, tags, priceAtAGlance, priceRangeText),
      faqs,
      citySlug: cSlug,
      targetCityName: cityName,
      targetCitySlug: cSlug,
      isHub,
      nearestHubName,
      nearestHubSlug,
      cardThumbHtml,
      mapPopupHtml,
      mapPopupHtmlCompact,
      image: mainImage,
      images: imageList,
      galleryImages,
      featured: s.featured === true || s.featured === "true",
    });
  }));
}

module.exports = async function () {
  return loadStudios(DEFAULT_COUNTRY);
};
module.exports.forCountry = loadStudios;
