const path = require("path");
const pluralize = require("./_11ty/pluralize.js");
const eleventyImg = require("@11ty/eleventy-img");
const Image = eleventyImg.default; // v7 exportiert die Hauptfunktion als "default", nicht als Modul-Root
const { generateHTML } = eleventyImg;
const CleanCSS = require("clean-css");
const { minify: minifyHtml } = require("html-minifier-terser");

// Erzeugt komprimierte WebP + optimierte Originalformat-Varianten aus den
// grossen Quellbildern (Logo, Hero, Stadt-Header-Fotos) statt die unkomprimierten
// Originale 1:1 auszuliefern. Ergebnisse landen unter /images/optimized/ und
// werden von eleventy-img gecacht (kein erneutes Verarbeiten bei jedem Build).
async function optimizedImage(src, alt, { widths = [640], formats = ["webp", "jpeg"], sizes = "100vw", loading = "lazy", fetchpriority, class: className } = {}) {
  const metadata = await Image(src, {
    widths,
    formats,
    outputDir: "./_site/images/optimized/",
    urlPath: "/images/optimized/",
  });
  const imgAttributes = {
    alt,
    sizes,
    loading,
    decoding: "async",
  };
  if (fetchpriority) imgAttributes.fetchpriority = fetchpriority;
  if (className) imgAttributes.class = className;
  return generateHTML(metadata, imgAttributes);
}

// Ausgelagert nach _11ty/studioImage.js, damit _data/studios.js dieselbe
// Funktion direkt in JS aufrufen kann (siehe Kommentar dort - noetig, weil
// async Shortcodes innerhalb von Nunjucks-Macros keinen Output liefern).
const studioImage = require("./_11ty/studioImage.js");

module.exports = function (eleventyConfig) {
  // Als Global-Data registriert (Factory-Funktion, die die eigentliche Funktion
  // zurueckgibt) statt als Datei unter _data/ - dort wuerde Eleventy die Funktion
  // selbst als Value-Factory aufrufen und durch ihren Rueckgabewert ersetzen.
  // So bleibt "pluralize" sowohl in Templates ({{ pluralize(...) }}) als auch in
  // eleventyComputed-Funktionen (data.pluralize(...)) die aufrufbare Funktion.
  eleventyConfig.addGlobalData("pluralize", () => pluralize);

  eleventyConfig.addNunjucksAsyncShortcode("optimizedImage", optimizedImage);
  eleventyConfig.addNunjucksAsyncShortcode("studioImage", studioImage);
  eleventyConfig.addNunjucksAsyncShortcode("studioImage", studioImage);

  // CSS im Build minifizieren statt das unveraenderte Quell-CSS per Passthrough
  // 1:1 auszuliefern.
  eleventyConfig.addTransform("cssmin", function (content, outputPath) {
    if (outputPath && outputPath.endsWith(".css")) {
      return new CleanCSS({}).minify(content).styles;
    }
    return content;
  });

  // HTML-Output minifizieren (Whitespace/Kommentare entfernen) - kleinere
  // Antworten ohne sichtbaren Unterschied.
  eleventyConfig.addTransform("htmlmin", function (content, outputPath) {
    if (outputPath && outputPath.endsWith(".html")) {
      return minifyHtml(content, {
        collapseWhitespace: true,
        removeComments: true,
        collapseBooleanAttributes: true,
        minifyCSS: true,
        minifyJS: true,
      });
    }
    return content;
  });

  // css/style.css wird NICHT mehr per Passthrough kopiert (das wuerde den
  // cssmin-Transform unten umgehen, da Passthrough-Dateien nie durch die
  // Transform-Pipeline laufen) - stattdessen rendert style-output.njk den Inhalt
  // ueber _data/rawCss.js und wird dabei automatisch minifiziert.
  eleventyConfig.addPassthroughCopy("images");
  eleventyConfig.addPassthroughCopy("fonts");
  eleventyConfig.addPassthroughCopy("js");
  eleventyConfig.addPassthroughCopy("robots.txt");
  eleventyConfig.addPassthroughCopy("favicon.ico");
  eleventyConfig.addPassthroughCopy("favicon-16x16.png");
  eleventyConfig.addPassthroughCopy("favicon-32x32.png");
  eleventyConfig.addPassthroughCopy("favicon-48x48.png");
  eleventyConfig.addPassthroughCopy("apple-touch-icon.png");
  eleventyConfig.addPassthroughCopy("android-chrome-192x192.png");
  eleventyConfig.addPassthroughCopy("android-chrome-512x512.png");
  eleventyConfig.addPassthroughCopy("site.webmanifest");
  // Fuer GitHub Pages: haelt die Custom-Domain-Zuordnung ueber jeden Deploy hinweg
  // aufrecht (beim Actions-basierten Deploy wird sonst nichts automatisch gesetzt).
  eleventyConfig.addPassthroughCopy("CNAME");
  // Fuer GitHub Pages: haelt die Custom-Domain-Zuordnung ueber jeden Deploy hinweg
  // aufrecht (beim Actions-basierten Deploy wird sonst nichts automatisch gesetzt).
  eleventyConfig.addPassthroughCopy("CNAME");

  // studios.json liegt ausserhalb von site/ (Single Source of Truth im Editor-Server)
  // und wird von Eleventys Standard-Watcher sonst nicht erfasst.
  eleventyConfig.addWatchTarget(
    path.join(__dirname, "..", "editor-server", "data", "studios.json")
  );

  // Haengt UTM-Parameter an ausgehende Studio-Website-Links an, damit in Google
  // Analytics erkennbar ist, dass der Traffic von potterymaps kam - funktioniert
  // per URL-Objekt auch dann korrekt, wenn die Website-URL bereits eine eigene
  // Query-String hat.
  eleventyConfig.addFilter("withUtm", function (url) {
    if (!url) return url;
    try {
      const parsed = new URL(url);
      parsed.searchParams.set("utm_source", "potterymaps");
      parsed.searchParams.set("utm_medium", "referral");
      parsed.searchParams.set("utm_campaign", "studio_listing");
      return parsed.toString();
    } catch (e) {
      return url;
    }
  });

  eleventyConfig.addFilter("slugify", function (str) {
    return String(str || "")
      .toLowerCase()
      .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue")
      .replace(/é|è|ê/g, "e").replace(/à|â/g, "a").replace(/ç/g, "c")
      .replace(/ß/g, "ss")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");
  });

  return {
    dir: {
      input: ".",
      includes: "_includes",
      data: "_data",
      output: "_site",
    },
  };
};
