const fs = require("fs");
const path = require("path");

// Liest die CSS-Quelldatei als Rohtext ein, damit style-output.njk sie durch
// die Eleventy-Transform-Pipeline (und damit den cssmin-Transform) schicken kann -
// eine per addPassthroughCopy kopierte Datei wuerde diese Pipeline umgehen.
module.exports = () => fs.readFileSync(path.join(__dirname, "..", "css", "style.css"), "utf-8");
