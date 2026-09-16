const citySlug = require("./citySlug.js");

// Die 20 garantierten Staedte, in dieser Reihenfolge angezeigt.
const TARGET_CITY_NAMES = [
  "Zürich", "Genève", "Basel", "Lausanne", "Bern", "Winterthur", "Luzern",
  "St. Gallen", "Lugano", "Biel/Bienne", "Thun", "Köniz", "Fribourg",
  "La Chaux-de-Fonds", "Schaffhausen", "Uster", "Chur", "Vernier", "Sion",
  "Neuchâtel",
];

const INTROS = {
  "Zürich": "Zürich ist die grösste Stadt der Schweiz und bietet gleich mehrere Studios zum Keramik bemalen – ideal für einen kreativen Nachmittag, ein Date oder einen Kindergeburtstag.",
  "Genève": "In Genève lässt sich Keramik bemalen wunderbar mit einem Spaziergang am See verbinden – ein entspanntes Freizeitangebot für Einheimische und Besucher.",
  "Basel": "Basel mit seiner lebendigen Kunst- und Kulturszene hat auch für Keramikmal-Fans einiges zu bieten.",
  "Lausanne": "Lausanne am Genfersee ist bekannt für Kunst und Design – auch Keramik bemalen findet hier in der Region seinen Platz.",
  "Bern": "In der Bundesstadt Bern gibt es gemütliche Ateliers, in denen man in Ruhe eigene Keramikstücke gestalten kann.",
  "Winterthur": "Winterthur, die Kunststadt im Zürcher Umland, bietet Gelegenheit, kreativ zu werden und eigene Keramik zu bemalen.",
  "Luzern": "Luzern mit seiner malerischen Altstadt lädt auch zum Keramik bemalen ein – ein schönes Ausflugsziel für die ganze Familie.",
  "St. Gallen": "In St. Gallen lässt sich Keramik bemalen als kreative Auszeit vom Alltag geniessen.",
  "Lugano": "Im südlichen Lugano am Luganersee ist Keramik bemalen eine schöne Freizeitaktivität mit mediterranem Flair.",
  "Biel/Bienne": "Die zweisprachige Stadt Biel/Bienne bietet Raum für kreative Stunden beim Keramik bemalen.",
  "Thun": "Thun am Fusse der Berner Alpen ist ein beliebtes Ausflugsziel – auch für kreative Aktivitäten wie Keramik bemalen.",
  "Köniz": "Köniz in der Agglomeration Bern liegt nah an mehreren kreativen Angeboten rund ums Keramik bemalen.",
  "Fribourg": "Die zweisprachige Universitätsstadt Fribourg bietet Gelegenheiten, beim Keramik bemalen kreativ zu werden.",
  "La Chaux-de-Fonds": "La Chaux-de-Fonds in den Neuenburger Bergen ist bekannt für Uhrmacherkunst und Kreativität – auch Keramik bemalen passt gut dazu.",
  "Schaffhausen": "Schaffhausen am Rheinfall ist ein schönes Ziel für einen kreativen Tag mit Keramik bemalen.",
  "Uster": "Uster im Zürcher Oberland liegt nahe an mehreren Ateliers zum Keramik bemalen.",
  "Chur": "Chur, die älteste Stadt der Schweiz, bietet auch Raum für kreative Erlebnisse wie Keramik bemalen.",
  "Vernier": "Vernier bei Genève liegt nahe an kreativen Angeboten rund ums Keramik bemalen.",
  "Sion": "Sion im Wallis, umgeben von Bergen und Reben, ist auch ein schöner Ort für kreative Auszeiten wie Keramik bemalen.",
  "Neuchâtel": "Neuchâtel am gleichnamigen See lädt zu einem kreativen Ausflug rund ums Keramik bemalen ein.",
};

const COORDS = {
  "Zürich": [47.3769, 8.5417],
  "Genève": [46.2044, 6.1432],
  "Basel": [47.5596, 7.5886],
  "Lausanne": [46.5197, 6.6323],
  "Bern": [46.9480, 7.4474],
  "Winterthur": [47.5001, 8.7241],
  "Luzern": [47.0502, 8.3093],
  "St. Gallen": [47.4245, 9.3767],
  "Lugano": [46.0037, 8.9511],
  "Biel/Bienne": [47.1368, 7.2468],
  "Thun": [46.7580, 7.6280],
  "Köniz": [46.9241, 7.4144],
  "Fribourg": [46.8065, 7.1619],
  "La Chaux-de-Fonds": [47.0999, 6.8252],
  "Schaffhausen": [47.6970, 8.6350],
  "Uster": [47.3500, 8.7211],
  "Chur": [46.8499, 9.5320],
  "Vernier": [46.2144, 6.0836],
  "Sion": [46.2331, 7.3606],
  "Neuchâtel": [46.9900, 6.9293],
};

module.exports = TARGET_CITY_NAMES.map((name) => ({
  name,
  slug: citySlug(name),
  intro: INTROS[name] || `Entdecke Keramik bemalen in ${name}.`,
  lat: COORDS[name][0],
  lng: COORDS[name][1],
}));
