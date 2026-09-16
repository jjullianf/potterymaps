const eleventyImg = require("@11ty/eleventy-img");
const Image = eleventyImg.default; // v7 exportiert die Hauptfunktion als "default", nicht als Modul-Root
const { generateHTML } = eleventyImg;

// Rendert entweder das Studio-Bild (inkl. extern gehosteter URLs aus dem
// "Studio eintragen"-Formular - eleventy-img laedt diese selbst herunter,
// bevor sie optimiert werden) oder, falls kein Bild gesetzt ist ODER die
// URL beim Build nicht verarbeitet werden kann (toter Link etc.), einen
// dezenten Marken-Platzhalter. Beide Faelle nutzen dieselbe CSS-Klasse fuer
// Seitenverhaeltnis/Groesse, damit das Layout nicht springt.
//
// Bewusst als eigenstaendiges Modul (nicht nur als Nunjucks-Shortcode in
// .eleventy.js): async Shortcodes funktionieren zuverlaessig direkt in einem
// Template, aber NICHT innerhalb eines Nunjucks-Macros (dort liefert der
// Aufruf lautlos leeren Output). _data/studios.js ruft diese Funktion daher
// direkt in JS auf und speichert das fertige HTML pro Studio vorberechnet
// (s.cardThumbHtml) - das studio-card.njk-Macro gibt dieses HTML nur noch aus.
async function studioImage(s, { widths = [640], sizes = "100vw", loading = "lazy", fetchpriority, wrapClass } = {}) {
  const placeholderHtml = `<div class="${wrapClass} studio-image-placeholder"><img class="studio-image-placeholder-icon" src="/apple-touch-icon.png" alt="" loading="lazy"></div>`;

  if (!s.image || !String(s.image).trim()) {
    return placeholderHtml;
  }

  try {
    const metadata = await Image(s.image.trim(), {
      widths,
      formats: ["webp", "jpeg"],
      outputDir: "./_site/images/optimized/",
      urlPath: "/images/optimized/",
    });
    const imgAttributes = {
      alt: s.name,
      sizes,
      loading,
      decoding: "async",
      class: wrapClass,
    };
    if (fetchpriority) imgAttributes.fetchpriority = fetchpriority;
    return generateHTML(metadata, imgAttributes);
  } catch (err) {
    console.warn(`[studioImage] Bild fuer "${s.name}" (${s.image}) konnte nicht verarbeitet werden, zeige Platzhalter: ${err.message}`);
    return placeholderHtml;
  }
}

module.exports = studioImage;
