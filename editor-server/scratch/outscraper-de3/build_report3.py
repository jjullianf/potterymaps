"""Sortiert den neuen Outscraper-Export (unveraendert gelassen) in A/B/C/D. Schreibt NICHT in studios.json."""
import csv, json, re
from pathlib import Path
HERE = Path(__file__).parent
RAW = json.loads((HERE / "_raw_dump.json").read_text(encoding="utf-8"))["N"]
OLD = json.loads((HERE.parent / "outscraper-de" / "_raw_dump.json").read_text(encoding="utf-8"))
EVID = json.loads((HERE / "evidence.json").read_text(encoding="utf-8"))
EMAILS = json.loads((HERE / "emails_C.json").read_text(encoding="utf-8"))
def pad_plz(p):
    p = re.sub(r"\D", "", str(p or ""))
    return p.zfill(5) if p else ""


def hours_de(wh):
    """Google-Zeiten (englisch, 12h) in deutsche Kurzform: 'Di–Fr 18–20:30 Uhr, Sa–So 13–18:30 Uhr, Mo geschlossen'."""
    if not wh:
        return ""
    try:
        d = json.loads(wh)
    except Exception:
        return ""
    days = [("Monday", "Mo"), ("Tuesday", "Di"), ("Wednesday", "Mi"), ("Thursday", "Do"), ("Friday", "Fr"), ("Saturday", "Sa"), ("Sunday", "So")]

    def conv(t):
        m = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", t.strip(), re.I)
        if not m:
            return t
        h, mm, ap = int(m.group(1)), m.group(2), (m.group(3) or "").lower()
        return h, mm, ap

    def rng(s):
        a, b = [x.strip() for x in s.replace("–", "-").split("-")]
        am_b = re.search(r"(am|pm)$", b, re.I)
        ap_b = am_b.group(1).lower() if am_b else ""
        am_a = re.search(r"(am|pm)$", a, re.I)
        ap_a = am_a.group(1).lower() if am_a else ap_b
        def f(t, ap):
            m = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*(?:am|pm)?", t, re.I)
            h, mm = int(m.group(1)), m.group(2)
            if ap == "pm" and h != 12:
                h += 12
            if ap == "am" and h == 12:
                h = 0
            return f"{h}:{mm}" if mm and mm != "00" else f"{h}"
        return f"{f(a, ap_a)}–{f(b, ap_b)}"

    items = []
    for en, de in days:
        v = d.get(en)
        if not v:
            continue
        v = [x for x in v]
        if v == ["Closed"]:
            items.append((de, "geschlossen"))
        else:
            try:
                items.append((de, " und ".join(rng(x) for x in v) + " Uhr"))
            except Exception:
                return ""
    # aufeinanderfolgende gleiche Werte zusammenfassen
    out, i = [], 0
    while i < len(items):
        j = i
        while j + 1 < len(items) and items[j + 1][1] == items[i][1]:
            j += 1
        label = items[i][0] if i == j else (f"{items[i][0]}–{items[j][0]}" if j > i + 1 else f"{items[i][0]}, {items[j][0]}")
        out.append(f"{label} {items[i][1]}")
        i = j + 1
    return ", ".join(out)


def slug(s):
    s = s.lower().replace("'", "").replace("&", " and ")
    for a, b in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("é", "e"), ("è", "e")]:
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def clean_url(u):
    if not u or u == "None":
        return ""
    u = u.split("%3F")[0].split("?")[0]
    return u



G = {}
def add(i, grp, why): G[i] = (grp, why)
PYS = "Website Paint your Style: Standort Berlin; Gäste suchen sich Keramik aus und bemalen sie ('Sitzplätze nur für Malende', Tisch bis 2,5 Std.)"
C = {
 3: ("Knutselwinkel", "Berlin", "BE", "Website: 'im Knutselwinkel kann jeder Keramik bemalen', Porzellan selber bemalen", "berlin@knutselwinkel.de", "Impressum knutselwinkel.de"),
 4: ("Color Your Day", "Berlin", "BE", "Website: 'Keramik selber bemalen: Wähle ein Keramikstück Deiner Wahl und gestalte es', Plätze reservieren", "hello@colouryourday.de", "Kontaktseite colouryourday.de"),
 5: ("Paint your Style Kreuzberg", "Berlin", "BE", "Website Paint your Style Kreuzberg: 'sucht Euch Eure Wunschkeramik und Farbe aus und bringt sie nach dem Bemalen zum Brennen zurück'", "", ""),
 6: ("Keramino", "Berlin", "BE", "Website: 'Keramik selbst bemalen', Rohlinge aussuchen, Farben, Stempel und Schablonen", "hello@keramino.de", "Impressum keramino.de"),
 11: ("Paint your Style Friedrichshain", "Berlin", "BE", PYS, "simplon8@paintyourstyle.de", "Standortseite Paint your Style Friedrichshain (Reservierungen und Events)"),
 22: ("Namy's Keramikmalstudio", "Berlin", "BE", "Website: freies Bemalen von Tellern, Tassen, Schüsseln zu den Öffnungszeiten, glasiert und gebrannt", "email@keramikbemalen.com", "Impressum keramikbemalen.com"),
 23: ("Paint your Style Zehlendorf", "Berlin", "BE", PYS, "onkeltom1@paintyourstyle.de", "Standortseite Paint your Style Zehlendorf (Reservierungen)"),
 24: ("Paint your Style Köpenick", "Berlin", "BE", PYS, "boelsche103@paintyourstyle.de", "Standortseite Paint your Style Köpenick"),
 27: ("Ceramic Club", "Berlin", "BE", "Website: 'Male 2,5 Stunden frei Hand oder mit unseren Stempeln & Schablonen', Keramikstücke ab 18 €", "info@ceramicclub.de", "Impressum ceramicclub.de"),
 51: ("Paint your Style Hermsdorf", "Berlin", "BE", PYS, "Heinse27@paintyourstyle.de", "Standortseite Paint your Style Hermsdorf"),
 55: ("Meet & Make", "Berlin", "BE", "Website: Format 'Keramik bemalen' mit Ticket-Buchung, Keramik abholen, Special Events (Ceramic & Girls u. a.); daneben Töpfern und Drink & Paint", "hello@meetandmake.de", "Kontaktseite meetandmake.de"),
 61: ("Kreativraum Berlin", "Berlin", "BE", "Website: 'Im Kreativraum Berlin bemalst du Keramik', Glasur und Brand durch das Team", "info@kreativraum-berlin.de", "Impressum kreativraum-berlin.de"),
 71: ("KeraKunst Keramikstudio", "Berlin", "BE", "Website: 'Bei uns habt ihr die Möglichkeit, Keramik zu bemalen', Workshops, Kindergeburtstage (Adresse nur in den Google-Daten)", "info@kerakunst.de", "Kontaktseite kerakunst.de"),
}
for i, t in C.items(): add(i, "C", t[3])
add(69, "B", "Kleinmachnow (14532): Selbstgemacht - Das Keramik Café; Website: Workshops mit Rohlingen und Designs zur Auswahl")
add(75, "B", "Falkensee (14612): Paint your Style Falkensee; Website: 'Sitzplätze nur für Maler'")
DUP = {0: "Mao Mao Keramik Berlin", 1: "Paint your Style Charlottenburg", 2: "Paint your Style Schöneberg", 8: "Keramik for Fun", 9: "Call me Picasso", 10: "Paint your Style Prenzlauer Berg"}
for i, n in DUP.items(): add(i, "A", f"{n} – bereits im Verzeichnis (Duplikat)")
SHOP = [103, 15, 88, 100, 52, 79, 135, 38, 91, 119, 72, 92, 106, 98, 104, 109, 111, 113, 114, 112, 116, 99]
for i in SHOP: add(i, "A", "Shop, Einzelhandel, Museum oder Fachhandel; kein Mal-Angebot für Gäste")
CAFE = [74, 90, 93, 94, 96, 107, 108, 54, 102, 86, 87, 115, 56, 95]
for i in CAFE: add(i, "A", "Café, Restaurant, Event-/Kreativ-Angebot oder Büro ohne Keramik-Bemalen für Gäste (z. B. Spin Painting, Schmuck, Kerzen)")
POT = [12, 13, 14, 16, 17, 18, 20, 21, 28, 29, 31, 32, 33, 34, 35, 37, 43, 45, 46, 47, 49, 50, 57, 58, 59, 60, 62, 63, 64, 65, 67, 68, 76, 77, 78, 80, 82, 83, 85, 89, 91, 97, 101, 105, 110, 118, 120, 121, 122, 123, 124, 126, 128, 129, 130, 133, 136, 137, 30, 26, 39]
for i in POT:
    if i not in G: add(i, "A", "Töpfer-/Keramikwerkstatt oder Kursanbieter (Drehscheibe, Aufbau, Verkauf eigener Keramik); kein Bemalen fertiger Rohlinge durch Gäste")
add(30, "A", "Porzellanmalerei Auftragsarbeiten (Werkstatt laut Website in Österreich), kein Mal-Angebot für Gäste in Berlin")
add(39, "A", "Triviar: Erlebnis-Buchungsplattform für Kurse, kein eigener Betrieb")
add(70, "A", "Keramik-Museum Berlin")
D = {
 25: "crazypaint Keramik und Café: Name deutet auf Bemalen, Website sperrt den Abruf (HTTP 403), nichts belegt",
 66: "The ClayStation: Website sperrt den Abruf (HTTP 403), nichts belegt",
 73: "Keramik & Ton (Teltow): Website sperrt den Abruf (HTTP 403), nichts belegt",
 84: "Manufaktur Pankow: Website sperrt den Abruf (HTTP 403), nichts belegt",
 125: "Good Clay Sunshine Neukölln: Website sperrt den Abruf (HTTP 403), nichts belegt",
 41: "Keramikwerkstatt Töpferei Eva Trenz Diakite: Website nicht erreichbar, nichts belegt",
 53: "tonart lankwitz (Töpferverein): Website liefert 404, nichts belegt",
 81: "Orient Art Studio Schöneberg: Website liefert 404, nichts belegt",
 117: "Keramikatelier Lichtenberg (Bezirksamt): kommunale Kurse; Rohlinge können im Kurs bemalt werden, offenes Bemalen für Gäste nicht belegt",
 7: "Keramikwerkstatt (14059): keine Website, keine Belege",
 19: "Bagma-Keramik: keine Website, keine Belege",
 36: "Tebling-Hass: keine Website, keine Belege",
 40: "Atelier Yafang Qi, Porzellan + Tuschmalerei: keine Website, keine Belege",
 42: "Phoenix-Galeria Keramikwerkstatt: keine Website, keine Belege",
 44: "Jetzt Kreativ: keine Website, keine Belege",
 48: "porzellan & raku: keine Website, keine Belege",
 127: "Keramik Bestiarium: keine Website, keine Belege",
 131: "Hun-Art Einrichtung des Besonderen: keine Website, keine Belege",
 132: "Grünfläche: keine Website, keine Belege",
 134: "Keramikwerkstatt Schnörkelei: keine Website, keine Belege",
 81: "Orient Art Studio Schöneberg: Website liefert 404, nichts belegt",
}
for i, why in D.items(): add(i, "D", why)
for i in (3,4,5,6,11,22,23,24,27,51,55,61,71): pass
missing = [i for i in range(len(RAW)) if i not in G]
print("ohne Zuordnung:", missing)
assert not missing
EXTRA = {}
def clean_url(u):
    if not u or u == "None": return ""
    return u.split("%3F")[0].split("?")[0]

def record(r, nm, city, reg, why, em, srcem, tag, idx):
    street = (r["street"] or "").replace("Str.", "Straße").replace("str.", "straße")
    return {"datei": tag, "zeile": idx + 2, "name": r["name"], "name_vorschlag": nm, "slug_vorschlag": re.sub(r"(-berlin)+$", "-berlin", slug(f"{nm} {city}")),
            "stadt": city, "bundesland": reg, "adresse": r["address"], "strasse": street, "plz": pad_plz(r["postal_code"]),
            "lat": r["latitude"], "lng": r["longitude"], "telefon": r["phone"] if r["phone"] not in (None, "None") else "",
            "oeffnungszeiten_de": hours_de(r["working_hours"]), "website": clean_url(r["website"]), "email": em, "email_quelle": srcem,
            "begruendung": why, "google_place_id": r["place_id"]}

rows = {"A": [], "B": [], "C": [], "D": []}
for i, r in enumerate(RAW):
    grp, why = G[i]
    if grp == "C":
        nm, city, reg, why2, em, srcem = C[i]
        rows["C"].append(record(r, nm, city, reg, why2, em, srcem, "N", i))
    else:
        rows[grp].append({"datei": "N", "zeile": i + 2, "name": r["name"], "adresse": r["address"], "plz": pad_plz(r["postal_code"]),
                          "stadt_laut_daten": r["city"], "website": clean_url(r["website"]), "begruendung": why})
for grp, lst in rows.items():
    keys = sorted({k for x in lst for k in x}, key=lambda k: list(lst[0].keys()).index(k) if k in lst[0] else 99)
    with open(HERE / f"gruppe_{grp}.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(lst)
print({g: len(v) for g, v in rows.items()})
for x in rows["C"]: print(x["stadt"], "|", x["name_vorschlag"], "|", x["slug_vorschlag"], "|", x["strasse"], x["plz"], "|", x["oeffnungszeiten_de"][:60], "|", x["email"] or "-")
