// Liest die Bilderliste eines Studios (siehe editor-server/public/index.html,
// Feld "images", JSON-Array von URLs/relativen Pfaden, erstes Element = Hauptbild).
// Fallback auf das alte einzelne "image"-Feld, damit Studios, die noch nicht im
// neuen Editor gespeichert wurden, nicht plötzlich ohne Bild dastehen.
function getImageList(s) {
  let arr = [];
  try {
    arr = JSON.parse(s.images || "[]");
  } catch (e) {
    arr = [];
  }
  arr = (arr || []).map((v) => String(v || "").trim()).filter(Boolean);
  if (!arr.length && s.image && String(s.image).trim()) {
    arr = [String(s.image).trim()];
  }
  return arr;
}

module.exports = { getImageList };
