import json,sys,io,contextlib,re
sys.path.insert(0,'editor-server/scratch/outscraper-de3')
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_report3 as b
hours_de=b.hours_de
RAW=[]
for dd,ii in (("de5",4),("de5",6),("de7",52),("de7",140),("de7",158),("de7",82),("de7",113),("de6",3)):
    RAW.append(json.load(open(f'editor-server/scratch/outscraper-{dd}/_raw_dump.json',encoding='utf-8'))['N'][ii])
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
HH,NW,BW="HH","NW","BW"
mk(0,"studio1200-keramik-selbst-bemalen-hamburg","Studio1200°","Hamburg",HH,addr="Schopstraße 26, 20255 Hamburg",hours="",
 tags="reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Der Preis richtet sich nach der gewählten Keramik. Preise stehen auf der Seite «Preise». Gruppen, Events oder individuelle Terminwünsche per Nachricht.",
 pickup_time="Nach 10 Tagen, zu den Öffnungszeiten · Keramik wird 3 Monate aufbewahrt",
 special_events="Junggesellinnenabschiede, Geburtstage für Klein und Groß, Firmenevents, langer Mädelsabend, Familienfeiern, Babyshower, Workshops und Geschenkgutscheine (nur im Geschäft).",
 description="Malstudio in Hamburg, seit Mai 2023. Du suchst vor Ort eine Keramik aus, bemalst sie mit verschiedenen Techniken, danach glasiert und brennt das Studio dein Stück. Nach 10 Tagen ist es abholbereit.")
mk(1,"keramik-hof-flottbek-hamburg","Keramik Hof Flottbek","Hamburg",HH,"keramikhofflottbek@gmail.com",addr="Dornstückenweg 8, 22607 Hamburg",
 hours="Nov/Dez: Di, Fr 12–18 Uhr (späteste Startzeit 15 Uhr), Sa, So Startzeiten 10:30 und 14:30 Uhr (4–8 Personen) bzw. 11 und 15 Uhr (9–14 Personen)",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="16",
 studio_fee="Maximal 3 Stunden, nicht verlängerbar · Termine nur nach Vereinbarung",
 price_note="Die meisten Rohlinge kosten 16–25 €, im Preis sind Farbe, Aufenthalt und Brennen enthalten. Es gibt mehr als 150 verschiedene Artikel. Kinder sind ab 8 Jahren willkommen. Getränke, Snacks und Kuchen darfst du mitbringen. Das Brennen fremder Keramik ist nicht möglich.",
 special_events="Kindergeburtstage ab 8 Jahren, Junggesellenabschiede, Betriebs- und Weihnachtsfeiern, Fuß- und Handabdrücke der Kleinsten. Platz für 14 Personen in der Werkstatt und 8 im Pavillon.",
 description="Keramikwerkstatt in Hamburg-Flottbek. Du bemalst nach Terminabsprache bis zu 3 Stunden, im Rohlingspreis sind Farbe, Aufenthalt und Brand enthalten. Es gibt über 150 Artikel, in der Werkstatt ist Platz für 14 Personen.")
mk(2,"malunikat-moenchengladbach","MalUnikat","Mönchengladbach",NW,addr="Wallstraße 6, 41061 Mönchengladbach",hours="",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="20",
 studio_fee="150 Minuten Kreativzeit ab 20 € · Begleitpersonen ab 4 Jahren zahlen 20 € Studiogebühr",
 price_note="Rohling, Farben, Pinsel, Materialien und Glanzbrand sind inklusive, es gibt keine Extra-Gebühren. Termine buchst du online, ab 6 Personen telefonisch oder per WhatsApp. Der Tisch wird bis zu 15 Minuten nach dem Termin reserviert. Es gibt eine Warteliste.",
 special_events="Größere Gruppen auch außerhalb der Öffnungszeiten, in den Herbstferien 20 % Rabatt für Schüler und Studierende bis 21 Jahre (Mindestrohlingwert 30 €).",
 description="Keramikmalstudio in Mönchengladbach mit 150 Minuten Kreativzeit ab 20 €. Rohling, Farben, Pinsel und Glanzbrand sind inklusive. Termine buchst du online, ab 6 Personen telefonisch oder per WhatsApp.")
mk(3,"ceramaze-studio-moers","Ceramaze Studio","Moers",NW,hours="",addr="Neustraße 33b, 47441 Moers",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Startseite. Malslots buchst du über ceramaze-malslot.de, Gruppenbuchungen sind möglich. Das Team begleitet dich Schritt für Schritt.",
 description="Keramikstudio in Moers, in dem du Keramik selbst bemalst. Malslots buchst du online, Gruppenbuchungen sind möglich.")
mk(4,"die-tonzeche-krefeld","Die Tonzeche","Krefeld",NW,addr="Lessingstraße 49, 47799 Krefeld",hours="",
 tags="reservation-only",
 price_note="Keramikmalen buchst du über den Online-Shop (tonzeche.sumupstore.com). Es gibt auch einen Malkoffer für zuhause. Weil das Studio keine Angestellten hat, kann es beim Termin Wartezeit geben.",
 description="Keramikstudio in Krefeld, in dem du Keramik bemalst. Du buchst über den Online-Shop, es gibt auch einen Malkoffer für zuhause.")
mk(5,"studio-clay-aachen","Studio CLAY","Aachen",NW,"info@studioclay.de",hours="",
 price_note="Neben Töpferkursen gibt es Angebote zum Keramik bemalen für Anfänger, inklusive Brennen. Preise und Termine stehen auf der Website.",
 description="Keramikstudio in Aachen mit Töpferangeboten und Kursen zum Keramik bemalen mit Glasuren, auch für Anfänger.")
mk(6,"zqtl-ceramics-aachen","ZQTL ceramics","Aachen",NW,hours="",
 price_note="Die Website bietet den Kurs «Keramik bemalen & glasieren» an. Preise und Termine stehen auf der Kursseite.",
 description="Keramikstudio in Aachen mit Töpferkursen und dem Kurs «Keramik bemalen & glasieren».")
mk(7,"ezo-ceramics-muenster","Ezo Ceramics","Münster",NW,hours="",
 tags="reservation-only",price_from="50",
 price_note="Der Workshop «Keramik bemalen» kostet 50 €, mit großer Auswahl und allem inklusive. Er ist in Münster und Rheine buchbar.",
 description="Keramikstudio in Münster mit Töpferkursen und dem Workshop «Keramik bemalen» (50 €, alles inklusive).")
json.dump(raw,open(p,'w'),ensure_ascii=False,indent=2)
print(len(d))
