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
    s = s.lower()
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
C = {
 0: ("ceramore", "Düsseldorf", "NW", "Website: 'Keramik bemalen in Düsseldorf', Rohlinge, 'Jetzt reservieren'", "info@ceramore.de", "Impressum ceramore.de"),
 1: ("Eigenlob Keramik", "Düsseldorf", "NW", "Website: 'Keramik malen zum Alles-Inklusive-Preis', MalSes, Maltermin reservieren", "info@eigenlob-keramik.de", "Impressum eigenlob-keramik.de"),
 3: ("DüsselLiebe", "Düsseldorf", "NW", "Website: 'Willkommen im Keramikmalstudio Düsselliebe', Ladies Night, Kindergeburtstage", "info@duessel-liebe.de", "Seite Standort und Kontakt duessel-liebe.de"),
 4: ("Sponk Keramik", "Düsseldorf", "NW", "Website: 'Keramik bemalen und Töpfern im Herzen von Düsseldorf', Workshop 'Keramik bemalen' 42 € fix p.P.", "info@sponkkeramik.de", "Kontakt-/Impressum-Seite sponkkeramik.de"),
 5: ("MANUFATTURA", "Düsseldorf", "NW", "Website: 'keramik selbst bemalen', Mal-Sessions, Preise, Terminanfrage", "", ""),
 16: ("Studio Ami Malwerkstatt", "Düsseldorf", "NW", "Website (Studio Ton): 'Studio Ami Malwerkstatt ... Keramik bemalen', eigene Adresse Birkenstraße 67", "info@studioami.de", "Kontaktseite studioton.de/studioami.de (Studio Ami)"),
 20: ("Studio Brick", "Düsseldorf", "NW", "Website: Kreativstudio mit Workshops; Termine 'Keramik bemalen inkl. Tasse' (28 €), Keramik bemalen & Wein (40,90 €). Kein reines Mal-Atelier, Workshops auch zu anderen Techniken", "", ""),
 8: ("Keramik for Fun", "Berlin", "BE", "Website: 'Bei Keramik For Fun könnt ihr Keramik selbst bemalen', keine Vorerfahrung nötig", "info@keramikforfun.de", "Kontakt-/Impressum-Seite keramikforfun.de"),
 27: ("Mao Mao Keramik", "Berlin", "BE", "Website maomao-keramik.de: 'Keramik bemalen' in Stuttgart, Berlin & Heilbronn, Terminbuchung", "", ""),
 29: ("Paint your Style Schöneberg", "Berlin", "BE", "Website: 'Der Tisch steht Dir bis zu 2 1/2 Stunden zur Verfügung', Reservierung empfohlen, Di–Sa 12–21 Uhr", "rhein48@paintyourstyle.de", "Kontakt-/Anfahrt-Seite Paint your Style Schöneberg"),
 61: ("Call me Picasso", "Berlin", "BE", "Website: 'Keramikcafé in Berlin-Schöneberg: Keramik bemalen, Kaffee oder Tee genießen', Termin reservieren", "info@callmepicasso.de", "Kontakt-/Impressum-Seite callmepicasso.de"),
 28: ("Mao Mao Keramik", "Stuttgart", "BW", "Website maomao-keramik.de: 'Keramik bemalen' in Stuttgart, Berlin & Heilbronn, Terminbuchung", "", ""),
 30: ("Lamooi Gutenbergstraße", "Stuttgart", "BW", "Website: 'Wähle Dir bei uns im Laden Deine Keramik aus, die Du bemalen möchtest', zwei Ateliers in Stuttgart-West", "info@lamooi.de", "Impressum lamooi.de (gemeinsame Adresse beider Ateliers)"),
 31: ("Lamooi Gutbrodstraße", "Stuttgart", "BW", "Website: 'Wähle Dir bei uns im Laden Deine Keramik aus, die Du bemalen möchtest', zwei Ateliers in Stuttgart-West", "info@lamooi.de", "Impressum lamooi.de (gemeinsame Adresse beider Ateliers)"),
 32: ("LUMI Keramik", "Stuttgart", "BW", "Website: 'suchst du dir vor Ort ein Rohkeramikstück aus und bemalst es nach deinen eigenen Ideen'", "hallo@lumi-keramik.de", "Startseite lumi-keramik.de (Kontaktzeile)"),
 39: ("Ma Si – The Italian Experience", "Stuttgart", "BW", "Website: 'Keramikmalatelier: Deine Keramikträume auf Rohlinge bringen'; daneben Café/Events/Workshops", "", ""),
}
for i, (nm, city, reg, why, em, src_) in C.items(): add(i, "C", why)
add(18, "B", "Meerbusch-Büderich (40667): Meerwalt Studio; Website bestätigt Keramik selbst bemalen (Neusser Str. 10)")
A = {
 2: None,
}
A = {
 6: "Instagram-Profil eines Töpferstudios (Mia.töpfert); keine Website, kein Mal-Angebot erkennbar",
 7: None, 9: None, 11: None, 14: None,
 10: "Töpferworkshops (eigene Kunstwerke aus Ton); auf der Website kein Bemalen fertiger Rohlinge",
 12: "Studio Ton Keramikwerkstatt: Töpfern/Drehscheibe, Kurse und Verkauf. Das Bemal-Angebot läuft über Studio Ami (eigener Eintrag)",
 13: "Café-Bar (Kultur); kein Keramik-Angebot gefunden",
 15: "Porzellanmanufaktur KPM, Verkauf; Berlin-Charlottenburg",
 17: "pottery art café Mitte (Köln) – bereits im Verzeichnis (Duplikat)",
 23: "pottery art café Sülz (Köln) – bereits im Verzeichnis (Duplikat)",
 19: "Hetjens-Museum (Keramikmuseum)",
 21: "Café Calma (Instagram), kein Mal-Angebot erkennbar",
 22: "Brunch-Café (Soulbrunch)",
 24: "Design-Shop mit handbemalter Keramik und Porzellan (fertige Stücke), keine Mal-Angebote für Gäste",
 25: "Café/Bar (Kausal)",
 26: "Mikku: DIY-Töpfern (Kurse mit Gipsformen/Drehscheibe), kein Bemalen von Rohlingen",
 33: "Töpfertempel: Töpfern (Drehscheibe), Kurse; kein Bemalen von Rohlingen",
 38: "Töpfertempel: Töpfern (Drehscheibe), Kurse; kein Bemalen von Rohlingen (Doppeleintrag)",
 34: "The Makery: Shop (Verkauf)",
 35: "Isaia Ceramics: Töpferkurse/Drehscheibe, Verkauf",
 36: "Königliche Gartenakademie: Gartenbau/Kurse, Verkauf",
 37: "Lisa Meixner Arte Ceramica: Töpferkurse, offene Keramikwerkstatt",
 42: "Terra Cotta: Atelier mit eigener Keramik und Ausstellungen; Website nennt kein Mal-Angebot",
 44: "The Clay Factory Konstanz: Töpfern (Community Studio, Kurse)",
 45: "Keramikraum Konstanz: Raku-Keramik und Töpferkurse",
 46: "HofArt Studio: Malkurse und Kreativworkshops; Keramik wird auf der Website nicht erwähnt",
 49: "nue pottery: handgemachte Keramik (Shop)",
 50: "Bunzlauer Keramik: Verkauf (Polish Pottery)",
 51: "Triviar: Erlebnis-Buchungsplattform für Kurse, kein eigener Betrieb",
 52: "POCO Berlin-Spandau: Möbelmarkt", 53: "OBI Markt: Baumarkt", 54: "smow Berlin: Möbelgeschäft",
 55: "MUJI: Einzelhandel", 56: "POCO Berlin-Wedding: Möbelmarkt", 58: "Tchibo: Einzelhandel",
 60: "fragile.: handgemachtes Porzellan (Shop)",
 62: "Kreativ Point Kornbeck: Kunstbedarf-Fachhandel und Mal-/Zeichenkurse (Acryl, Aquarell); keine Keramik",
}
for i, why in A.items():
    if why: add(i, "A", why)
D = {
 2: "glazed. Dein Keramik Bemal Studio (Düsseldorf): Name nennt Bemalen, Website sperrt den Abruf (HTTP 403), nichts belegt",
 7: "The Clay Company Shop & Manufaktur (Düsseldorf): Website sperrt den Abruf (HTTP 403), nichts belegt",
 11: "The Clay Company Community Club (Düsseldorf): Website sperrt den Abruf (HTTP 403), nichts belegt",
 9: "Pottery.Hontas Keramik Studio (Düsseldorf): Website sperrt den Abruf (HTTP 403) nach Umleitung auf potteryhontas.com, nichts belegt",
 14: "Kunstraum Reformator Töpferstudio (Düsseldorf): Website sperrt den Abruf (HTTP 403), Name deutet auf Töpfern",
 43: "Atelier KunstZwerk (Konstanz): Website sperrt den Abruf (HTTP 403), nichts belegt",
 40: "Frida & Fred Kreativcafé (Konstanz): Seite zeigt Kreativ-Workshops, aber keine Aussage zu Keramik; Frida's Atelier-Unterseite ungeprüft",
 41: "Kreativ Werkstätte (Konstanz): 'spontan reinkommen und malen', Keramik abholen, Tonverkauf; ob fertige Rohlinge bemalt werden, steht nicht ausdrücklich da",
 47: "Manufattura/Werkstatt Flingern (Düsseldorf): keine Website in den Daten, keine Belege",
 48: "Aliya Keramik (Düsseldorf): keine Website in den Daten, keine Belege",
 59: "OBD Art Studio & Community Space (Düsseldorf): keine Website in den Daten, keine Belege",
 57: "Studio Calma by Artibloom (Düsseldorf): Kreativ-Studio mit Workshops (u. a. Keramik-Wandfliese bemalen, Kerzen, Aquarell); Keramik-Bemalen nur als einzelne Workshops, Mal-Atelier unklar",
}
for i, why in D.items(): add(i, "D", why)
missing = [i for i in range(len(RAW)) if i not in G]
assert not missing, missing

# Berlin-Studios aus der frueheren Koeln-Datei (Gruppe B), Website dort bestaetigt
EXTRA = {0: ("Paint your Style Charlottenburg", "Aus der Köln-Datei: Website bestätigt Keramik bemalen (Paint your Style Charlottenburg-Wilmersdorf)"),
         7: ("Paint your Style Prenzlauer Berg", "Aus der Köln-Datei: Website bestätigt Keramik bemalen (Paint your Style Prenzlauer Berg)")}

def clean_url(u):
    if not u or u == "None": return ""
    return u.split("%3F")[0].split("?")[0]

def record(r, nm, city, reg, why, em, srcem, tag, idx):
    street = (r["street"] or "").replace("Str.", "Straße").replace("str.", "straße")
    return {"datei": tag, "zeile": idx + 2, "name": r["name"], "name_vorschlag": nm, "slug_vorschlag": slug(f"{nm} {city}"),
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
for i, (nm, why) in EXTRA.items():
    r = OLD["KOELN"][i]
    rows["C"].append(record(r, nm, "Berlin", "BE", why, "", "", "KOELN", i))
for grp, lst in rows.items():
    keys = sorted({k for x in lst for k in x}, key=lambda k: list(lst[0].keys()).index(k) if k in lst[0] else 99)
    with open(HERE / f"gruppe_{grp}.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(lst)
print({g: len(v) for g, v in rows.items()})
for x in rows["C"]: print(x["stadt"], "|", x["name_vorschlag"], "|", x["slug_vorschlag"], "|", x["strasse"], x["plz"], "|", x["oeffnungszeiten_de"][:60], "|", x["email"] or "-")
