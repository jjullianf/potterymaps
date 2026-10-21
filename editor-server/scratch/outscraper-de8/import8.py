import json,sys,io,contextlib,re
sys.path.insert(0,'editor-server/scratch/outscraper-de3')
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_report3 as b
hours_de=b.hours_de
RAW=json.load(open('editor-server/scratch/outscraper-de8/_raw_dump.json',encoding='utf-8'))['N']
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
      "quelle_hinweis":"Outscraper (Google Maps); Aufnahme anhand der Website geprüft am 21.10.2026",
      "lat":float(r['latitude']),"lng":float(r['longitude']),"country":"DE","currency":"EUR","postcode":plz,"region":region})
    s.update(kw); slugs.add(slug); d.append(s)
NI,SH,MV="NI","SH","MV"
KC=dict(tags="walk-in, reservation-empfohlen, birthday-parties, corporate-events",price_from="7",
 price_note="Komplettpreise von 7 bis 75 € je nach Rohling, Farben, Pinsel, Glasur und Brand sind inklusive. Es gibt keine zusätzliche Gebühr. Gruppen ab 6 Personen sind willkommen.",
 pickup_time="Innerhalb von 7 Tagen · Express nach 3 Tagen für 2 € Aufpreis pro Stück · Versand gegen Aufpreis möglich",
 special_events="Geburtstage, Firmenfeiern und Abschlussfeiern für Gruppen ab 6 Personen, bei Bedarf mit früherer oder späterer Öffnung nach Absprache. Reservierung wird empfohlen, spontan vorbeikommen geht, solange Plätze frei sind.",
 hat_instagram=INS("keramikcafe"),hours="Mo, Di geschlossen, Mi–Fr 11–18 Uhr, Sa, So 10–20 Uhr")
mk(0,"keramik-kitchen-braunschweig","Keramik Kitchen","Braunschweig",NI,"info@keramikkitchen.de",hours="",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Termine reservierst du über den Kalender, der bis zu fünf Monate im Voraus buchbar ist.",
 special_events="Kindergeburtstage, Junggesellinnenabschiede, Betriebsausflüge und Weihnachtsfeiern. Keramikmalen bei Kindergeburtstagen zu Hause ist ebenfalls möglich.",
 description="Keramikmalstudio in Braunschweig, in dem du Keramik selbst bemalst. Termine reservierst du online im Kalender, auch für Kindergeburtstage, JGA und Firmenfeiern.")
mk(6,"keramik-cafe-harz-goslar","Keramik Café Harz Goslar","Goslar",NI,"gs@keramik-cafe-harz.de",**KC,
 description="Kleines Keramikmalstudio in der Goslarer Innenstadt. Du wählst einen Rohling und bemalst ihn selbst, Glasur und Brand sind im Preis enthalten. Reservierung wird empfohlen, spontan geht es bei freien Plätzen.")
mk(7,"keramik-cafe-harz-salzgitter","Keramik Café Harz Salzgitter","Salzgitter",NI,"sz@keramik-cafe-harz.de",addr="In den Blumentriften 27, 38226 Salzgitter",**KC,
 description="Keramikmalstudio in Salzgitter-Lebenstedt, Schwesterstudio des Keramik Cafés in Goslar. Du bemalst einen Rohling selbst, Glasur und Brand sind im Preis enthalten. Reservierung wird empfohlen.")
mk(9,"lieblingstasse-keramikstudio-wolfenbuettel","Lieblingstasse Keramikstudio","Wolfenbüttel",NI,"info@lieblingstasse-keramik.de",
 hours="Mo, Di geschlossen, Mi–Fr 14:30–19 Uhr, Sa 12–19 Uhr, So 12–16:30 Uhr",
 tags="reservation-empfohlen, birthday-parties, hen-party, corporate-events",price_from="16",
 studio_fee="Keine Zusatzgebühr · 2 Stunden Kreativ- und Malzeit",
 price_note="Beispielpreise für Tassen, Teller oder Müslischalen: 16–26 €. Rohkeramik, Farben, Malutensilien, Glasieren und Brennen sind im Preis enthalten. Plätze buchst du online.",
 special_events="Kindergeburtstage, Junggesellenabschiede, Teamtage und Auftragsarbeiten. Für Gruppen ab 10 Personen öffnet das Studio außerhalb der Öffnungszeiten.",
 hat_instagram=INS("lieblingstasse_keramik_bemalen"),
 description="Keramikstudio in Wolfenbüttel, in dem du Rohkeramik nach Wahl bemalst. Du hast 2 Stunden Mal- und Kreativzeit, Farben, Glasur und Brand sind im Preis enthalten. Plätze buchst du online.")
mk(10,"tuschbar-rostock","Tuschbar","Rostock",MV,"kontakt@tuschbar.de",
 hours="Mo, So geschlossen, Di, Mi 13–19 Uhr, Do, Fr 12–20 Uhr, Sa 11–18 Uhr",
 tags="reservation-empfohlen",price_from="10.50",
 studio_fee="Keine Zusatzgebühr · ca. 2,5 Stunden Malzeit · Farben, Werkzeug, Glasur und Brand inklusive",
 price_note="Die Rohlinge kosten etwa 10,50 bis 46,50 € je nach Größe, Form und Fassungsvermögen. Reservierung ist besonders für Samstage, Ferien und Gruppen ab 5 Personen dringend empfohlen, idealerweise 6–8 Wochen im Voraus. Es gibt eine Warteliste.",
 pickup_time="Nach ca. 7 Tagen",
 special_events="Gruppen ab 5 Personen, Klassenausflüge und Malen@home (Keramik zum Bemalen für zuhause). Feste Malzeiten, etwa Di und Mi 13–15:30 oder 16–18:45 Uhr.",
 hat_instagram=INS("tuschbar_rostock"),
 description="Keramik-Malstudio in Rostock, in dem du in etwa 2,5 Stunden einen Rohling bemalst. Farben, Glasur und Brand sind im Preis enthalten. Eine Reservierung wird dringend empfohlen, vor allem am Samstag und in den Ferien.")
mk(11,"hej-pottery-rostock","Hej Pottery","Rostock",MV,"info@hej-pottery.de",
 tags="reservation-only",studio_fee="2,5 Stunden frei bemalen",
 price_note="Preise stehen nicht auf der Website. Reserviert wird über die Seite «Reservierungen».",
 pickup_time="Nach 1–4 Tagen",
 special_events="Gruppen sind willkommen, die Website nennt Schulen, Kitas, Firmen und Workshops.",
 description="Keramikmalstudio in Rostock für eine kreative Auszeit. Du bemalst Keramik 2,5 Stunden lang frei, das Studio glasiert und brennt deine Stücke. Plätze reservierst du über die Website.")
mk(25,"keramikon-hannover","Keramikon","Hannover",NI,"hallo@keramikon-linden.de",
 hours="Mo, Do, Fr 16–19 Uhr, Sa 10–13 und 15–18 Uhr, So 12–15 Uhr, Di, Mi geschlossen",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Online-Buchung wird empfohlen, spontan vorbeikommen geht, solange Plätze frei sind.",
 pickup_time="Nach etwa einer Woche · feste Abholzeiten stehen auf der Website",
 special_events="Workshops, Kindergeburtstage, JGA und Geburtstage sowie Firmen- und Teamevents.",
 hat_instagram=INS("keramikon_linden"),
 description="Kreativstudio in Hannover-Linden, in dem du Keramik bemalst, ohne Vorkenntnisse. Du bekommst eine kurze Einführung in die Farben, nach etwa einer Woche ist dein Stück glasiert und gebrannt. Online buchen wird empfohlen.")
mk(26,"keramikmalstudio-malzeit-hannover","Keramikmalstudio MalZeit","Hannover",NI,"info@malzeit-hannover.de",
 hours="Mo, Di geschlossen, Do, Fr 14–19 Uhr, Sa 11–14 und 15–18 Uhr, So 11–14 Uhr, Mi nur Abendmalen an angekündigten Terminen",
 tags="reservation-empfohlen, birthday-parties, hen-party, corporate-events",
 price_note="Einzelpreise stehen nicht auf der Website. Farben, Malhilfsmittel, Glasur und Brand sind im Preis enthalten.",
 pickup_time="Abholung zu festen Zeiten, Do und Fr 16–18 Uhr, Sa 12–14 und 16–18 Uhr, So 12–14 Uhr",
 special_events="Kindergeburtstage, Junggesellinnenabschiede, private Feiern und Firmenevents sowie Abendmalen an angekündigten Mittwochen.",
 hat_instagram=INS("malzeithannover"),
 description="Keramikmalstudio an der Podbielskistraße in Hannover, seit 2013. Du suchst dir aus vielen Rohlingen etwas aus und bemalst es in Ruhe, Glasur und Brand sind inklusive. Reservierung wird erbeten, auch kurzfristig.")
mk(91,"porzellancafe-suedstadt-hannover","Porzellancafé Südstadt","Hannover",NI,"suedstadt@porzellancafe.de",addr="Dieckmannstraße 1, 30171 Hannover",
 hours="Mo, Di geschlossen, Mi, Fr 14–19 Uhr, Do 10–19 Uhr, Sa, So 11–14 und 15–18 Uhr",
 tags="reservation-only, birthday-parties, hen-party, corporate-events",price_from="20",price_mug="20",price_plate="20",
 studio_fee="Mindestumsatz 22 € pro Person · ca. 3 Stunden",
 price_note="Eine Tasse kostet etwa 20 €, ein klassischer Frühstücksteller (21 cm) ebenfalls 20 €. Farben, Hilfsmaterial, Glasur und Brennen sind im Preis enthalten. Das Porzellancafé hat Standorte in der Südstadt und in der List sowie Malen@Home zum Mitnehmen.",
 pickup_time="Ca. 7 Tage · Abholtermin wird am Maltag genannt, Abholzettel (oder Foto) mitbringen",
 special_events="Geburtstagsfeiern, JGA, Betriebsfeiern und «Langes Malen bis 22 Uhr» an bestimmten Terminen (12.11., 26.11. und 10.12.2026). Eine Tischreservierung über das Buchungstool wird vorab erbeten.",
 hat_instagram=INS("porzellancafe"),
 description="Keramik zum Selbstbemalen in der Hannoveraner Südstadt, mit spülmaschinenfesten Tellern, Tassen und Schalen. Zweiter Standort des Porzellancafés neben der List. Einen Tisch reservierst du vorab über das Buchungstool.")
mk(27,"nadel-und-pinsel-hannover","Nadel und Pinsel","Hannover",NI,"info@nadelundpinsel.de",addr="In der Rehre 24, 30457 Hannover",hours="",
 tags="reservation-only",studio_fee="Maltermine von 3 Stunden",
 price_note="Preise stehen nicht auf der Website. Für die Maltermine ist eine Anmeldung nötig.",
 special_events="Neben Keramik bemalen gibt es Handarbeits- und Kreativworkshops, zum Beispiel Stricktreff und Ferienaktionen, sowie den Menüpunkt «Events».",
 hat_instagram=INS("nadel_pinsel"),
 description="Keramikmalstudio und Treffpunkt für Kreativworkshops in Hannover-Wettbergen, dazu ein Fachgeschäft für Handarbeit. Die Maltermine dauern jeweils 3 Stunden, Anmeldung ist nötig.")
mk(37,"malhafen-luebeck","Malhafen Lübeck","Lübeck",SH,"moin@malhafen.de",addr="Hüxstraße 24, 23552 Lübeck",
 hours="Mo geschlossen, Di–Do 13–18 Uhr, Fr 13–21 Uhr, Sa 11–19:30 Uhr, So 11–16:30 Uhr, an Feiertagen geschlossen",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="15",
 studio_fee="Mindestumsatz 20 € Keramik pro Person · Malplatz und Einweisung inklusive · Gruppen bis 2,5 Stunden",
 price_note="Becher und Tassen 18–30 €, Teller und Platten 15–69 €, Schalen und Schüsseln 15–69 €, Dosen und Spardosen 15–49 €, Vasen 15–49 €, Sticker und Figuren 3,50–18 €.",
 pickup_time="Nach ca. 10–21 Tagen, je nach Saison · feste Abholzeiten stehen auf der Website",
 special_events="Kindergeburtstage ab 10 Jahren, Junggesellinnenabschied, Firmenveranstaltungen, Teambuilding und Weihnachtsfeiern. Studio kann exklusiv gemietet werden, mobiles Pop-up-Event und Zuhause-Sets sind möglich. Online buchen bis 5 Personen, größere Gruppen per Anfrage.",
 hat_instagram=INS("malhafen.keramik_bemalen"),
 description="Keramikmalstudio in der Lübecker Hüxstraße. Du bemalst eine Tasse, einen Teller oder eine Schale selbst, der Malplatz und die Einweisung sind im Keramikpreis enthalten. Du kannst online buchen oder spontan vorbeischauen.")
mk(52,"porzellanmagie-osnabrueck","Porzellanmagie","Osnabrück",NI,"",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Die Inhaberin Maren Lieder glasiert und brennt deine Stücke. Wegen hoher Nachfrage sind viele Tage ausgebucht, es gibt eine Warteliste.",
 special_events="Veranstaltungen und Gutscheine, Einzelheiten stehen auf der Website.",
 description="Kleines Keramikmalatelier im Osnabrücker Westerberg. Du bemalst Keramik selbst, auch ohne Vorkenntnisse, das Glasieren und Brennen übernimmt das Atelier. Die Nachfrage ist hoch, daher wird früh reserviert.")
mk(57,"keramik-und-mosaik-kiel","Keramik und Mosaik","Kiel",SH,"",addr="Kämpenstraße 2, 24106 Kiel",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party",
 price_note="Preise stehen nicht auf der Startseite. Tische reservierst du vorab, gelegentlich werden Plätze spontan frei.",
 special_events="Kindergeburtstage und JGA, außerdem Keramik to go und Mosaik.",
 description="Keramik- und Mosaikstudio in Kiel-Wik, in dem du Rohkeramik selbst bemalst. Einen Tisch reservierst du vorab. Es gibt auch Keramik to go sowie Angebote für Kindergeburtstage und JGA.")
mk(69,"maleo-keramik-studio-bad-schwartau","maleo Keramik Studio","Bad Schwartau",SH,"maleo-keramik@gmx.de",hours="",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="12",
 studio_fee="Keine Buchungsgebühr · 2 Stunden pro Termin",
 price_note="Keramik kostet je nach Größe und Form etwa 12 bis 45 €, Material, Glasur und Brand sind inklusive. Bezahlt wird vor Ort. Termine stehen im Buchungstool und tagesaktuell auf Instagram.",
 pickup_time="Etwa 2 Wochen nach dem Bemalen",
 special_events="JGA, Babyparty und Geburtstage, Firmenfeiern und Teamevents sowie Kindergeburtstage.",
 hat_instagram=INS("maleo.keramik"),
 description="Keramikmalstudio in Bad Schwartau bei Lübeck. Du buchst online eine Malsession von 2 Stunden und bezahlst nur die Keramik vor Ort, Material, Glasur und Brand sind inklusive.")
mk(70,"atelier-am-see-ratzeburg","Atelier am See","Ratzeburg",SH,"hej@dasatelieramsee.com",addr="Schloßwiese 3, 23909 Ratzeburg",
 hours="Fr 15–20:30 Uhr, Sa 11–16:30 Uhr, zwei Sonntage pro Monat 11–16:30 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, corporate-events",price_from="7",
 studio_fee="Mindestumsatz 25 € pro Person und Reservierung · 2,5 Stunden",
 price_note="Fliesen, Schilder und Vasen 7–18 €, Schalen 10–50 €, Becher und Tassen 20–29 €, Teller und Platten 19–49 €, Krüge 39–59 €. Farbe, Werkzeug, Einführung, Glasur und Brand sind inklusive. Bezahlt wird vor Ort per Karte.",
 pickup_time="In der Regel etwa 1 Woche nach dem Besuch · Versand für Urlauber möglich",
 special_events="Kindergeburtstage (30–39 € je nach Tag und Paket, nur mit Vorkasse), Teamevents, Firmenfeiern und Geburtstage für 20–30 Personen. Dazu Aufbau-Töpfern mittwochs 18–20:30 Uhr.",
 hat_instagram=INS("dasatelieramsee"),
 description="Mal-Atelier direkt am Ratzeburger See neben dem Strandbad. Du reservierst online einen Malplatz für 2,5 Stunden, Farbe, Glasur und Brand sind im Preis enthalten. Dazu gibt es Aufbau-Töpfern und Events.")
mk(32,"studio-paula-keramik-goettingen","Studio Paula Keramik","Göttingen",NI,"paula-keramik@gmx.de",
 hours="Mo geschlossen, Di, Sa 11–17 Uhr, Mi–Fr 11–18 Uhr",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Du wählst aus ausgewählten Rohlingen, meist Geschirr aus Steingut oder handgemachtem Steinzeug. Plätze buchst du online.",
 hat_instagram=INS("paula_keramik"),
 description="Keramikstudio in der Göttinger Innenstadt, in dem du ausgewählte Rohlinge bemalst. Du wählst Geschirr aus Steingut oder handgemachtem Steinzeug und buchst deinen Platz online.")
mk(92,"paint-your-style-goettingen","Paint your Style Göttingen","Göttingen",NI,"",
 tags="kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen auf der Standortseite nicht. Reservierung online, für Gruppen ab 6 Personen per Formular.",
 pickup_time="Ca. 1–3 Tage (allgemeine Angabe der Paint-your-Style-Website)",
 special_events="Kindergeburtstage, Junggesellenabschiede, Schul- und Kita-Ausflüge sowie Firmenfeiern.",
 hat_instagram=INS("goettingenpaintyourstyle"),
 description="Malstudio für Ideen auf Keramik in der Göttinger Innenstadt. Du suchst dir Keramik aus, bemalst sie selbst, und das Team glasiert und brennt sie. Reservierung online.")
mk(82,"glanzstueck-keramik-malstudio-melle","Glanzstück Keramik-Malstudio","Melle",NI,"",
 tags="reservation-only",
 price_note="Preise und Ablauf stehen nicht auf der Buchungsseite.",
 description="Keramik-Malstudio in Melle bei Osnabrück. Plätze werden online gebucht, Preise und Ablauf nennt die Buchungsseite nicht.")
json.dump(raw,open(p,'w'),ensure_ascii=False,indent=2)
print(len(d))
