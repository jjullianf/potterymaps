// Umami-Zusatzereignisse (cookielos, ohne Consent). Es werden nur Namen von Aktionen und
// Ateliers gezaehlt, nie Eingaben oder personenbezogene Daten. Ohne geladenes Umami
// (z.B. lokal oder durch Werbeblocker) ist track() ein No-Op.
(function () {
  function track(name, data) {
    try {
      if (window.umami && typeof window.umami.track === "function") window.umami.track(name, data || {});
    } catch (e) {}
  }

  function pageType() {
    var p = location.pathname;
    if (/\/studio\/[^\/]+/.test(p)) return "studio";
    if (/\/staedte\/[^\/]+/.test(p)) return "stadt";
    if (/\/studios-nahe\/[^\/]+/.test(p)) return "studios-nahe";
    if (/\/karte\/?$/.test(p)) return "karte";
    if (/\/events\/?$/.test(p)) return "events";
    if (/^\/(ch|de)?\/?$/.test(p)) return "start";
    return "andere";
  }

  function slugOf(href) {
    var m = (href || "").match(/\/studio\/([^\/?#]+)/);
    return m ? m[1] : "";
  }

  function currentStudio() {
    return slugOf(location.pathname);
  }

  document.addEventListener("click", function (e) {
    var t = e.target;
    if (!t || !t.closest) return;

    // Karte: Klick auf Pin und auf Link im Popup
    var popupLink = t.closest(".leaflet-popup a[href], .map-card a[href]");
    if (popupLink) {
      var card = popupLink.closest(".map-card");
      var nameLink = card ? card.querySelector(".map-card-name") : popupLink;
      track("karte_popup_klick", { studio: slugOf(nameLink.getAttribute("href")), seite: pageType() });
      return;
    }
    if (t.closest(".leaflet-marker-icon")) {
      track("karte_pin_klick", { seite: pageType() });
      return;
    }

    var a = t.closest("a[href]");
    if (!a) return;
    var href = a.getAttribute("href") || "";

    // Kontaktdaten auf der Studioseite
    if (/^tel:/i.test(href)) {
      track("kontakt_klick", { art: "telefon", studio: currentStudio() });
    } else if (/^mailto:/i.test(href)) {
      track("kontakt_klick", { art: "email", studio: currentStudio() });
    } else if (/instagram\.com/i.test(href) && currentStudio()) {
      track("kontakt_klick", { art: "instagram", studio: currentStudio() });
    } else if (/(google\.[a-z.]+\/maps|maps\.app\.goo\.gl|goo\.gl\/maps)/i.test(href)) {
      track("kontakt_klick", { art: "route", studio: currentStudio() });
    } else if (/\/studio-eintragen\/\?studio=/.test(href)) {
      track("fehler_melden_klick", { studio: currentStudio() });
    } else if (/\/studio\/[^\/]+/.test(href) && !/\/studio\/[^\/]+/.test(location.pathname) && !a.closest(".site-header")) {
      // Klick von einer Liste oder Karte zur Studioseite
      track("studio_oeffnen", { studio: slugOf(href), von: pageType() });
    } else if (a.closest("#city-suggestions")) {
      track("stadt_suche", { aktion: "vorschlag", ziel: href.replace(/\/$/, "").split("/").pop() });
    }
  });

  // Stadtsuche auf der Startseite: nur ob gesucht wurde, nie der eingegebene Text
  var searchForm = document.getElementById("city-search-form");
  if (searchForm) {
    searchForm.addEventListener("submit", function () {
      track("stadt_suche", { aktion: "enter" });
    });
  }

  // Formulare (Atelier eintragen, Event anfragen): nur dass abgeschickt wurde
  document.addEventListener("submit", function (e) {
    var f = e.target;
    if (!f || f.id === "city-search-form") return;
    var name = f.id === "studio-form" ? "studio-eintragen" : f.id === "anfrage-form" ? "event-anfrage" : f.id || "formular";
    track("formular_abgeschickt", { formular: name });
  });

  // Scrolltiefe, jede Marke pro Seite einmal
  var marks = [25, 50, 75, 100];
  var sent = {};
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      ticking = false;
      var doc = document.documentElement;
      var total = doc.scrollHeight - window.innerHeight;
      if (total <= 0) return;
      var pct = (window.scrollY / total) * 100;
      marks.forEach(function (m) {
        if (pct >= m - 1 && !sent[m]) {
          sent[m] = true;
          track("scrolltiefe_" + m, { prozent: m, seite: pageType() });
        }
      });
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
})();
