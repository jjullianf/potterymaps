import json,sys,io,contextlib,re
sys.path.insert(0,'editor-server/scratch/outscraper-de3')
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_report3 as b
hours_de=b.hours_de
RAW=json.load(open('editor-server/scratch/outscraper-de12/_raw_dump.json',encoding='utf-8'))['N']
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
BW,BY,NI,SH,MV,SN,BB,RP,ST,HE,NW,HH,TH="BW","BY","NI","SH","MV","SN","BB","RP","ST","HE","NW","HH","TH"
RES="reservation-only"; REC="reservation-empfohlen"
KID="kids-friendly, birthday-parties"
def P(s): return s
mk(0,"kunterwerk-keramikmalstudio-garmisch-partenkirchen","Kunterwerk Keramikmalstudio","Garmisch-Partenkirchen",BY,"info@kunterwerk.de",
 hours="Mo, Di geschlossen, Mi 13–17:30 Uhr, Do 13–20 Uhr, Fr, Sa 10–12 und 13–20 Uhr, So 10–12 und 13–15:30 Uhr",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",
 studio_fee="Ca. 2 Stunden Kreativzeit pro Platz · zum Weitermalen gibt es einen vergünstigten Slot",
 price_note="Der Kreativ-Workshop kostet 35 € und enthält ein Keramikstück bis 20 €, größere Stücke kosten Aufpreis. Reservierung wird empfohlen, spontan geht es bei freien Plätzen.",
 pickup_time="In der Regel innerhalb von 5 Öffnungstagen · Versand gegen Pauschale ab 15 €",
 special_events="Kindergeburtstage, Team-Events, Junggesellinnen- und Junggesellenabschiede und Babypartys, jeweils mit eigenem Bereich für Gruppen.",
 hat_instagram=INS("daskunterwerk"),
 description="Keramikmalstudio in Garmisch-Partenkirchen mit etwa 2 Stunden Kreativzeit pro Platz. Reservieren wird empfohlen, spontan geht es bei freien Plätzen. Es gibt eigene Bereiche für Gruppen und Events.")
mk(3,"mal-zauber-dessau","Mal Zauber","Dessau-Roßlau",ST,hours="",
 tags="reservation-only, kids-friendly, birthday-parties",
 price_note="Preise stehen nicht auf der Website. Anfragen und Reservierungen laufen nur über das Kontaktformular.",
 special_events="Kindergeburtstage, Late-Night-Malen, Party-Boxen, Geburtstagsfeiern und Kindergartenausflüge.",
 description="Keramik-Malstudio in Dessau. Reservierungen laufen über das Kontaktformular. Es gibt Late-Night-Malen, Party-Boxen und Angebote für Kindergeburtstage.")
mk(8,"pinselwerk-husum","Pinselwerk Husum","Husum",SH,tags=RES,
 price_note="Preise stehen nicht auf der Website. Über 150 Rohlinge zur Auswahl. Bitte den Wunschtermin über die Website reservieren.",
 pickup_time="Nach einigen Tagen · Versand auf Wunsch",
 special_events="Candle-Light-Abende mit Keramik bemalen am 29.10. und 26.11.2026, jeweils 19–22 Uhr.",
 description="Keramikmalstudio in Husum mit über 150 Rohlingen. Du reservierst deinen Wunschtermin über die Website und holst dein Stück nach einigen Tagen ab.")
mk(9,"pinselwerk-cuxhaven","Pinselwerk Cuxhaven","Cuxhaven",NI,tags=RES,
 price_note="Preise stehen nicht auf der Website. Über 150 Rohlinge zur Auswahl. Bitte den Wunschtermin über die Website reservieren.",
 pickup_time="Nach einigen Tagen · Versand auf Wunsch",
 special_events="Candle-Light-Abend mit Keramik bemalen am 30.10.2026, 19–22 Uhr.",
 description="Keramikmalstudio in Cuxhaven mit über 150 Rohlingen. Du reservierst deinen Wunschtermin über die Website und holst dein Stück nach einigen Tagen ab.")
mk(17,"klueterbuedel-keramik-bemalen-westoverledingen","Klüterbüdel Keramik bemalen","Westoverledingen",NI,hours="",
 tags="reservation-only, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen auf der Unterseite «Preise». Termine buchst du online. Gruppen bis 18 Personen.",
 special_events="Familien- und Geburtstagsfeiern, Junggesellenabschiede und Firmenevents für Gruppen bis 18 Personen.",
 hat_instagram=INS("klueterbuedel_keramikbemalen"),
 description="Keramik-Malstudio in Westoverledingen in Ostfriesland. Termine buchst du online, für Gruppen bis 18 Personen gibt es Angebote für Feiern, JGA und Firmenevents.")
mk(22,"farbtupfer-keramik-malstudio-norden","Farbtupfer Keramik Malstudio","Norden",NI,hours="",
 tags="corporate-events, birthday-parties",
 price_note="Preise stehen auf einer eigenen Preisseite. Termine und Fragen per Telefon, WhatsApp oder E-Mail.",
 special_events="Geburtstagsfeiern und Teamevents für Kollegen, auch außerhalb der Öffnungszeiten.",
 description="Keramik-Malstudio in Norden an der Nordsee. Termine und Fragen klärst du per Telefon, WhatsApp oder E-Mail, für Gruppen gibt es Geburtstags- und Teamevents.")
mk(24,"your-craft-aurich","Your Craft","Aurich",NI,hours="",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party",price_from="16.90",
 studio_fee="Ca. 2 bis 2,5 Stunden für Erwachsene, ca. 1 bis 1,5 Stunden für Kinder",
 price_note="Ab 16,90 € all-inclusive mit Rohling, Einführung, Farben, Utensilien, Glasieren und Brennen. Spontan vorbeikommen oder telefonisch bzw. online einen Termin vereinbaren.",
 pickup_time="Brennen dauert in der Regel 1–2 Wochen, danach 4 Wochen Zeit zur Abholung (jeder weitere Monat 5 €) · Versand für 7,99 €",
 special_events="Geburtstag, Junggesellenabschied, Kindergärten und Schulklassen sowie Events und Workshops.",
 hat_instagram=INS("yourcraft_store"),
 description="Keramikstudio in Aurich. Du kannst vorbeikommen oder online buchen, Rohling, Farben, Glasur und Brand sind inklusive. Versand ist gegen Gebühr möglich.")
mk(27,"pinselzauber-keramikcafe-hildesheim","Pinselzauber Keramikcafé","Hildesheim",NI,"pinselzauber-keramikcafe@outlook.de",
 hours="Mi–Fr 16:30–19:30 Uhr, Sa, So 10–15:30 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties",price_from="11",
 studio_fee="Nur bei der «Langen Malzeit» (4 Stunden) Mindestumsatz 32 € pro Person",
 price_note="Kleine Dekoartikel und Tiere ca. 11 €, Tassen 19–26 €, Teller und große Rohlinge 25–60 €. Das Haus ist für dieses Jahr laut Website ausgebucht, Januar-Termine sind ab Anfang November buchbar.",
 pickup_time="Nach 2–3 Wochen",
 hat_instagram=INS("pinselzauber.keramikcafe"),
 description="Keramikcafé in Hildesheim. Du reservierst über die Website, das Haus ist derzeit stark ausgebucht, neue Termine erscheinen im Kalender. Nach 2 bis 3 Wochen ist dein Stück gebrannt.")
mk(28,"kreativraum-celle","KreativRaum Celle","Celle",NI,"michaela@kreativraum-celle.de",
 hours="Mo, Mi, Do, So geschlossen, Di, Fr 16–19 Uhr, Sa 11–14 und 15–18 Uhr, weitere Zeiten nach Vereinbarung",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Reservierung online über das Buchungstool. Bei «Krabbeln & Keramik» und «MädelsMomente» fällt nur der Keramikpreis an.",
 special_events="«Krabbeln & Keramik» für Kinder von 0–2 Jahren mit Eltern, donnerstags 10–12 Uhr, JGA, Geburtstage und Firmenveranstaltungen.",
 hat_instagram=INS("kreativraum_celle"),
 description="Kreativstudio in Celle, in dem du Keramik bemalst. Du reservierst online, außerdem gibt es «Krabbeln & Keramik» für Kleinkinder sowie JGA und Firmenveranstaltungen.")
mk(29,"farbenfroh-celle","farbenfroh celle","Celle",NI,"kontakt@farbenfroh-celle.de",
 hours="Mi 16–19 Uhr, Fr 15–18 Uhr, Sa 11–14 und 15–18 Uhr, sonst nach Absprache",
 tags="reservation-empfohlen, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Reservierung erwünscht.",
 pickup_time="Abholung Mi 17–19 Uhr, Fr 16–18 Uhr, Sa 12–14 und 16–18 Uhr",
 special_events="Firmenfeiern, Junggesellinnenabschiede und Geburtstage für bis zu 24 Personen.",
 hat_instagram=INS("farbenfroh_celle"),
 description="Keramik-Malstudio in der Celler Altstadt. Du bemalst Keramik zu festen Zeiten, eine Reservierung ist erwünscht. Für Gruppen bis 24 Personen gibt es Feiern, JGA und Firmenevents.")
mk(34,"celines-ceramics-bremerhaven","Celine's Ceramics","Bremerhaven","HB","info@celines-ceramics.de",
 hours="Di, Fr 14–19 Uhr, sonst nach Vereinbarung",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Termine werden nach Vereinbarung über WhatsApp, Instagram oder Telefon abgestimmt.",
 hat_instagram=INS("celines.ceramics"),
 description="Keramikstudio in Bremerhaven, in dem du Keramik selber bemalst. Termine vereinbarst du über WhatsApp, Instagram oder Telefon.")
mk(36,"keramikatelier-busching-neumuenster","Keramikatelier Busching (Kreativhof)","Neumünster",SH,hours="",
 tags="reservation-only, kids-friendly",
 price_note="Preise stehen nicht auf der Startseite. Lange Malabende (19–22 Uhr) ab 16 Jahren mit Reservierung, nächster Termin 28.10.2026. Keramiken werden nur noch maximal 8 Wochen aufbewahrt.",
 special_events="Lange Malabende, RaBu-Malkurse für Kinder ab 4 Jahren bis 7. Klasse.",
 description="Keramikatelier auf dem Kreativhof in Neumünster. Du reservierst einen Maltermin, es gibt Lange Malabende ab 16 Jahren und regelmäßige Malkurse für Kinder.")
mk(44,"farbfluss-ceramic-art-cafe-neubrandenburg","Farbfluss Ceramic Art Café","Neubrandenburg",MV,
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Termine buchst du online über einen Buchungslink.",
 pickup_time="Etwa 2 Wochen nach dem Malen",
 description="Ceramic Art Café in Neubrandenburg. Du buchst online einen Termin und holst dein bemaltes Stück etwa 2 Wochen später ab.")
mk(50,"smileandpeace-groemitz","smileandpeace Grömitz","Grömitz",SH,addr="Am Strande 15, 23743 Grömitz",
 price_note="Preise und Zeiten stehen auf der Unterseite des Studios Grömitz. Das Studio liegt nur wenige Schritte von der Seebrücke entfernt.",
 special_events="Keramik bemalen, Töpfern im Handaufbau und Workshops. Das Studio gehört zu smileandpeace in Hamburg und Grömitz.",
 hat_instagram="",
 description="Keramikstudio direkt am Meer in Grömitz, einen Steinwurf von der Seebrücke entfernt. Neben Keramik bemalen gibt es Töpfern im Handaufbau und Workshops. Schwesterstudio von smileandpeace in Hamburg.")
mk(51,"pott-und-pinsel-fehmarn","Pott und Pinsel","Fehmarn",SH,"info@pottundpinsel.de",hours="",
 tags="reservation-only",price_from="10",
 studio_fee="Ca. 2,5 Stunden · Malbox-Ausleihe: Mindestumsatz 100 € und 50 € Kaution",
 price_note="Keramik kostet ca. 10–50 € inklusive Farbe, Glasur und Brand. Reservierung über das Buchungssystem oder per E-Mail.",
 pickup_time="Nach 7–10 Tagen im Abholschrank in der Scheune · Versand gegen Gebühr",
 hat_instagram=INS("pott_und_pinsel"),
 description="Keramik bemalen auf Fehmarn in Sahrensdorf. Du reservierst eine Session von etwa 2,5 Stunden, nach 7 bis 10 Tagen ist dein Stück gebrannt. Es gibt auch eine Malbox zum Ausleihen.")
mk(54,"paint-art-bad-harzburg","Paint Art","Bad Harzburg",NI,"paint-art@gmx.net",
 hours="Fr 16–20 Uhr, Sa 14–19 Uhr, Termine nach Vereinbarung jederzeit",
 tags="reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Termine nach Vereinbarung sind jederzeit möglich.",
 pickup_time="Nach 3–5 Tagen",
 special_events="Geburtstage, Junggesellinnenabschiede, Firmenevents (Weihnachtsfeiern, Jubiläen), Teambuilding sowie Kitas und Schulklassen mit bis zu 10 Kindern.",
 description="Keramik-Malstudio in Bad Harzburg im Harz. Du bemalst Keramik vor Ort, Termine sind nach Vereinbarung jederzeit möglich, die Stücke sind nach 3 bis 5 Tagen abholbereit.")
mk(55,"farbe-trifft-ton-nuthetal","Farbe trifft Ton","Nuthetal",BB,"info@farbe-trifft-ton.de",
 hours="Mi 13–19 Uhr, Do, Fr 13–20 Uhr, Sa 10–18 Uhr, So, Feiertage und Ferien abweichend",
 tags="reservation-only, kids-friendly, birthday-parties",price_from="20",
 studio_fee="Malzeit bis zu 3 Stunden pro Reservierung · Kindergeburtstag Mindestumsatz 24 € pro Kind",
 price_note="Keramik kostet 20–59 €. Bitte stets reservieren, die Plätze sind begrenzt. Reservierungsanfragen über Instagram werden nicht bearbeitet.",
 pickup_time="Innerhalb von 1 Woche",
 special_events="Malen in den Abend (bis 22 Uhr), Kindergeburtstag, Keramik-Workshop für Erwachsene, Feierlichkeiten und Malpaket für zu Hause.",
 hat_instagram=INS("farbe_trifft_ton_"),
 description="Keramik-Malstudio in Nuthetal bei Potsdam. Du reservierst einen Tisch für bis zu 3 Stunden, Keramik gibt es ab 20 €. Nach etwa einer Woche ist dein Stück abholbereit.")
mk(57,"ella-keramik-malstudio-sonthofen","ella Keramik-Malstudio Allgäu","Sonthofen",BY,"hallo@ella-keramikbemalen.de",
 hours="Mo, Di, So geschlossen, Mi, Do 14:30–20 Uhr, Fr 12:30–21 Uhr, Sa 11:30–20 Uhr",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Der Malplatz wird über «Malplatz buchen» reserviert.",
 pickup_time="Nach 14 Tagen · Turbo-Brand gegen Aufpreis innerhalb von 3 Tagen",
 special_events="Kleine Spuren, Glühwein & Keramik, Achtsames Malen, Wine & Paint und Märchen & Keramik.",
 hat_instagram=INS("ella.keramik.allgaeu"),
 description="Keramik-Malstudio in Sonthofen im Allgäu. Du buchst online einen Malplatz, nach 14 Tagen ist dein Stück gebrannt, ein Turbo-Brand geht gegen Aufpreis in 3 Tagen.")
mk(61,"keramikwerkstatt-straubing","Die Keramikwerkstatt Straubing","Straubing",BY,"info@keramikwerkstatt-straubing.de",
 hours="Di–So 9–20 Uhr nach Terminvereinbarung",
 tags="reservation-only, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Startseite. Die Werkstatt hat keine festen Öffnungszeiten, Termine buchst du online.",
 special_events="Team-Events, Junggesellenabschiede, Verlaufstechnik-Workshop und Drehkurse.",
 hat_instagram=INS("keramikwerkstatt_straubing"),
 description="Keramikwerkstatt in Straubing, in der du nach Terminvereinbarung Keramik bemalst. Es gibt außerdem Team-Events, JGA und Kurse an der Drehscheibe.")
mk(63,"bemals-dir-keramikmalstudio-prien","Bemal's Dir! Franziskas Keramikmalstudio","Prien am Chiemsee",BY,"bemalsdir.keramikmalen@gmail.com",
 hours="Di, Do, Fr 9–12 Uhr, Fr zusätzlich 19–22 Uhr, So 9–12 und 14–17 Uhr",
 tags="reservation-empfohlen",
 studio_fee="Mindestens 1,5 Stunden einplanen, mehr ist möglich",
 price_note="Preise stehen nicht auf der Startseite. Für Freitagabend und Sonntag ist eine Reservierung nötig. Versand nach Hause ist möglich.",
 hat_instagram=INS("bemalsdir"),
 description="Keramikmalstudio in Prien am Chiemsee. Du planst mindestens 1,5 Stunden ein, für den Freitagabend und den Sonntag musst du reservieren. Versand nach Hause ist möglich.")
mk(64,"dein-lieblingsstueck-keramikmalstudio-trostberg","Dein Lieblingsstück Keramikmalstudio","Trostberg",BY,addr="Marienplatz 11, 83308 Trostberg",
 hours="Ab 1. Dezember: Mo–Mi 16–20 Uhr und jeden ersten Samstag im Monat 12–18 Uhr",
 tags="reservation-only",
 studio_fee="Ca. 3 Stunden",
 price_note="Preise stehen nicht auf der Website. Lebensmittelechte Farben, alle Hilfsmittel, Glasieren und Brennen sind im Preis enthalten. Reservierung über den Kalender.",
 pickup_time="Nach etwa 14 Tagen",
 hat_instagram=INS("deinlieblingsstueck.malstudio"),
 description="Keramikmalstudio in Trostberg im Chiemgau. Du reservierst im Kalender einen Platz für etwa 3 Stunden, nach etwa 14 Tagen ist dein Stück gebrannt.")
mk(66,"malzeit-plauen","Malzeit","Plauen",SN,hours="Di–Fr 15–18 Uhr, Sa 12–18 Uhr, in den Ferien Di–Sa 12–18 Uhr, Mo, So und Feiertage geschlossen",
 tags="reservation-only, kids-friendly, birthday-parties",
 price_note="Preise stehen nicht auf der Website. Tische reservierst du über «Tisch reservieren».",
 special_events="Workshops, Kindergeburtstage, Feiern und Schulklassen.",
 description="Keramik-Malstudio in der Plauener Innenstadt. Du reservierst einen Tisch, dazu gibt es Workshops, Kindergeburtstage, Feiern und Schulklassen.")
mk(68,"bemalbarr-keramikmalstudio-neustadt-am-ruebenberge","bemalbarr Keramikmalstudio","Neustadt am Rübenberge",NI,"hallo@bemalbarr.de",
 hours="Mo, So geschlossen, Di, Mi 15–20:30 Uhr, Fr 14–19:30 Uhr, Sa 10–18:30 Uhr, Do geschlossen",
 tags="reservation-only, hen-party, corporate-events, birthday-parties",price_from="7",
 studio_fee="2,5 Stunden pro Malplatz · Material, Betreuung, Glasieren und Brennen inklusive",
 price_note="Keramik kostet 7–45 € je nach Größe, Form und Besonderheit, Sticker 3,50 €. Du zahlst nur das gewählte Keramikstück.",
 special_events="Junggesellinnen- und Junggesellenabschiede, kreative Geburtstagsfeiern und Team-Events.",
 hat_instagram=INS("bemalbarr"),
 description="Keramikmalstudio in Neustadt am Rübenberge bei Hannover. Du reservierst online einen Malplatz für 2,5 Stunden und zahlst nur das gewählte Keramikstück.")
mk(71,"lislart-studio-aschaffenburg","LislArt Studio","Aschaffenburg",BY,"hello@lislart.de",hours="",
 price_note="Der Workshop «Paint your Cup® – Keramik bemalen» kostet 12 €, das «Ocean Special» 19 €. Workshop-Termine sind buchbar.",
 hat_instagram=INS("lisl.art"),
 description="Studio in Aschaffenburg mit Workshops zum Keramik bemalen, etwa «Paint your Cup®».")
mk(78,"auszeitkeramik-freigericht","auszeitkeramik","Freigericht",HE,hours="",
 price_note="Preise und Termine stehen nicht auf der Startseite. Du wählst aus Rohkeramikprodukten ein Lieblingsstück und bemalst es.",
 description="Atelier in Freigericht-Somborn, in dem du dir aus Rohkeramik ein Lieblingsstück aussuchst und bemalst.")
mk(80,"zitronengold-gelnhausen","zitronengold","Gelnhausen",HE,"info@zitronengold.de",
 hours="Do 16–19 Uhr, Fr 18–21 Uhr, Sa 11–14 und 15–18 Uhr, So 11–14 Uhr, im November und Dezember zusätzlich Mi 16–19 Uhr",
 tags="walk-in, reservation-empfohlen, corporate-events",
 price_note="Preise stehen nicht auf der Website. Eine Anmeldung im Voraus ist erwünscht, spontan geht es bei freien Plätzen.",
 pickup_time="Nach 1–2 Wochen · Abholung frühestens 30 Minuten nach Öffnung",
 special_events="MalSessions, Betriebsevents, Feierlichkeiten in den eigenen Räumen und ein mobiles Atelier zum Ausleihen (Malen@Home).",
 hat_instagram=INS("zitronengold_keramik_schmuck"),
 description="Keramikstudio in Gelnhausen, in dem du Keramik selbst bemalst. Eine Anmeldung wird erwünscht, spontan geht es bei freien Plätzen. Nach 1 bis 2 Wochen ist dein Stück fertig.")
mk(87,"naylas-keramik-studio-dietmannsried","Naylas Keramik Studio","Dietmannsried",BY,"naylas.studio@yahoo.com",hours="",
 tags="kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Startseite. Du wählst Rohlinge und arbeitest mit verschiedenen Techniken.",
 special_events="Mädelsabend, Junggesellinnenabschied, Kindergeburtstag und Firmenevents.",
 hat_instagram=INS("naylaskeramikstudio"),
 description="Keramikstudio mit Keramikbedarf in Dietmannsried im Allgäu. Du wählst Rohlinge und bemalst sie mit verschiedenen Techniken, auch für Mädelsabende, JGA, Kindergeburtstage und Firmenevents.")
mk(88,"malstudio-keramikliebe-memmingen","Malstudio Keramikliebe","Memmingen",BY,"info@malstudio-keramikliebe.de",
 hours="Mo–Mi geschlossen, Do 15–21 Uhr, Fr 14–19:30 Uhr, Sa, So 10–17 Uhr",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Reserviert wird über die Seite «Reservieren».",
 pickup_time="Spätestens nach 10 Tagen im Studio",
 hat_instagram=INS("malstudio.keramikliebe"),
 description="Keramik-Malstudio in Memmingen. Du reservierst online, nach spätestens 10 Tagen holst du dein Stück im Studio ab.")
mk(92,"keramik-malwerkstatt-biberach","KERAMIK Malwerkstatt","Biberach an der Riß",BW,"info@keramik-malwerkstatt.de",
 hours="Mo 18–20:30 Uhr, Fr 15–17:30 und 18–20:30 Uhr, Sa 14–16:30 Uhr, Do teilweise 18–20:30 Uhr, Di, Mi, So geschlossen, weitere Zeiten nach Absprache",
 tags="reservation-empfohlen",
 price_note="Preise stehen nicht auf der Website, sie gelten inklusive Farben, Glasur und Brand. Reservierungen bitte über die Homepage.",
 special_events="Etagerenkurs und Yoga & Keramik (29.11.2026, 15–19 Uhr).",
 hat_instagram=INS("keramik_malwerkstatt"),
 description="Keramik-Malwerkstatt in Biberach an der Riß. Reservierungen laufen über die Homepage, dazu gibt es Kurse wie Etagere und Yoga & Keramik.")
mk(94,"einmalig-keramikmalstudio-buchloe","einMalig Keramikmalstudio Buchloe","Buchloe",BY,"info@einmalig-keramikmalstudio.de",
 hours="Mo–Mi geschlossen, Do, Fr 14:30–20:30 Uhr, Sa, So 9:30–18:30 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="20",
 studio_fee="Zwei Stunden Malzeit",
 price_note="Keramikrohlinge zum Festpreis ab ca. 20 €. Online-Buchung für Gruppen bis 6 Personen, größere Gruppen per E-Mail. Die Zeiten können kurzfristig abweichen.",
 pickup_time="In der Regel ca. 7 Tage nach dem Mal-Erlebnis",
 special_events="JGA 39 € pro Person (ab 6 Personen), Geburtstage und Familienfeiern 25 € pro Teilnehmer (ab 6 Personen), Team-Events 39 € pro Person (ab 10 Personen), Kindergeburtstage, Babyshower und Schulausflüge.",
 hat_instagram=INS("einmalig.buchloe"),
 description="Keramikmalstudio in Buchloe mit 2 Stunden Malzeit. Rohlinge gibt es ab etwa 20 €, Events wie JGA und Geburtstage haben feste Preise pro Person.")
mk(104,"kerameo-leonberg","Kerameo","Leonberg",BW,"info@kerameo.de",hours="",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Du buchst online über einen Buchungslink.",
 pickup_time="In der Regel 2–3 Wochen, der genaue Termin wird am Besuchstag genannt",
 description="Keramik-Malstudio in Leonberg. Du buchst online einen Termin und erfährst am Besuchstag, wann dein Stück nach etwa 2 bis 3 Wochen fertig ist.")
mk(115,"pottery-sisters-achim","pottery sisters","Achim",NI,"potterysisters25@gmail.com",
 hours="Di, Fr 17–19:30 Uhr, Sa 12–14:30 und 15–17:30 Uhr",
 tags="walk-in, reservation-empfohlen, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Online-Buchung über «Termin buchen», spontanes Vorbeikommen während der Öffnungszeiten ist laut Website möglich.",
 special_events="Geburtstage, Team Events und Junggesellinnen- und Junggesellenabschiede über die Events-Seite, Gruppenanfragen per E-Mail.",
 hat_instagram=INS("hi.potterysisters"),
 description="Keramik-Malstudio in Achim bei Bremen. Du buchst online oder kommst spontan vorbei, für Geburtstage, Team Events und JGA gibt es eine Events-Seite.")
mk(116,"green-dream-atelier-hilgermissen","Green Dream Atelier","Hilgermissen",NI,"info@greendreamatelier.de",hours="Nach Terminabsprache",
 tags="reservation-only, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Buchung per E-Mail, WhatsApp oder über «Jetzt Workshop buchen».",
 special_events="Workshops, mobile Workshops, Junggesellinnenabschiede, Team-Events und private Events.",
 description="Atelier in Hilgermissen bei Bremen mit Workshops, in denen du Keramik wie Teller, Tassen und Schüsseln bemalst. Das Atelier öffnet nach Terminabsprache.")
mk(119,"maltelier-ludwigsfelde","Maltelier","Ludwigsfelde",BB,"office@maltelier.de",
 hours="Mo, Di geschlossen, Mi, Do 14–19 Uhr, Fr 14–20 Uhr, Sa, So 11–18 Uhr",
 tags="reservation-only, kids-friendly",price_from="15",
 studio_fee="Ca. 2,5 Stunden · Farben, Materialien, Hilfsmittel, Glasieren von Hand und Brennservice inklusive",
 price_note="Keramik kostet in der Regel 15–60 € je nach Rohling. Tische buchst du über maltelier.paintslot.de.",
 pickup_time="Etwa 2–3 Wochen nach dem Bemalen, das genaue Datum bekommst du beim Besuch",
 special_events="Mach.Mal.Mit. Familie (jeden zweiten Mittwoch), Baby (jeden ersten Mittwoch, 10–12 Uhr), Aufbrezeln und Mystik (ab 16 Jahren) sowie Ferienprogramm.",
 description="Keramik-Malstudio und DIY-Event-Studio in Ludwigsfelde südlich von Berlin. Du buchst einen Tisch für etwa 2,5 Stunden, Keramik kostet 15 bis 60 €.")
mk(120,"keramik-pinselsaal-elmshorn","Keramik-Pinselsaal","Elmshorn",SH,"kontakt@keramik-pinselsaal.de",
 tags="kids-friendly, birthday-parties, hen-party, corporate-events",price_from="3",
 studio_fee="Mindestumsatz 15 € pro Person",
 price_note="Keramik kostet 3–44 €, die meisten Tassen, Becher, Müslischalen und Teller 20–25 €.",
 pickup_time="Nach etwa einer Woche",
 special_events="Geburtstage, Junggesellinnenabschiede, Freundinnen- und Freundeabende, Team-Building, Weihnachts- und Osterdekoration und Kindergeburtstage.",
 hat_instagram=INS("keramik.pinselwerk"),
 description="Keramikmalstudio in der Elmshorner Marktstraße. Es gilt ein Mindestumsatz von 15 € pro Person, die meisten Stücke kosten 20 bis 25 €. Nach etwa einer Woche ist dein Stück gebrannt.")
mk(127,"ton-studio-ahrensburg","ton.studio.","Ahrensburg",SH,hours="",
 price_note="Preise und Ablauf stehen nicht auf der Startseite. Die Website nennt Keramik zu bemalen.",
 hat_instagram=INS("ton.studio.ahrensburg"),
 description="Töpfer- und Keramikstudio in Ahrensburg bei Hamburg mit Möglichkeit, Keramik zu bemalen.")
mk(132,"fijnwerk-studio-ratingen","Fijnwerk Studio","Ratingen",NW,
 hours="Do 15–18 Uhr, Fr 12–18 Uhr, Sa 11–14 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, corporate-events",
 price_note="Preise stehen nicht auf der Startseite. Über 200 Rohlinge und fast 100 Farben und Glasuren. Gebucht wird über den Buchungskalender.",
 special_events="Gast-Workshops, Weihnachtsfeiern, Teamevents und Kindergeburtstage.",
 description="Keramikmalstudio in der Ratinger Altstadt mit über 200 Rohlingen und fast 100 Farben und Glasuren. Du buchst über den Kalender, es gibt auch Teamevents und Kindergeburtstage.")
mk(138,"keramikdate-buxtehude","Keramikdate","Buxtehude",NI,"info@keramikdate.de",
 hours="Fr 15–17:30 Uhr, Sa, So 10–12:30 und 13:30–16 Uhr",
 tags="reservation-only, kids-friendly, hen-party, corporate-events",
 studio_fee="Mindestumsatz 25 € pro Person · Malplatz für 2,5 Stunden",
 price_note="Online-Buchung über den Buchungslink oder per Kontaktformular. Keramik To Go: Bestellung per E-Mail mit 48 Stunden Vorlauf.",
 pickup_time="Etwa 2 Wochen nach dem Bemalen · Abholung Fr 15:30–17 Uhr, Sa, So 10:30–12:30 und 14–16 Uhr",
 special_events="Gruppen, JGA und Teamevents (auch außerhalb der Öffnungszeiten), Kindergeburtstage ab 8 Jahren nur unter der Woche, Gutscheine.",
 hat_instagram=INS("keramikdate"),
 description="Keramikstudio in Buxtehude. Du buchst online einen Malplatz für 2,5 Stunden, dazu gibt es Keramik To Go zum Bemalen zu Hause sowie Events für Gruppen.")
mk(141,"kreativo-keramikmalen-augsburg","Kreativo Keramikmalen","Augsburg",BY,hours="",
 price_note="Preise und Zeiten stehen nicht auf der Startseite. Ein kleines Malstudio in Haunstetten-Siebenbrunn, Parken direkt vor dem Haus möglich. Das Angebot «Keramik malen daheim» bringt das Malstudio zu dir nach Hause.",
 description="Kleines Keramikmalstudio in Augsburg-Haunstetten, das auch Keramik zum Malen daheim anbietet.")
mk(145,"zink-und-zauber-schorndorf","Zink und Zauber","Schorndorf",BW,hours="Di 9–11:30 und 16:30–18:30 Uhr, Do 16:30–18:30 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Startseite. Termine buchst du auf der Seite «Termin buchen». Außerdem gibt es einen Koffer2go zum Bemalen zu Hause.",
 special_events="Junggesellinnenabschied, Firmen- und Teamevent sowie Kindergeburtstag.",
 hat_instagram=INS("zinkundzauber"),
 description="Keramikmalstudio in Schorndorf-Haubersbronn. Termine buchst du online, außerdem gibt es einen Koffer2go zum Bemalen zu Hause.")
mk(146,"mmepottine-keramik-malwerkstatt-leutenbach","MmePottine Keramik-Malwerkstatt","Leutenbach",BW,hours="",
 tags="reservation-only, kids-friendly, birthday-parties, corporate-events",
 price_note="Preise stehen nicht auf der Startseite. Anmeldung zur offenen Malwerkstatt über die Reservierungsseite. Neue Termine für Frühjahr 2027 sind buchbar. Die Malbox «to go» kann ebenfalls reserviert werden.",
 special_events="Kindergeburtstage, Hochzeiten, Mädelsabende, Firmenfeiern und Workshops. Malbox to go zum Bemalen zu Hause.",
 description="Kleine Kreativwerkstatt in Leutenbach im Rems-Murr-Kreis, etwa 20 km außerhalb von Stuttgart. Du meldest dich zur offenen Malwerkstatt an und suchst dir aus einem großen Sortiment Rohkeramik aus.")
mk(150,"kreative-ideenwerkstatt-welzheim","Kreative-Ideenwerkstatt","Welzheim",BW,"info@kreative-ideenwerkstatt.de",
 hours="Mo 15–18 Uhr, Mi 10–12 Uhr (spontan oder zur Abholung), weitere Termine online",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",
 studio_fee="Drei Stunden zum Bemalen",
 price_note="Preise stehen nicht auf der Website. Andere Termine buchst du online.",
 pickup_time="Etwa drei Wochen nach dem Bemalen",
 hat_instagram=INS("kreative_ideenwerkstatt"),
 description="Keramik-Malwerkstatt in Welzheim im Schwäbischen Wald. Du hast drei Stunden zum Bemalen, Termine buchst du online, nach etwa drei Wochen ist dein Stück gebrannt.")
mk(163,"kunterbunt-keramik-ladenburg","Kunterbunt Keramik","Ladenburg",BW,
 hours="Do 15–18 Uhr, Fr 10–12 und 15–18 Uhr, Sa 10–13 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties",
 price_note="Preise stehen nicht auf der Startseite. Malen ist nur nach vorheriger Reservierung per E-Mail möglich, gleich zu Beginn des Termins findet eine ausführliche Maleinführung statt. Begleitplätze gibt es nicht, pro Besucher wird ein Rohling bemalt.",
 special_events="Feierabendmalen, Veranstaltungen und Malbox für zuhause.",
 description="Keramikmalstudio in Ladenburg bei Heidelberg. Malen ist nur nach Reservierung per E-Mail möglich, zu Beginn gibt es eine ausführliche Einführung.")
mk(172,"headfull-of-clay-potsdam","headfull of clay","Potsdam",BB,"info@headfullofclay.de",hours="",
 price_note="Preise stehen nicht auf der Startseite. Die Website nennt Keramik bemalen als Angebot im Atelier.",
 hat_instagram=INS("headfull_ceramics"),
 description="Keramikatelier in Potsdam-Babelsberg mit Töpferangeboten und der Möglichkeit, Keramik zu bemalen.")
mk(182,"cafe-kreativa-schieder-schwalenberg","Café Kreativa","Schieder-Schwalenberg",NW,hours="Mi–So 14–18 Uhr, Frühstück Mi–Fr 8–11 Uhr nach Voranmeldung",
 tags="walk-in",
 price_note="Für freies Bemalen steht kein Preis auf der Website. Der Workshop «Weihnachtsmalerei» kostet 10 € pro Person zuzüglich Rohkeramik und Getränke. Gruppen ab 6–7 Personen sollen einen Tag vorher anrufen.",
 pickup_time="Die Stücke bleiben zum Lasieren und Brennen im Café, du wirst benachrichtigt · Versand möglich",
 special_events="Workshop «Weihnachtsmalerei» am 12.11.2026, Frühstücksbuffets mit Keramikmalerei kombinierbar.",
 description="Café mit Keramikmalerei in Schieder-Schwalenberg. Du kannst ohne Termin malen, Gruppen ab 6 bis 7 Personen rufen einen Tag vorher an. Frühstück ist mit Keramikmalen kombinierbar.")
mk(191,"kreativ-cafe-ton-und-tasse-neukirch","Kreativ Café Ton&Tasse","Neukirch/Lausitz",SN,"info@toepferei-lehmann.de",
 hours="Mo–Fr 14–20 Uhr, Sa 10–18 Uhr, So 11–16 Uhr",
 tags="walk-in, reservation-empfohlen, corporate-events",
 studio_fee="Etwa 1,5–2 Stunden, je nach Detailgrad auch länger",
 price_note="Der Preis richtet sich nach dem gewählten Rohling, Farben, Material, Brennen und Verpackung sind inklusive. Eine Reservierung ist ratsam, im November und Dezember ist ohne Reservierung kein Malplatz garantiert.",
 pickup_time="Nach etwa 14 Tagen, das Datum steht auf dem Lieferschein",
 special_events="Themenabende und Workshops mit Anmeldung, Catering ab 10 Personen und individuelle Öffnungszeiten für Schulklassen und Gruppen.",
 description="Kreativ-Café in Neukirch in der Oberlausitz. Du bemalst etwa 1,5 bis 2 Stunden, Material und Brand sind inklusive. Im Winter und in der Hochsaison wird eine Reservierung geraten.")
mk(231,"hasinger-keramik-mal-studio-darmstadt","Hasinger Keramik-Mal-Studio","Darmstadt",HE,"hallo@hasinger-keramik.de",addr="Jahnstraße 1, 64285 Darmstadt",
 hours="Mo 10–20 Uhr, Di 15–21 Uhr, Mi, Do geschlossen, Fr 15–20 Uhr, Sa 10–20 Uhr, So ausgewählte Specials",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party",
 studio_fee="Ca. 2 Stunden",
 price_note="Preise stehen nicht auf der Startseite. Du reservierst einen Tisch online oder telefonisch unter 06151 2785137.",
 pickup_time="Nach etwa 2 Wochen",
 special_events="Kurse, Kindergeburtstage sowie Feiern und JGA.",
 hat_instagram=INS("hasinger_keramik"),
 description="Keramik-Malstudio in Darmstadt-Bessungen. Du wählst einen Rohling, bemalst ihn etwa zwei Stunden lang und holst ihn nach etwa zwei Wochen gebrannt ab.")
mk(237,"kreativista-studio-bonn","Kreativista Studio","Bonn",NW,hours="",
 price_note="Preise stehen nicht auf der Startseite. Die Website nennt Workshops wie «Porzellan-Tasse bemalen» und «Vase bemalen», Termine auf der Seite «Termine».",
 special_events="Workshops zum Bemalen von Porzellan und Keramik.",
 hat_instagram=INS("kreativista_studio"),
 description="Studio in Bonn mit Workshops, in denen du Porzellan- und Keramikartikel wie Tassen und Vasen bemalst.")
mk(240,"frau-kramer-atelier-bonn","FRAU KRAMER Atelier","Bonn",NW,"info@frau-kramer.de",addr="Sternenburgstraße 38, 53115 Bonn",
 hours="Mi 14–19 Uhr, Do, Fr 10–12:30 und 14–21:45 Uhr, Sa, So 10–18:30 Uhr",
 tags="reservation-only, hen-party, kids-friendly, birthday-parties",
 price_note="Preise stehen nicht auf der Startseite. Du reservierst online über «Malen vor Ort». Betriebsferien vom 23.12.2026 bis 12.01.2027.",
 pickup_time="Fertige Stücke nur während der Öffnungszeiten, frühestens ab 15 Uhr",
 special_events="Junggesellenabschiede, Feste und Events sowie Kindergeburtstage.",
 hat_instagram=INS("fraukramer"),
 description="Keramikmalwerkstatt des Ateliers FRAU KRAMER in Bonn mit festen Mal-Zeiten. Du reservierst online einen Termin in der Werkstatt in der Sternenburgstraße.")
mk(256,"deine-keramikmalerei-schwabmuenchen","Deine Keramikmalerei","Schwabmünchen",BY,"info@deine-keramikmalerei.de",
 hours="Mo, Di geschlossen, Mi 9:30–12 und 15:45–18 Uhr, Do, Fr 15:45–18 Uhr, Sa 9:30–12 und 13:30–18 Uhr, So 9:30–12 und 13:30–15:30 Uhr",
 tags="reservation-only, birthday-parties",price_from="15",
 studio_fee="2 Stunden zum Bemalen inklusive kurzer Einführung",
 price_note="Rohkeramik ab 15 €. Die Reservierung ist kostenfrei, für bis zu 8 Personen.",
 pickup_time="Nach 7 Werktagen (Mo–Sa) zu den Öffnungszeiten",
 special_events="Late Evening 18:30–20:30 Uhr, Special-Events ab 16 Jahren und Paint & Wine (25 € pro Person inklusive Wein und Wasser, zuzüglich Keramik).",
 hat_instagram=INS("deine_keramikmalerei"),
 description="Keramikmalstudio in Schwabmünchen bei Augsburg. Du reservierst kostenlos einen Platz für 2 Stunden, Rohkeramik gibt es ab 15 €, nach 7 Werktagen ist dein Stück abholbereit.")
mk(155,"naturwerkstatt-miriam-becker-karlsruhe","Naturwerkstatt Miriam Becker","Karlsruhe",BW,hours="",
 price_note="Die Website führt «Keramik bemalen» als Workshop und eine Kreativbox «Rohkeramik bemalen» zum Bemalen zu Hause. Preise und Termine stehen auf den Unterseiten.",
 hat_instagram=INS("naturwerkstattmbecker"),
 description="Werkstatt in Karlsruhe mit Töpferkursen, einem Workshop «Keramik bemalen» und einer Kreativbox zum Bemalen zu Hause.")
mk(159,"schoenmalerei-karlsruhe","Schoenmalerei","Karlsruhe",BW,hours="",
 price_note="Der Seitentitel lautet «Keramik selbst bemalen». Preise und Zeiten stehen nicht auf der Startseite.",
 hat_instagram=INS("schoenmalerei_karlsruhe"),
 description="Keramikmalstudio in Karlsruhe-Nordstadt, in dem du Rohkeramik selbst bemalst.")
mk(95,"pinsellust-keramik-malstudio-bergen-auf-ruegen","PinselLust Keramik Malstudio","Bergen auf Rügen",MV,"pinsellust@web.de",
 hours="Do 11–14 Uhr, Fr 14–17 Uhr, Sa 10–12:30 und 14–16:30 Uhr, am 31.10.2026 Sa 10–13 Uhr",
 tags="reservation-only",price_from="15",
 price_note="Rohlinge kosten ab ca. 15 € je nach Größe und Form. Tische buchst du online.",
 pickup_time="Nach ca. 2 Wochen im Studio",
 special_events="Auszeit allein, Nachmittag mit Freunden oder Familie und besondere Events.",
 hat_instagram=INS("pinsellust_malstudio"),
 description="Keramik-Malstudio in Bergen auf Rügen. Du buchst online einen Tisch, Rohlinge gibt es ab etwa 15 €, nach etwa 2 Wochen holst du dein Stück ab.")
mk(25,"keramikliebe-lingen","Keramikliebe Lingen","Lingen",NI,hours="",
 price_note="Die Startseite nennt «Dein Keramik-Malstudio», Preise und Ablauf stehen nicht dort.",
 description="Keramik-Malstudio in der Lingener Innenstadt.")
mk(102,"pauly-keramik-fellbach","pauly keramik","Fellbach",BW,
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Startseite. Termine buchst du online über «Jetzt buchen». Neben Keramik bemalen gibt es Töpferkurse und Keramikverkauf.",
 special_events="Gruppenevents wie JGA, Kindergeburtstage und Firmenfeiern, Schnupperkurse an der Töpferscheibe und Handbuildingkurse.",
 description="Töpferstudio in Fellbach, das im Oktober 2025 eröffnet hat. Neben Töpferkursen kannst du Keramik bemalen, Termine buchst du online.")
mk(114,"potterya-delmenhorst","Potterya","Delmenhorst",NI,
 tags="reservation-only, birthday-parties, hen-party, corporate-events",
 price_note="Im Preis des Rohlings sind alle Kosten außer den Getränken enthalten. Derzeit ist nur Barzahlung möglich. Die Potterya liegt im Pop-Up-Store «Zeitraum» mitten in Delmenhorst. Plätze buchst du online.",
 special_events="Geburtstagsfeiern, Teambuilding-Workshops, Junggesellenabschiede und die Keramikmalkiste für zuhause.",
 description="Keramikmalstudio im Pop-Up-Store «Zeitraum» in der Delmenhorster Innenstadt. Im Rohlingspreis sind alle Kosten außer Getränken enthalten, Plätze buchst du online.")
mk(123,"porzellanlaedchen-hamburg","Porzellanlädchen","Hamburg",HH,hours="",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Startseite. Du buchst über «Termin buchen».",
 description="Keramikmalstudio in Hamburg-Nord, in dem du Keramik selbst bemalst. Termine buchst du online.")
mk(124,"kreativspass-buchholz","KreativSpass Buchholz","Buchholz in der Nordheide",NI,hours="",
 tags="reservation-only, birthday-parties",
 price_note="Preise stehen nicht auf der Startseite. Beim freien Malen wählst du vor Ort ein Keramikstück, bekommst eine kurze Einführung und holst es nach dem Brennen ab. Material ist inklusive.",
 special_events="Events von Geburtstagen bis Teamabenden sowie DIY-Kurse wie Töpfern und Seife gießen.",
 description="Kreativstudio in Buchholz in der Nordheide mit freiem Malen auf Keramik, Events und DIY-Kursen. Du buchst online, Material ist inklusive.")
mk(125,"porzellanikum-augsburg","Porzellanikum","Augsburg",BY,addr="Karolinenstraße 11, 86150 Augsburg",hours="",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen auf der Startseite im Abschnitt zu den Gebühren pro Keramik. 150 Keramikformen, 60 Farben und 25 Hilfsmittel und Techniken wie Stempel und Siebdruck. Tische reservierst du online.",
 special_events="Paint & Pearls, Paint & Brunch, Paint & Dine, Paint & Wine, Paint & Beat, Weihnachten, Ostern, Muttertag, Kindergeburtstag, Firmenevent, Junggesellinnen- und Mädelsabend.",
 description="Event- und Kreativstudio in Augsburg, in dem du Rohkeramik designst und bemalst. Es gibt 150 Keramikformen und Specials wie Paint & Wine oder Paint & Brunch.")
mk(204,"kera-terra-keramikstudio-mainz","Kera Terra Keramikstudio","Mainz",RP,hours="",
 tags="walk-in",
 price_note="Preise stehen nicht auf der Startseite. Das Studio hat Café-Atmosphäre und liegt nahe dem Hauptbahnhof. In den Ferien ist auch montags und dienstags geöffnet.",
 pickup_time="Nach etwa 7–10 Tagen",
 description="Keramikmalwerkstatt in der Mainzer Innenstadt mit Café-Atmosphäre. Du wählst vor Ort deinen Rohling und bemalst ihn mit Farben, Pinseln und Schablonen, nach 7 bis 10 Tagen ist er abholbereit.")
mk(207,"pinselbar-mainz","Pinselbar Mainz","Mainz",RP,tags="reservation-only, kids-friendly",
 price_note="Du zahlst ausschließlich den Preis des gewählten Rohlings, eine Malpauschale gibt es nicht. Kinder unter 12 Jahren nur mit mindestens einer Begleitperson anmelden. Plätze reservierst du online, neue Termine werden regelmäßig veröffentlicht.",
 special_events="Mal-Party, Gutscheine und Kooperationen wie «kavé goes Pinselbar» mit Matcha.",
 description="Keramikmalstudio in Mainz. Du zahlst nur den Preis deines Rohlings, eine Malpauschale gibt es nicht. Plätze reservierst du online zu festen Terminen.")
json.dump(raw,open(p,'w'),ensure_ascii=False,indent=2)
print(len(d))
