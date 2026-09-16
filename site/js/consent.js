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

  function initMapGates() {
    var gates = document.querySelectorAll(".map-consent-gate");
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
      document.querySelectorAll(".map-consent-gate").forEach(loadMapEmbed);
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
