// Einmaliges Skript: laedt fuer jede der 20 Staedte ein lizenzfreies Foto ueber
// die Pexels API und speichert es lokal unter site/images/cities/[slug].jpg.
// Wird NICHT beim Build oder zur Laufzeit aufgerufen - manuell mit:
//   node scripts/fetch-city-photos.js
// ausfuehren, wenn neue Staedte dazukommen oder Bilder aktualisiert werden sollen.
const fs = require("fs");
const path = require("path");

function loadEnv(envPath) {
  const content = fs.readFileSync(envPath, "utf-8");
  const env = {};
  content.split("\n").forEach((line) => {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) return;
    const idx = trimmed.indexOf("=");
    if (idx === -1) return;
    env[trimmed.slice(0, idx).trim()] = trimmed.slice(idx + 1).trim();
  });
  return env;
}

const env = loadEnv(path.join(__dirname, "..", ".env"));
const API_KEY = env.PEXELS_API_KEY;

if (!API_KEY) {
  console.error("PEXELS_API_KEY fehlt in site/.env");
  process.exit(1);
}

const targetCities = require("../_data/targetCities.js");
const OUT_DIR = path.join(__dirname, "..", "images", "cities");

async function searchPhoto(query) {
  const url = `https://api.pexels.com/v1/search?query=${encodeURIComponent(query)}&per_page=1&orientation=landscape`;
  const res = await fetch(url, { headers: { Authorization: API_KEY } });
  if (!res.ok) throw new Error(`Pexels API Fehler ${res.status} fuer "${query}"`);
  const data = await res.json();
  return data.photos && data.photos[0] ? data.photos[0] : null;
}

async function downloadImage(url, destPath) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Download fehlgeschlagen (${res.status}): ${url}`);
  const buffer = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync(destPath, buffer);
}

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const results = [];

  for (const city of targetCities) {
    const destPath = path.join(OUT_DIR, `${city.slug}.jpg`);
    try {
      let photo = await searchPhoto(`${city.name} Switzerland cityscape`);
      if (!photo) {
        photo = await searchPhoto(`${city.name} Switzerland`);
      }
      if (!photo) {
        console.log(`- ${city.name}: kein Foto gefunden, wird uebersprungen (Platzhalterfarbe greift)`);
        results.push({ city: city.name, status: "kein Foto gefunden" });
        continue;
      }
      const photoUrl = photo.src.large || photo.src.landscape || photo.src.original;
      await downloadImage(photoUrl, destPath);
      console.log(`✓ ${city.name}: gespeichert (Foto von ${photo.photographer}, Pexels)`);
      results.push({ city: city.name, status: "ok", photographer: photo.photographer });
    } catch (err) {
      console.log(`- ${city.name}: Fehler - ${err.message}`);
      results.push({ city: city.name, status: "Fehler: " + err.message });
    }
    // Kleine Pause, um das Rate-Limit der kostenlosen Pexels-API zu schonen.
    await new Promise((r) => setTimeout(r, 300));
  }

  console.log("\n=== Zusammenfassung ===");
  results.forEach((r) => console.log(`${r.city}: ${r.status}`));
}

main();
