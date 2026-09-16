// Einmaliges Skript: setzt das feste Feld "price_from" pro Studio.
// Die Werte wurden NICHT per Regex/Mustersuche ermittelt, sondern durch manuelles
// Lesen von price_mug, price_plate, studio_fee und price_note pro Studio (Stand
// siehe studios.json zum Zeitpunkt der Ausfuehrung). Regel dabei:
//   - Falls eine Studio-/Sitzungsgebuehr pro Person genannt ist (z.B. "CHF 20 pro
//     Person"), gilt deren niedrigster reeller Tarif (z.B. Kinderpreis) als
//     price_from - auch wenn Keramikstuecke separat verrechnet werden.
//   - Falls es keine separate Studiogebuehr gibt ("Keine separate Studiogebühr"),
//     gilt der niedrigste genannte Stueckpreis als price_from.
//   - Zuschlaege (Verlaengerung, Distanz/km, Gold/Platin-Veredelung, Express,
//     Storno-/No-Show-Gebuehren) und Gruppen-Rabatte ab Mindestpersonenzahl
//     zaehlen NICHT als price_from.
//   - War kein verlaesslicher Basispreis auffindbar: price_from = null.
//
// Schreibt ueber die laufende Editor-Server-API (PUT /api/state), damit wie bei
// jeder Aenderung automatisch ein Backup entsteht.
//
// Ausfuehren (bei laufendem Editor-Server):
//   node scripts/set-price-from.js

const BASE = "http://localhost:4000";

const PRICE_FROM = {
  "unique-keramik-malatelier-aarberg": 34,
  "paint-it-easy-ceramics-studio-ceramic-painting-keramik-bemalen-basel": 20,
  "ceramix-toepferstudio-und-pottery-painting-bern": 15,
  "fenetre-a-l-art-keramik-bemalen-keramik-cafe-bern": 39.9,
  "fabrika-azteka-peinture-sur-ceramique-biel-bienne": 25,
  "kreativ-art-box-burgdorf": 6,
  "atelier-herzton-batterkinden": 30,
  "selbergmalt-ch-buelach": 20,
  "maison-ceramique-cortaillod": 20,
  "keramikum-ceramic-painting-studio-zwicky-duebendorf-duebendorf": 15,
  "ceramique-cafe-fribourg-fribourg": 39,
  "noon-cafe-ceramique-geneva": 25,
  "atelier-seestern-keramik-bemalen-in-kaltbrunn-region-rapperswil-kaltbrunn": 15,
  "keramikmalerei-jasmin-agner-kriens": 15,
  "kreativ-pause-keramik-bemalen-laufenburg-laufenburg": 25,
  "hello-frances-pottery-painting-keramikmalen-lucerne": 15,
  "siya-ceramics-i-siya-keramik-i-pottery-painting-lucerne": 20,
  "moon-clay-painting-studio-lucerne": 15,
  "valou-ceramics-montreux": 50,
  "auerhand-offenes-atelier-murgenthal": 20,
  "keramikstudio-kreativ-live-oberhofen": 18,
  "tom-s-tonwerk-ostermundigen": 10,
  "pinselstrich-ceramic-cafe-rueti": 15,
  "two-room-club-keramikstudio-workshop-space-solothurn": 35,
  "spazio-keramikmalstudio-coffee-more-sursee": 20,
  "creative-you-ceramic-painting-studio-thalwil-thalwil": 30,
  "levin-art-studio-ehem-the-rainbow-club-winterthur": 69,
  "janella-keramikatelier-wuerenlingen": 30,
  "hello-frances-keramikmalen-paint-your-own-pottery-zofingen": 15,
  "creative-you-ceramic-painting-studio-zug-zug": 29,
  "atelier-alfar-zuerich": 68,
  "keramik-mal-cafe-zuerich": 45,
  "loki-studio-zurich-oerlikon-zuerich": 59,
  "paint-it-easy-zuerich-creative-cafe-keramik-bemalen-zuerich": 20,
  "paintlounge-paintevents-malstudio-zuerich": 25,
  "siya-ceramics-i-siya-keramik-i-pottery-painting-zuerich": 20,
  "ceramic-malbar-gmbh-zuerich": null,
  "bisquerie-keramik-bemalen-in-zuerich-saentisstrasse-7-8008-zuerich-zuerich": 45,
  "craft-room-red-fox-liestal": 20,
  "craft-room-red-fox-basel": 20,
  "ceramigas-keramik-selbst-bemalen-basel": 15,
  "herzart-winterthur-winterthur": 18,
  "herzart-weisslingen-weisslingen": 18,
  "lavendear-studio-luzern": 59,
  "teig-ton-atelier-st-gallen": 140,
  "tonwerk-keramik-st-gallen": 30,
  "ceramio-reute-ar": 18,
};

async function main() {
  const state = await fetch(`${BASE}/api/state`).then((r) => r.json());
  const studios = state.studios;

  const missing = studios.filter((s) => !(s.slug in PRICE_FROM));
  if (missing.length) {
    console.log("WARNUNG: kein price_from hinterlegt fuer:", missing.map((s) => s.slug));
  }

  let set = 0;
  let nulled = 0;
  studios.forEach((s) => {
    if (s.slug in PRICE_FROM) {
      s.price_from = PRICE_FROM[s.slug];
      if (PRICE_FROM[s.slug] === null) nulled++;
      else set++;
    }
  });

  const res = await fetch(`${BASE}/api/state`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(state),
  });
  const result = await res.json();
  console.log(`Gespeichert (Backup erstellt: ${result.savedAt})`);
  console.log(`price_from gesetzt: ${set}, bewusst leer gelassen (Unsicherheit): ${nulled}`);
}

main();
