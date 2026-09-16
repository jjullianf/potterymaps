// Einmaliges Skript: geocodiert die Adresse (address + city) jedes Studios ueber
// die kostenlose Nominatim-API (OpenStreetMap) und speichert lat/lng zurueck.
// Haelt das Nominatim-Nutzungslimit von max. 1 Anfrage/Sekunde ein und sendet
// einen eigenen User-Agent, wie von Nominatim gefordert.
//
// Schreibt ueber die laufende Editor-Server-API (PUT /api/state), damit wie bei
// jeder Aenderung automatisch ein Backup der vorherigen studios.json entsteht -
// NICHT direkt die Datei anfassen.
//
// Ausfuehren (bei laufendem Editor-Server, siehe editor-server/):
//   node scripts/geocode-studios.js

const BASE = "http://localhost:4000";
const USER_AGENT = "KeramikVerzeichnis/1.0 (privates Verzeichnis-Projekt)";
const NOMINATIM_URL = "https://nominatim.openstreetmap.org/search";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function buildQuery(address, city) {
  // Adresse enthaelt Stadt/Land manchmal schon (z.B. "...9000 St. Gallen, Schweiz") -
  // Duplizieren verwirrt Nominatim und liefert dann faelschlich kein Ergebnis.
  let query = address;
  if (!query.toLowerCase().includes(city.toLowerCase())) query += `, ${city}`;
  if (!/schweiz|suisse|svizzera/i.test(query)) query += `, Schweiz`;
  return query;
}

async function runQuery(query) {
  const url = `${NOMINATIM_URL}?format=json&limit=1&q=${encodeURIComponent(query)}`;
  const res = await fetch(url, { headers: { "User-Agent": USER_AGENT } });
  if (!res.ok) throw new Error(`Nominatim Fehler ${res.status} fuer "${query}"`);
  const results = await res.json();
  if (!results.length) return null;
  return { lat: parseFloat(results[0].lat), lng: parseFloat(results[0].lon) };
}

// Standard-Strassentyp-Abkuerzungen ausschreiben, falls die erste Anfrage kein
// Ergebnis liefert - keine Ratearbeit, nur eine ueblichere Schreibweise derselben
// Adresse (z.B. "Chem." -> "Chemin").
const ABBREVIATIONS = [
  [/\bChem\.\s/gi, "Chemin "],
  [/\bStr\.\s/gi, "Strasse "],
  [/\bAv\.\s/gi, "Avenue "],
  [/\bRte\.\s/gi, "Route "],
];

async function geocode(address, city) {
  const query = buildQuery(address, city);
  let result = await runQuery(query);
  if (result) return result;

  let expanded = query;
  ABBREVIATIONS.forEach(([re, replacement]) => {
    expanded = expanded.replace(re, replacement);
  });
  if (expanded !== query) {
    await sleep(1100);
    result = await runQuery(expanded);
  }
  return result;
}

async function main() {
  const state = await fetch(`${BASE}/api/state`).then((r) => r.json());
  const studios = state.studios;

  const ok = [];
  const failed = [];
  const skipped = [];

  for (const s of studios) {
    if (!s.address || !s.city) {
      skipped.push(s.name);
      continue;
    }
    if (s.lat && s.lng) {
      ok.push(s.name + " (bereits vorhanden)");
      continue;
    }
    try {
      const coords = await geocode(s.address, s.city);
      if (coords) {
        s.lat = coords.lat;
        s.lng = coords.lng;
        ok.push(s.name);
        console.log(`✓ ${s.name}: ${coords.lat}, ${coords.lng}`);
      } else {
        s.lat = "";
        s.lng = "";
        failed.push(s.name);
        console.log(`- ${s.name}: kein Ergebnis gefunden`);
      }
    } catch (err) {
      s.lat = "";
      s.lng = "";
      failed.push(s.name + " (" + err.message + ")");
      console.log(`- ${s.name}: Fehler - ${err.message}`);
    }
    // Nominatim-Nutzungsrichtlinie: max. 1 Anfrage pro Sekunde.
    await sleep(1100);
  }

  const res = await fetch(`${BASE}/api/state`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(state),
  });
  const result = await res.json();
  console.log(`\nGespeichert (Backup erstellt: ${result.savedAt})`);

  console.log("\n=== Zusammenfassung ===");
  console.log(`Erfolgreich geocodiert: ${ok.length}`);
  console.log(`Fehlgeschlagen: ${failed.length}`);
  if (failed.length) failed.forEach((f) => console.log("  - " + f));
  if (skipped.length) {
    console.log(`Übersprungen (keine Adresse/Stadt): ${skipped.length}`);
    skipped.forEach((f) => console.log("  - " + f));
  }
}

main();
