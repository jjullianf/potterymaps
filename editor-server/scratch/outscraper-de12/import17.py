import json,sys,io,contextlib,re
sys.path.insert(0,'editor-server/scratch/outscraper-de3')
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_report3 as b
hours_de=b.hours_de
G=json.load(open('/tmp/geo5.json'))
def R(k,street,plz,phone,web):
    return {'name':k,'address':'','street':street,'postal_code':plz,'phone':phone,'website':web,'latitude':G[k][0],'longitude':G[k][1],'working_hours':'None'}
RAW=[R('aichach','Werlberger Straße 7','86551','','https://www.atelierfriendsco.de/'),
 R('pruem','Teichstraße 6','54595','+49 151 46489652','https://mal-bank.de/pruem'),
 R('mett','Im Fronhof 4','54675','+49 1575 2228742','https://mal-bank.de/mettendorf'),
 R('hx','Am Markt 8','37671','+49 5271 9510020','https://keramikbemalen-hx.de/'),
 R('fds','Loßburger Straße 20','72250','+49 171 8229622','https://www.porzellinchen.de/')]
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
BY,RP,NW,BW="BY","RP","NW","BW"
mk(0,"atelier-friends-und-co-aichach","Atelier Friends & Co.","Aichach",BY,"info@atelierfriendsco.de",addr="Werlberger Straße 7, 86551 Aichach",
 hours="Mo, So geschlossen, Di, Mi, Fr 10–12 und 13–18 Uhr, Do 10–12 und 13–20 Uhr, Sa 10–19 Uhr",
 tags="reservation-empfohlen, kids-friendly, birthday-parties, hen-party",
 price_note="All-inclusive-Preis mit Keramik, Farben, Hilfsmitteln, Glasieren und Brennen. Eine Müslischüssel kostet zum Beispiel ca. 17 €. Das Studio arbeitet mit Reservierungen, spontan vorbeischauen geht mit Glück, ein Platz ist nicht garantiert. Dazu gehört ein Concept Store mit regionalen Marken.",
 pickup_time="Nach ca. 14 Tagen im Atelier",
 special_events="Kindergeburtstag (24 € pro Gast) sowie Geburtstage, JGA und andere Anlässe, auch für exklusive Runden.",
 hat_instagram=INS("atelier_friendsco"),
 description="Keramikstudio mit Concept Store in Aichach. Du reservierst online einen Platz, wählst vor Ort ein Stück und bemalst es. Nach etwa 14 Tagen ist dein Stück glasiert, gebrannt und abholbereit.")
MB=dict(tags="reservation-empfohlen, kids-friendly, birthday-parties, corporate-events",price_from="15",
 studio_fee="Meist ca. 2–3 Stunden · Farben, Pinsel, Material, Glasur und Brand inklusive",
 price_note="Rohlinge kosten ab ca. 15 €, nach oben offen. Reservierung über die Buchungs-App oder per WhatsApp, spontan vorbeikommen geht manchmal, dann vorher anrufen. Kinder sind ab ca. 3 Jahren willkommen, der Zugang ist barrierefrei. Bemalen zu Hause mit Sets ist möglich.",
 pickup_time="In der Regel nach etwa 10 Tagen (1–2 Wochen) · Versand auf Wunsch",
 special_events="Feste feiern, Gruppen bis 30 Personen (ab 10 Personen auch außerhalb der Öffnungszeiten), Technikabende und Workshops.",
 hat_instagram=INS("diemalbank"))
mk(1,"mal-bank-pruem","Mal-Bank Prüm","Prüm",RP,"pruem@mal-bank.de",addr="Teichstraße 6, 54595 Prüm",
 hours="Mo, Di Ruhetag (außer in den Ferien), Mi–Fr 14:30–18 Uhr, Sa, So 10–13 und 14:30–18 Uhr, lange Donnerstage bis 21 Uhr am 12.11. und 26.11.2026",**MB,
 description="Keramikmalstudio am Teichplatz in Prüm, Filiale der Mal-Bank aus Mettendorf, eröffnet am 1. Oktober 2026. Du reservierst einen Platz, wählst einen Rohling und bemalst ihn, Glasur und Brand sind im Preis enthalten.")
mk(2,"mal-bank-mettendorf","Mal-Bank Mettendorf","Mettendorf",RP,"info@mal-bank.de",addr="Im Fronhof 4, 54675 Mettendorf",hours="Lange Donnerstage bis 21 Uhr am 19.11.2026, sonst nach Reservierung",**MB,
 description="Keramikmalstudio in Mettendorf in der Südeifel, Hauptstandort der Mal-Bank mit Filiale in Prüm. Du reservierst einen Platz, bemalst einen Rohling, nach etwa 10 Tagen ist er gebrannt und abholbereit.")
mk(3,"schoengekuesst-keramikmalwerkstatt-hoexter","Schöngeküsst Keramikmalwerkstatt","Höxter",NW,"heike@keramikbemalen-hx.de",addr="Am Markt 8, 37671 Höxter",hours="",
 tags="reservation-empfohlen, kids-friendly",
 studio_fee="Mindestmalumsatz 20 € pro Person (25 € bei Sonderterminen), wird mit der Keramik verrechnet · ein Malslot dauert etwa 3 Stunden",
 price_note="Einzelpreise stehen im Keramikkatalog. Die 20 € werden bei der Buchung als Vorkasse fällig. Ein zusätzlicher Malslot zum Fertigstellen ist einmal kostenfrei, jeder weitere kostet 20 €. Kostenlose Stornierung bis 48 Stunden vorher. Kinder unter 12 Jahren brauchen eine erziehungsberechtigte Begleitung. Eigene Schablonen und Zeichnungen dürfen mitgebracht werden.",
 pickup_time="Nach etwa 14 Tagen mit Abholschein · fertige Keramik wird bis zu 8 Wochen aufbewahrt",
 special_events="Gutscheine ab 20 € und Keramik-Malkoffer zum Bemalen zu Hause. Kinder, Erwachsene und Gruppen sind willkommen.",
 hat_instagram=INS("schoengekuesst"),
 description="Keramikmalwerkstatt am Markt in Höxter, seit der Eröffnung als Keramik-Mal-Café beliebt. Ein Malslot dauert etwa 3 Stunden, es gilt ein Mindestmalumsatz von 20 € pro Person. Nach etwa 14 Tagen ist dein Stück abholbereit.")
mk(4,"porzellinchen-freudenstadt","Porzellinchen Freudenstadt","Freudenstadt",BW,"info@porzellinchen.de",addr="Loßburger Straße 20, 72250 Freudenstadt",hours="",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Termine buchst du über den Buchungskalender, es gibt keine festen Öffnungszeiten. Das Studio hat am 11. Oktober 2026 eröffnet und ist der zweite Standort neben Öschelbronn.",
 special_events="Kindergeburtstage, Firmenevents und Junggesellenabschiede auf Anfrage per E-Mail oder WhatsApp.",
 description="Zweiter Standort des Keramikmalstudios Porzellinchen, eröffnet im Oktober 2026 in Freudenstadt. Du buchst über den Kalender einen freien Termin, es gibt keine festen Öffnungszeiten.")
json.dump(raw,open(p,'w'),ensure_ascii=False,indent=2)
print(len(d))
