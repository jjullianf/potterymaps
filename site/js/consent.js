(function () {
  "use strict";

  var STORAGE_KEY = "potterymaps_cookie_consent"; // "accepted" | "declined"

  function getConsent() {
    try {
      return window.localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null; // z.B. privater Modus ohne localStorage-Zugriff
    }
  }

  function setConsent(value) {
    try {
      window.localStorage.setItem(STORAGE_KEY, value);
    } catch (e) {
      // localStorage nicht verfuegbar - Banner wuerde dann bei jedem Aufruf
      // erneut erscheinen, aber die Seite funktioniert trotzdem weiter.
    }
  }

  // Laedt Google Analytics (gtag.js) nur, wenn eine Tracking-ID gesetzt UND
  // der Nutzer zugestimmt hat - nie vorher, nie unsichtbar im HTML eingebunden.
  function loadAnalytics() {
    var gaId = window.GA_MEASUREMENT_ID;
    if (!gaId) return; // ID noch nicht eingetragen - Analytics bleibt inaktiv
    if (window.__gaLoaded) return;
    window.__gaLoaded = true;

    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(gaId);
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag("js", new Date());
    gtag("config", gaId, { anonymize_ip: true });
  }

  // Ersetzt einen Google-Maps-Consent-Platzhalter (siehe studio.njk) durch das
  // echte iframe - entweder sofort (falls schon generell zugestimmt) oder erst
  // auf Klick auf "Karte laden" (nur fuer diese eine Karte, ohne die globale
  // Cookie-Entscheidung zu aendern).
  function loadMapEmbed(gate) {
    var src = gate.getAttribute("data-map-src");
    var title = gate.getAttribute("data-map-title") || "Karte";
    if (!src || gate.dataset.loaded === "true") return;
    gate.dataset.loaded = "true";
    var iframe = document.createElement("iframe");
    iframe.src = src;
    iframe.width = "100%";
    iframe.height = "300";
    iframe.style.border = "0";
    iframe.loading = "lazy";
    iframe.title = title;
    gate.replaceWith(iframe);
  }

  // Klick-Tracking auf ausgehende Studio-Website-Links (siehe studio.njk) - der
  // Event-Aufruf ist ein No-Op ohne Wirkung, solange gtag() (siehe loadAnalytics)
  // noch nicht existiert, also ohne Consent kein Tracking-Aufruf.
  function initOutboundLinkTracking() {
    document.addEventListener("click", function (e) {
      var link = e.target.closest(".studio-website-link");
      if (!link || typeof window.gtag !== "function") return;
      window.gtag("event", "studio_link_click", {
        studio_slug: link.getAttribute("data-studio-slug") || "",
        studio_name: link.getAttribute("data-studio-name") || "",
      });
    });
  }

  function initMapGates() {
    // ":not(.leaflet-consent-gate)" ist wichtig - Leaflet-Karten tragen beide
    // Klassen (siehe initLeafletGates unten), sonst wuerden fuer denselben
    // "Karte laden"-Button zwei verschiedene Click-Handler registriert.
    var gates = document.querySelectorAll(".map-consent-gate:not(.leaflet-consent-gate)");
    if (!gates.length) return;
    var consent = getConsent();
    gates.forEach(function (gate) {
      if (consent === "accepted") {
        loadMapEmbed(gate);
        return;
      }
      var btn = gate.querySelector(".map-consent-load-btn");
      if (btn) {
        btn.addEventListener("click", function () {
          loadMapEmbed(gate);
        });
      }
    });
  }

  // Leaflet/MarkerCluster werden selbst gehostet (siehe .eleventy.js), aber erst
  // bei Bedarf nachgeladen (nicht auf jeder Seite vorab), da schon das Laden der
  // Kartenkacheln von OpenStreetMap die IP-Adresse an Dritte übertraegt - das soll
  // genau wie beim Google-Maps-Embed erst nach Klick bzw. genereller Zustimmung
  // passieren, nicht automatisch beim Seitenaufruf.
  var leafletAssetsPromise = null;
  function loadLeafletAssets() {
    if (leafletAssetsPromise) return leafletAssetsPromise;
    leafletAssetsPromise = new Promise(function (resolve, reject) {
      ["/js/vendor/leaflet/leaflet.css", "/js/vendor/leaflet/MarkerCluster.css", "/js/vendor/leaflet/MarkerCluster.Default.css"].forEach(function (href) {
        var link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = href;
        document.head.appendChild(link);
      });
      var leafletScript = document.createElement("script");
      leafletScript.src = "/js/vendor/leaflet/leaflet.js";
      leafletScript.onerror = reject;
      leafletScript.onload = function () {
        var clusterScript = document.createElement("script");
        clusterScript.src = "/js/vendor/leaflet/leaflet.markercluster.js";
        clusterScript.onerror = reject;
        clusterScript.onload = resolve;
        document.body.appendChild(clusterScript);
      };
      document.body.appendChild(leafletScript);
    });
    return leafletAssetsPromise;
  }

  // Aktiviert eine einzelne Leaflet-Karte: blendet den eigentlichen Karten-Container
  // ein, entfernt den Hinweistext/Button und ruft danach die seitenspezifische
  // Init-Funktion (per data-init-fn benannt, z.B. window.__initHomeMap) auf, sobald
  // Leaflet geladen ist.
  function activateLeafletGate(gate) {
    if (gate.dataset.loaded === "true") return;
    gate.dataset.loaded = "true";
    var initFn = window[gate.getAttribute("data-init-fn")];
    var target = gate.querySelector(".leaflet-consent-target");
    if (target) {
      target.hidden = false;
      gate.replaceWith(target);
    }
    if (typeof initFn === "function") {
      loadLeafletAssets().then(initFn);
    }
  }

  function initLeafletGates() {
    var gates = document.querySelectorAll(".leaflet-consent-gate");
    if (!gates.length) return;
    var consent = getConsent();
    gates.forEach(function (gate) {
      if (consent === "accepted") {
        activateLeafletGate(gate);
        return;
      }
      var btn = gate.querySelector(".map-consent-load-btn");
      if (btn) {
        btn.addEventListener("click", function () {
          activateLeafletGate(gate);
        });
      }
    });
  }

  function showBanner() {
    var banner = document.getElementById("cookie-banner");
    if (banner) banner.hidden = false;
  }

  function hideBanner() {
    var banner = document.getElementById("cookie-banner");
    if (banner) banner.hidden = true;
  }

  function applyConsent(value) {
    setConsent(value);
    hideBanner();
    if (value === "accepted") {
      loadAnalytics();
      document.querySelectorAll(".map-consent-gate:not(.leaflet-consent-gate)").forEach(loadMapEmbed);
      document.querySelectorAll(".leaflet-consent-gate").forEach(activateLeafletGate);
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var consent = getConsent();

    if (consent === "accepted") {
      loadAnalytics();
    } else if (consent !== "declined") {
      showBanner();
    }

    initMapGates();
    initLeafletGates();
    initOutboundLinkTracking();

    var acceptBtn = document.getElementById("cookie-accept");
    var declineBtn = document.getElementById("cookie-decline");
    if (acceptBtn) acceptBtn.addEventListener("click", function () { applyConsent("accepted"); });
    if (declineBtn) declineBtn.addEventListener("click", function () { applyConsent("declined"); });

    var settingsLink = document.getElementById("cookie-settings-link");
    if (settingsLink) {
      settingsLink.addEventListener("click", function (e) {
        e.preventDefault();
        showBanner();
      });
    }
  });
})();
