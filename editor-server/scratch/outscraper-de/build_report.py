"""
Erzeugt aus den (unveraenderten) Outscraper-Exporten + evidence.json + emails_C.json die
Ergebnisdateien: Gruppe A/B/C/D als CSV. Aendert keine Originaldateien und schreibt NICHT in
studios.json.
"""
import csv, json, re
from pathlib import Path

HERE = Path(__file__).parent
RAW = json.loads((HERE / "_raw_dump.json").read_text(encoding="utf-8"))
EVID = json.loads((HERE / "evidence.json").read_text(encoding="utf-8"))
EMAILS = json.loads((HERE / "emails_C.json").read_text(encoding="utf-8"))

# (Gruppe, Begruendung / Beleg)  - Schluessel: "TAG:index"
G = {}
def add(tag, idx, grp, why):
    G[f"{tag}:{idx}"] = (grp, why)

# ---------------- KÖLN ----------------
add("KOELN", 1, "C", "Website potterylab.de: 'Keramik bemalen in Köln', Malslot 2,5 Std. inkl. Keramikauswahl")
add("KOELN", 2, "C", "Website potterylab.de: 'Keramik bemalen in Köln', Malslot 2,5 Std. inkl. Keramikauswahl")
add("KOELN", 3, "C", "Website: 'Keramik selbst bemalen in einer gemütlichen Café-Atmosphäre'")
add("KOELN", 5, "C", "Website: 'Keramik selber bemalen', Rohling aussuchen, bemalen (ca. 2,5 Std.), wir glasieren und brennen")
add("KOELN", 6, "C", "Website: 'Keramik bemalen in Köln', Rohling, Bemalen, Abholen; Café")
add("KOELN", 8, "C", "Website: 'Keramik bemalen in Köln' mit Bar & Außenbereich")
add("KOELN", 9, "C", "Website: 'Keramik selber bemalen', Malslot kostenlos, bezahlt wird der Rohling")
add("KOELN", 10, "C", "Website: Keramik-Malstudio, 'bemalst du Keramik nach deinen eigenen Vorstellungen'")
add("KOELN", 11, "C", "Website: 'Keramik selbst bemalen in einer gemütlichen Café-Atmosphäre'")
add("KOELN", 0, "B", "Berlin (10623): Paint your Style Charlottenburg-Wilmersdorf; Website bestätigt Keramik bemalen")
add("KOELN", 4, "B", "Berlin (10709): Börkey Keratech GmbH; zusätzlich klarer Ausschluss (Fachhandel für Keramik-/Porzellanbedarf)")
add("KOELN", 7, "B", "Berlin (10439): Paint your Style Prenzlauer Berg; Website bestätigt Keramik bemalen")
add("KOELN", 12, "B", "Berlin (10623): KPM Royal Porcelain Factory; zusätzlich klarer Ausschluss (Porzellanmanufaktur/Shop)")
add("KOELN", 13, "B", "Berlin (10587): boesner Berlin-Charlottenburg; zusätzlich klarer Ausschluss (Kunstbedarf-Fachhandel)")
add("KOELN", 14, "A", "Triviar Köln: Erlebnis-Buchungsplattform (triviar.de, 'Handverlesene Kurse & Workshops in Köln'), kein eigener Betrieb")

# ---------------- LEIPZIG ----------------
add("LEIPZIG", 0, "C", "Website: 'Keramik selbst bemalen & Töpferkurse', Kurs 'Keramik selbst bemalen'")
add("LEIPZIG", 1, "C", "Website: 'Keramikmalstudio - Erst malen, dann staunen', Termin vorab vereinbaren")
add("LEIPZIG", 3, "C", "Website: Kurs 'Keramik bemalen: Bemalen Sie Biskuitkeramik in entspannter Atelieratmosphäre' (Buchung über Partner Konfetti Töpfern)")
add("LEIPZIG", 4, "C", "Website ohkeramik.de: 'Keramik bemalen ... Gestalte deine Keramik-Lieblingsstücke', Leipzig mit eigenen Öffnungszeiten gelistet (Startseite nennt zuerst Annaberg/Oberwiesenthal)")
add("LEIPZIG", 16, "C", "Website: Angebot 'Keramik bemalen' (25 € je Person zzgl. Rohkeramik), Gästebewertungen 'Termin zum Keramik bemalen'")
# B
add("LEIPZIG", 17, "B", "Schkeuditz (04435): Keramikstudio Lima; Website nicht abrufbar (HTTP 403), Inhalt ungeprüft")
add("LEIPZIG", 40, "B", "Halle (Saale) (06108): Paint Your Style Halle; Website bestätigt Keramik bemalen")
add("LEIPZIG", 41, "B", "Chemnitz (09111): Made by You Chemnitz; Website: 'Keramik selbst bemalen'")
add("LEIPZIG", 43, "B", "Zwickau (08056): Made By You Zwickau; Website: 'Keramik selbst bemalen'")
add("LEIPZIG", 46, "B", "Taucha (04425): Hand & Werk Kreativladen Taucha; Website nennt Töpfern (Kurse), Mal-Angebot unklar")
add("LEIPZIG", 49, "B", "Elstertrebnitz (04523): Keramik-Zauber; Website zeigt Online-Shop")
# D
add("LEIPZIG", 12, "D", "Keine Website in den Daten, keine Belege für Bemalen (Name: Werkstatt & Laden)")
add("LEIPZIG", 13, "D", "Website camolita.de zeigt nur Strato-Platzhalter ('Domain freigeschaltet, noch keine Inhalte')")
add("LEIPZIG", 15, "D", "Töpferwerkstatt/Verein (Drehkurse, Kollektionen). Nur zum jährlichen 'Tag der offenen Töpferei' (14./15.03.2026) kann selbst hergestellte Keramik bemalt werden; sonst kein Mal-Angebot gefunden")
add("LEIPZIG", 21, "D", "Keine Website in den Daten, keine Belege (Adresse: Feinkost eG)")
add("LEIPZIG", 28, "D", "Kreativ-Workshopstudio (Kerzen, Lampen, Trockenblumen; Teamevent/JGA/Kindergeburtstag). Nur ein saisonaler Workshop 'XMAS with BÄM! Keramikkränze - Farbe & Feuer' erwähnt; unklar, ob Keramik bemalt wird")
add("LEIPZIG", 30, "D", "Website thoboe-tonkunst.de liefert keinen lesbaren Text; keine Belege (Name: Keramikwerkstatt)")
add("LEIPZIG", 48, "D", "Keine Website in den Daten, keine Belege (Name: Keramik Barbara Spindler)")
# A
A = {
    5: "makipottery.de: Drehkurse und offene Töpferwerkstatt (Drehscheibe, Werktisch, Glasiertisch); kein Bemalen von Rohlingen",
    6: "Töpferkurse und Verkauf eigener Keramik; kein Mal-Angebot auf der Website",
    7: "DIY-Workshops (Terrazzo, Aquarell, Tuften, Sticken, Glas bemalen); auf den geprüften Seiten kein Keramik-Bemalen",
    8: "Offene Töpferwerkstatt, Töpfer-Workshops, Shop/Templates; kein Bemalen von Rohlingen",
    9: "Keramik-Label/Kollektiv; Workshops laufen über Open Studio Papaya (Töpfern); kein Mal-Angebot. Gleiche Adresse wie Open Studio Papaya (Roßplatz 12)",
    10: "Verkauf eigener Töpferwaren und Töpferkurse; kein Bemalen von Rohlingen",
    11: "Shop für eigene handgefertigte Keramik und Handbuilding-Workshops; kein Mal-Angebot",
    14: "Künstlerin: Shop, Raku-Workshops, Workshop-Reisen; kein Bemalen von Rohlingen",
    18: "Offene Keramikwerkstatt und Drehkurse (Töpfern); kein Bemalen von Rohlingen",
    19: "Keramikwerkstatt im Kulturzentrum Werk 2: Töpferkurse/Projekte und Werkstattverkauf; kein Bemalen von Rohlingen",
    22: "Töpfer-Open-Studio und Workshops (Handbuilding, Drehscheibe, Glasieren); gleiche Adresse wie Studio Papaya",
    24: "Geschenk-/Concept-Laden ('Happy Store', Regalmieter, Unikate von Künstler*innen); kein Mal-Angebot",
    25: "Hobby- und Kunsttöpferei mit Töpferkursen; kein Bemalen von Rohlingen",
    26: "DIY-Kreativcafé (Polstern, Basteln, Miniaturen bemalen); auf der Website kein Keramik-Angebot",
    27: "Spin Painting (anderes Thema), kein Keramik",
    31: "Concept Store (Papeterie/Geschenke)",
    33: "Töpferei für Bau- und Gebrauchskeramik, Verkauf/Märkte; kein Mal-Angebot",
    34: "Hobby-/Kunstbedarf-Fachhandel (Kunstbedarf)",
    36: "Töpferkurse (Aufbautechniken, Glasieren) und Shop; kein Bemalen von Rohlingen",
    37: "Künstlerinnen-Atelier/Galerie für eigene Porzellanobjekte (Shop, Termine); kein Mal-Angebot",
    38: "Töpfern ohne Scheibe (Kurse); Bemalen (Engobe) nur an selbst getöpferten Objekten, keine fertigen Rohlinge",
    39: "Kunstschule (Zeichen-/Töpferkurse); Kunstschulen sind ausgeschlossen",
    42: "Goldschmiede (Schmuck, Goldschmiedekurse)",
    44: "Porzellan-Werkstattladen; Workshops zur Herstellung eigener Porzellanstücke, kein Bemalen von Rohlingen",
    45: "Töpfern im Stadtgut Mölkau; kein Bemalen von Rohlingen",
    47: "Verkaufsgalerie für Keramik, Kunst und Schmuck",
    50: "Keramikwerkstatt mit Verkauf/Märkten; Website nennt kein Mal-Angebot",
}
for i, why in A.items():
    add("LEIPZIG", i, "A", why)


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


CITY = {"KOELN": ("Köln", "NW"), "LEIPZIG": ("Leipzig", "SN")}

# bereinigte Anzeigenamen (SEO-Anhaengsel entfernt) - Vorschlag, in der Bestaetigung pruefbar
NAMES = {
    "KOELN:1": "Pottery Lab Südstadt", "KOELN:2": "Pottery Lab Innenstadt",
    "KOELN:3": "pottery art café Sülz", "KOELN:11": "pottery art café Mitte",
    "KOELN:5": "ceramify Studio Köln-Dellbrück", "KOELN:9": "ceramify Studio Köln-Innenstadt",
    "KOELN:6": "layers", "KOELN:8": "studio fein", "KOELN:10": "glaze",
    "LEIPZIG:0": "Kreativwerk Leipzig", "LEIPZIG:1": "Made by you Leipzig",
    "LEIPZIG:3": "Tirod-Art Keramik", "LEIPZIG:4": "OH! Keramik Leipzig",
    "LEIPZIG:16": "Kopffüßler Keramik- und Kreativwerkstatt",
}
# E-Mail nur, wenn auf Impressum/Kontakt-Seite (oder Kontaktzeile) wirklich genannt: (adresse, quelle)
EMAIL_OK = {
    "KOELN:1": ("info@pottery-lab.de", "Kontakt-/Impressum-Seite potterylab.de (weitere im Impressum: potterylabkoeln@outlook.de)"),
    "KOELN:2": ("info@pottery-lab.de", "Kontakt-/Impressum-Seite potterylab.de (weitere im Impressum: potterylabkoeln@outlook.de)"),
    "KOELN:3": ("info_suelz@pottery-art-cafe.de", "Kontaktseite pottery-art-cafe.de, Standort Sülz"),
    "KOELN:11": ("info@pottery-art-cafe.de", "Kontakt-/Impressum-Seite pottery-art-cafe.de, Standort Mitte"),
    "KOELN:5": ("info@ceramify-studio.de", "Impressum ceramify-studio.de"),
    "KOELN:9": ("info@ceramify-studio.de", "Impressum ceramify-studio.de"),
    "KOELN:6": ("koeln@layers-studios.de", "Kontaktseite layers-studios.de/koeln"),
    "KOELN:8": ("info@studiofein.com", "Impressum studiofein.com"),
    "KOELN:10": ("info@glazestudioo.de", "Impressum/Kontakt glazestudioo.de"),
    "LEIPZIG:0": ("kontakt@kreativwerk-leipzig.de", "Impressum/Kontakt kreativwerk-leipzig.de"),
    "LEIPZIG:4": ("hello@ohkeramik.de", "Impressum ohkeramik.de"),
    "LEIPZIG:16": ("info@kopffüssler.com", "Kontaktzeile auf der Startseite (Domain mit Umlaut)"),
}


def slug(s):
    s = s.lower()
    for a, b in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("é", "e"), ("è", "e")]:
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def clean_url(u):
    if not u or u == "None":
        return ""
    u = u.split("%3F")[0].split("?")[0]
    return u


rows = {"A": [], "B": [], "C": [], "D": []}
counts = {}
for tag, recs in RAW.items():
    counts[tag] = {"leer": 0, "A": 0, "B": 0, "C": 0, "D": 0}
    for i, r in enumerate(recs):
        if r["name"] in (None, "None"):
            counts[tag]["leer"] += 1
            continue
        key = f"{tag}:{i}"
        grp, why = G[key]
        counts[tag][grp] += 1
        ev = EVID.get(key, {})
        base = {
            "datei": tag, "zeile": i + 2, "name": r["name"], "adresse": r["address"], "plz": pad_plz(r["postal_code"]),
            "stadt_laut_daten": r["city"], "website": clean_url(r["website"]), "begruendung": why,
        }
        if grp == "C":
            city, region = CITY[tag]
            nm = NAMES[key]
            em = EMAIL_OK.get(key, ("", ""))
            base.update({
                "name_vorschlag": nm, "slug_vorschlag": slug(f"{nm} {city}") if nm.lower() not in ("layers", "studio fein", "glaze") else slug(f"{nm} {city}"),
                "stadt": city, "bundesland": region, "strasse": r["street"], "lat": r["latitude"], "lng": r["longitude"],
                "telefon": r["phone"] if r["phone"] != "None" else "", "oeffnungszeiten_de": hours_de(r["working_hours"]),
                "email": em[0], "email_quelle": em[1], "website_final": ev.get("url", ""), "google_place_id": r["place_id"],
            })
        rows[grp].append(base)

for grp, lst in rows.items():
    if not lst:
        continue
    fn = HERE / {"A": "gruppe_A_entfernt.csv", "B": "gruppe_B_anderer_ort.csv", "C": "gruppe_C_behalten.csv", "D": "gruppe_D_pruefen.csv"}[grp]
    keys = list(lst[0].keys()) if grp != "C" else list(lst[0].keys())
    with open(fn, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=sorted({k for r in lst for k in r}, key=lambda k: list(lst[0].keys()).index(k) if k in lst[0] else 99))
        w.writeheader()
        w.writerows(lst)
print(json.dumps(counts, indent=1))
print({g: len(v) for g, v in rows.items()})
for r in rows["C"]:
    print(r["name_vorschlag"], "|", r["slug_vorschlag"], "|", r["oeffnungszeiten_de"], "|", r["email"] or "(keine)")
