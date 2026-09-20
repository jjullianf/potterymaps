// Einmaliges Check-Skript: findet Studios, bei denen sowohl "walk-in" als auch
// "reservation-only" gleichzeitig gesetzt sind (diese beiden Tags schliessen
// sich inhaltlich aus). Aendert NICHTS an den Daten, gibt nur eine Liste aus.
//
// Aufruf: node scripts/check-conflicting-tags.js

const fs = require("fs");
const path = require("path");

const STUDIOS_JSON_PATH = path.join(
  __dirname,
  "..",
  "..",
  "editor-server",
  "data",
  "studios.json"
);

const raw = fs.readFileSync(STUDIOS_JSON_PATH, "utf-8");
const data = JSON.parse(raw);
const studios = data.studios || [];
const lines = raw.split("\n");

// Findet die Zeile, in der das "slug"-Feld dieses Studios im JSON-Rohtext
// steht - fuer eine hilfreiche Fundstelle, da die Datei kein CSV mit fixen
// Zeilen pro Eintrag ist.
function findSlugLine(slug) {
  const needle = `"slug": "${slug}"`;
  const idx = lines.findIndex((l) => l.includes(needle));
  return idx === -1 ? null : idx + 1; // 1-indiziert
}

const conflicts = studios
  .map((s) => {
    const tags = (s.tags || "").split(",").map((t) => t.trim());
    return { s, hasBoth: tags.includes("walk-in") && tags.includes("reservation-only") };
  })
  .filter((r) => r.hasBoth)
  .map((r) => ({
    name: r.s.name,
    slug: r.s.slug,
    city: r.s.city,
    line: findSlugLine(r.s.slug),
  }));

console.log(`Datei: ${path.relative(process.cwd(), STUDIOS_JSON_PATH)}`);
console.log(`Geprueft: ${studios.length} Studios`);
console.log("");

if (!conflicts.length) {
  console.log("Keine Konflikte gefunden - kein Studio hat gleichzeitig \"walk-in\" und \"reservation-only\" gesetzt.");
} else {
  console.log(`${conflicts.length} Studio(s) mit widerspruechlichen Tags ("walk-in" + "reservation-only"):`);
  console.log("");
  conflicts.forEach((c) => {
    console.log(`- ${c.name} (${c.city}) - Slug: ${c.slug}${c.line ? `, Zeile ${c.line}` : ""}`);
  });
}
