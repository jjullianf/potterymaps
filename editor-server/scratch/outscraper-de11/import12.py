import json,sys,io,contextlib,re
sys.path.insert(0,'editor-server/scratch/outscraper-de3')
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_report3 as b
hours_de=b.hours_de
RAW=json.load(open('editor-server/scratch/outscraper-de11/_raw_dump.json',encoding='utf-8'))['N']
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
BW,NW,RP,HE="BW","NW","RP","HE"
mk(2,"myfarah-keramik-malstudio-sindelfingen","MYFARAH Keramik-Malstudio","Sindelfingen",BW,
 tags="reservation-only, kids-friendly, birthday-parties, hen-party",
 price_note="Preise stehen nicht auf der Website. Reserviert wird online über den Button «Reservieren».",
 pickup_time="Nach ca. 2 Wochen · Keramik wird höchstens 3 Monate aufbewahrt",
 special_events="Afterwork, Paint Your Sound, Baby-Fußabdrücke, Junggesellenabschied, Kindergeburtstag sowie Angebote für Senioren und Schulen.",
 description="Keramik-Malstudio in der Sindelfinger Innenstadt. Du reservierst online, nach etwa 2 Wochen ist dein Stück glasiert und gebrannt. Es gibt Events wie Afterwork und Paint Your Sound sowie Angebote für JGA und Kindergeburtstage.")
mk(3,"ton-form-werkstatt-boeblingen","Ton Form Werkstatt","Böblingen",BW,"info@tonformwerkstatt.de",hours="",
 price_note="Preise stehen nicht auf der Startseite. Die Website bietet einen Workshop «Keramik selbst bemalen» an.",
 hat_instagram=INS("tonformwerksatt"),
 description="Keramikwerkstatt in Böblingen mit Workshops, darunter «Keramik selbst bemalen».")
mk(7,"lauter-atelier-kaiserslautern","Lauter Atelier","Kaiserslautern",RP,"info@lauteratelier.de",
 hours="Mo geschlossen, Di, Fr 15:15–18 und 18:15–21 Uhr, Mi, Do 10–12:45, 15:15–18 und 18:15–21 Uhr, Sa 10:15–13, 13:15–16 und 16:15–19 Uhr, außerdem nach Vereinbarung",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="14",
 price_note="Der Preis richtet sich nach dem Rohling, zur Orientierung kostet eine Tasse ca. 14 € und eine große Schüssel ca. 34 €. Reservierung über die Website, spontan geht es je nach Verfügbarkeit.",
 pickup_time="Abholung zu festen Zeiten, Di 16–17:30 und 19–20:30 Uhr, Mi 10:30–12:30 Uhr, Do 10:30–12:30, 16–17:30 und 19–20:30 Uhr, Fr 16–17:30 Uhr, Sa 11–12:30 und 14–15:30 Uhr",
 special_events="Kreativ feiern (JGA, Geburtstage, Betriebs- und Weihnachtsfeiern), Babyshower, Kindergeburtstage, Teambuilding, Töpferkurse, Keramik-Kiste und mobile Keramikworkshops für Schulen und Kindergärten.",
 hat_instagram=INS("lauteratelier.de"),
 description="Keramikatelier in Kaiserslautern mit festen Mal-Zeitfenstern. Du bemalst Tassen, Teller, Schalen und andere Rohlinge, reservierst online oder kommst spontan, wenn Platz frei ist.")
mk(12,"toepfertante-goeppingen","Töpfertante Göppingen","Göppingen",BW,"info@goeppingen.toepfertante.com",
 hours="Mo, Di geschlossen, Mi 14:30–17 Uhr, Do, Fr 14:30–19:45 Uhr, Sa 10–18:15 Uhr, So 11–16:15 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Termine buchst du online.",
 pickup_time="Nach 1–2 Wochen, spätestens 4 Wochen nach dem Bemaltermin abholen · Abholung Fr 15–17 Uhr und Sa 10:30–16 Uhr",
 special_events="Kindergeburtstage, Junggesellinnenabschiede, Teamevents, Babyshowerpartys und Weihnachtsfeiern.",
 description="Keramikmalstudio in der Göppinger Innenstadt, Schwesterstudio der Töpfertante in Esslingen. Termine buchst du online, nach 1 bis 2 Wochen ist dein Stück gebrannt.")
mk(32,"dorfkeramik-kierspe","Dorfkeramik","Kierspe",NW,hours="",
 tags="reservation-only",price_from="10",
 studio_fee="Anmeldegebühr 6,90 € bei der Anmeldung",
 price_note="Keramik kostet 10–65 €. Die meisten Sessions gibt es nur nach Terminbuchung online.",
 pickup_time="Etwa 7 Tage nach dem Malen, den genauen Termin bekommst du per E-Mail",
 special_events="Malsessions zu festen Terminen, Privatevents und Ladies Night (10 € Gebühr inklusive Getränk).",
 hat_instagram=INS("dorf_keramik"),
 description="Keramikmalstudio in Kierspe im Sauerland. Du buchst eine Session online, bemalst dein Stück und bekommst nach etwa 7 Tagen per E-Mail den Abholtermin.")
mk(39,"idyllic-studio-siegen","Idyllic Studio","Siegen",NW,"idilslan@gmail.com",hours="",
 tags="reservation-empfohlen, hen-party, birthday-parties",
 price_note="Preise für das Bemalen stehen nicht auf der Startseite. Bei der Reservierung wählst du ein Zeitfenster (12–14, 14–16, 16–18 oder 19–22 Uhr). Die Website nennt außerdem Keramik2Go, Babybauchschale (149 €) und Wochenend-Töpferkurse (250 €).",
 special_events="Keramik2Go (Keramik zu Hause bemalen), Junggesellenpaket, Geburtstags-Paket, Babybauchschale und Wochenend-Töpferkurs.",
 hat_instagram=INS("idyllic.studios"),
 description="Keramikstudio in der Siegener Innenstadt mit Keramik bemalen, Töpferkursen und Paketen für JGA und Geburtstage. Eine Reservierung wird empfohlen.")
mk(42,"keramali-fulda","Keramali","Fulda",HE,"info@keramali.de",hours="",addr="Horas, 36039 Fulda",
 tags="birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website.",
 special_events="Geburtstagsfeiern, Ladies Night, Gruppen-Events (auch Firmen- und Weihnachtsfeiern) und Junggesellinnenabschied.",
 hat_instagram=INS("_keramali_"),
 description="Keramik zum Selbstbemalen in Fulda-Horas. Die Website nennt Angebote für Geburtstage, Ladies Night, JGA und Gruppenevents.")
mk(49,"dies-und-das-kreativstudio-kredenbach","Dies&Das Kreativstudio","Kreuztal",NW,"studio@diesunddas.design",addr="Altlohe 1, 57223 Kreuztal",hours="",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Reservierung online.",
 pickup_time="Nach 2 Wochen",
 special_events="Geburtstag, Junggesellinnenabschied, Teamevent und Kindergeburtstag.",
 hat_instagram=INS("diesunddas.design"),
 description="Kreativstudio für Keramik im Kreuztaler Ortsteil Kredenbach. Du reservierst online, nach 2 Wochen ist dein bemaltes Stück gebrannt und abholbereit.")
json.dump(raw,open(p,'w'),ensure_ascii=False,indent=2)
print(len(d))
