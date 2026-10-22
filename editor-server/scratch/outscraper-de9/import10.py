import json,sys,io,contextlib,re
sys.path.insert(0,'editor-server/scratch/outscraper-de3')
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_report3 as b
hours_de=b.hours_de
RAW=json.load(open('editor-server/scratch/outscraper-de9/_raw_dump.json',encoding='utf-8'))['N']+json.load(open('editor-server/scratch/outscraper-de8/_raw_dump.json',encoding='utf-8'))['N'][2:3]
p='editor-server/data/studios.json'
raw=json.load(open(p)); d=raw if isinstance(raw,list) else raw['studios']
keys=list([s for s in d if s.get('slug')=='layers-koeln'][0].keys())
slugs={s['slug'] for s in d}
INS=lambda u:"ja, https://www.instagram.com/"+u+"/"
def mk(idx,slug,name,city,region,email="",addr=None,hours=None,**kw):
    r=RAW[idx]; assert slug not in slugs,slug
    s={k:"" for k in keys}
    plz=str(r['postal_code']).zfill(5)
    street=(r['street'] or '').replace('Str.','Straße').replace('str.','straße').replace('pl.','platz')
    s.update({"slug":slug,"name":name,"address":addr or f"{street}, {plz} {city}","city":city,
      "phone":(r['phone'] or '') if r['phone']!='None' else "","website":re.sub(r'%3F.*','',r['website']) if r['website'] else "","email":email.lower(),
      "opening_hours":hours if hours is not None else hours_de(r['working_hours']),"tags":"","images":"[]","image":"","custom_faq":"[]","contacted":False,"featured":False,
      "quelle_hinweis":"Outscraper (Google Maps); Aufnahme anhand der Website geprüft am 22.10.2026",
      "lat":float(r['latitude']),"lng":float(r['longitude']),"country":"DE","currency":"EUR","postcode":plz,"region":region})
    s.update(kw); slugs.add(slug); d.append(s)
NW,BW,HE,NI="NW","BW","HE","NI"
mk(16,"glazed-duesseldorf","glazed.","Düsseldorf",NW,"paint@glazeddus.de",
 hours="Mo geschlossen, Di 18:30–21:30 Uhr, Mi 11–21:30 Uhr, Do, Fr 14–21:30 Uhr, Sa 12–21:30 Uhr, So 12–18 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="18",price_mug="25",price_plate="18",
 studio_fee="Keine Malpauschale · 2,5 Stunden · Getränke und Candybar inklusive",
 price_note="Du zahlst nur den Rohling, im Preis sind alle Gebühren, Farben, Glasur, Brand und die Getränke enthalten. Kleine Stücke ab 18 €, Tassen und Becher 25–32 €, Teller ab 18 €, große Platten 58 €. Über 120 saisonal wechselnde Rohlinge. Pro Session maximal 26 Personen, Buchung vorab online.",
 pickup_time="Nach 3 Wochen zu festen Abholzeiten (Di, Mi 18:30–21:30 Uhr, Do, Fr 14–21:30 Uhr, Sa, So 10:30–17 Uhr)",
 special_events="Kindergeburtstage, geschlossene Gruppen für Geburtstage, JGA, Firmenfeiern und Team Events (auch mit eigenem Raum), Paint @Home sowie besondere Sessions wie Baby-Hand- und Fußabdrücke, Paint & Plopp und Lampenschirme.",
 hat_instagram=INS("glazed_dus"),
 description="Keramikmalstudio in Düsseldorf-Derendorf an der Tannenstraße. Du zahlst nur den Rohling, Malplatz, Farben, Glasur, Brand sowie Getränke und Candybar sind inklusive. Die Malsessions dauern 2,5 Stunden und werden vorab online gebucht.")
mk(124,"pinselfein-keramikatelier-ulm","Pinselfein Keramikatelier","Ulm",BW,"info@pinselfeinkeramikatelier.de",addr="Sporerstraße 4, 89079 Ulm",
 hours="Do, Fr 16–18 Uhr, Sa, So 12–14 und 14:45–16:45 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party",
 studio_fee="Buchungen dauern 2 Stunden",
 price_note="Preise stehen auf der Unterseite «Unsere Preise». Die Öffnungszeiten können abweichen, ohne Termin vorher kurz anrufen oder per WhatsApp schreiben. Die Keramikbox to go kostet die Keramik plus 20 € Kaution.",
 pickup_time="Nach etwa 5–7 Tagen · Versand auf Wunsch gegen Versandkosten",
 special_events="Gruppenbuchungen, Geburtstage, Kindergeburtstage, Junggesellenabschiede und Feste wie Valentinstag, Muttertag und Weihnachten sowie Kindercoaching. Keramikbox to go zum Bemalen an einem Ort deiner Wahl.",
 hat_instagram=INS("pinselfein_keramikatelier"),
 description="Kleines Keramikatelier in Ulm-Wiblingen. Du wählst einen Rohling, bemalst ihn zwei Stunden lang und das Atelier übernimmt Glasur und Brand. Termine buchst du online, die Öffnungszeiten können abweichen.")
mk(76,"fraustrauss-marburg","FrauStrauss","Marburg",HE,"hallo@fraustrauss.de",
 hours="Mo, Di, So geschlossen, Mi–Fr 13:30–16 und 16:30–19 Uhr, Sa 10:30–13, 13:30–16 und 16:30–19 Uhr",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="10",
 studio_fee="Keine Zusatzgebühr · 2 bis 2,5 Stunden pro Slot",
 price_note="Tassen und Becher 13–28 €, Teller 12–53 €, Schalen und Schüsseln 12–57 €, Krüge und Vasen 11–47 €, Dosen und Spardosen 14–37 €. Im Preis sind Rohling, Farben, Hilfsmittel, Beratung, Glasur und Brand enthalten. Wer nicht fertig wird, kann an einem Wochentag innerhalb eines Monats zum Fertigmalen vorbeikommen.",
 pickup_time="Nach ca. 14 Tagen, das genaue Datum bekommst du beim Bezahlen",
 special_events="Feiern und Gruppenevents, Malen zu Hause mit der Malkiste. Neben dem Keramikbemalen gibt es Töpfern, offene Werkstatt und Workshops. Im Sommer sitzt du auch auf der Terrasse, diese Plätze sind nicht buchbar.",
 hat_instagram=INS("fraustrauss.de"),
 description="Keramikmalstudio in der Marburger Oberstadt am Steinweg mit zwei Studios. Du wählst einen Rohling, bemalst ihn in einem Slot von etwa 2,5 Stunden, danach glasiert und brennt das Team. Buchen wird empfohlen, spontan geht es bei freien Plätzen.")
mk(63,"matja-keramik-sprockhoevel","matja Keramik","Sprockhövel",NW,"hallo@matja-keramik.de",
 hours="Di 15–18 Uhr, Fr, Sa 10–13 Uhr",
 tags="reservation-only, kids-friendly",
 studio_fee="Kostenlose Reservierung einer Malsession von 2,5 Stunden",
 price_note="Preise stehen nicht auf der Startseite. Du wählst aus Steingut-Keramik. Kinder unter 12 Jahren dürfen zum Bemalen kommen, wenn eine erwachsene Person begleitet, die ebenfalls malt.",
 pickup_time="In der Regel nach ca. 3 Wochen, Di 15–18 Uhr, Fr und Sa 10–13 Uhr",
 special_events="Babybauch-Schale und Events, außerdem Töpferkurse, offene Werkstatt und Brennservice.",
 description="Keramikstudio in einer alten Kornmühle in Sprockhövel im südlichen Ruhrgebiet. Du reservierst kostenlos eine Malsession von 2,5 Stunden und bemalst Steingut-Keramik. Dazu gibt es Töpferkurse und eine offene Werkstatt.")
mk(135,"bines-pottery-vechelde","Bines Pottery Keramikatelier","Vechelde",NI,hours="",
 tags="reservation-only, birthday-parties, hen-party",
 studio_fee="Termine online ohne feste Atelierzeiten · wenige Slots pro Monat",
 price_note="Preise stehen nicht auf der Startseite. Terminänderungen sind bis 24 Stunden vorher kostenlos. Zahlung per EC-Karte, Kreditkarte oder bar.",
 pickup_time="Nach ca. 10 Tagen im Atelier, kein Versand",
 special_events="Kindergeburtstage ab 8 Jahren und Junggesellinnenabschiede auf Anfrage per E-Mail.",
 description="Ruhiges Keramikatelier in Vechelde bei Braunschweig. Du buchst online einen Termin, bemalst einen Rohling mit Keramikfarben und holst ihn nach etwa 10 Tagen gebrannt ab. Es gibt nur wenige Slots pro Monat.")
json.dump(raw,open(p,'w'),ensure_ascii=False,indent=2)
print(len(d))
