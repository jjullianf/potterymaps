import json,sys,io,contextlib,re
sys.path.insert(0,'editor-server/scratch/outscraper-de3')
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_report3 as b
hours_de=b.hours_de
RAW=json.load(open('editor-server/scratch/outscraper-de12/_raw_dump.json',encoding='utf-8'))['N']
RAW.append({'name':'TWENTYWAYSOUT Obertshausen','address':'Kapellenstraße 2, 63179 Obertshausen','street':'Kapellenstraße 2','postal_code':'63179','phone':'+49 177 6770191','website':'https://www.twentywaysout.de/','latitude':'50.0832670','longitude':'8.8667368','working_hours':'None'})
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
BY,NI,HE,NW,BW="BY","NI","HE","NW","BW"
TW=dict(tags="reservation-only, kids-friendly, birthday-parties",
 studio_fee="5 € pro Person · Keramik wird separat berechnet · feste Malzeiten (ca. 2,5 Stunden) · bis 15 Personen online buchbar",
 pickup_time="Nach 10 bis 14 Tagen, samstags",hat_instagram="",
 special_events="Keramik bemalen für Groß und Klein, Events und Gruppen. Das Studio hat Standorte in Hanau, Obertshausen und Aschaffenburg.")
mk(143,"twentywaysout-hanau","TWENTYWAYSOUT Hanau","Hanau",HE,addr="Krämerstraße 8, 63450 Hanau",
 hours="Mi–Fr Malzeiten 15:30 und 18:30 Uhr, Sa 12, 15 und 18 Uhr, So 10 und 15 Uhr, Mo und Di geschlossen",**TW,
 price_note="Die Keramik wird separat berechnet, dazu kommen 5 € pro Person. Abholung samstags (Wintersaison 12–21 Uhr, Sommersaison 12–18 Uhr), unter der Woche nur für gebuchte Kurse geöffnet.",
 description="Keramik-Malstudio in der Hanauer Innenstadt. Du buchst online eine Malzeit mit festen Zeiten Mittwoch bis Sonntag, nach 10 bis 14 Tagen ist dein Stück abholbereit.")
mk(77,"twentywaysout-aschaffenburg","TWENTYWAYSOUT Aschaffenburg","Aschaffenburg",BY,addr="Roßmarkt 34, 63739 Aschaffenburg",
 hours="Do, Fr Malzeiten 15:30 und 18:30 Uhr, Sa 12, 15 und 18 Uhr, So 10 und 15 Uhr, Mo–Mi geschlossen",**TW,
 price_note="Die Keramik wird separat berechnet, dazu kommen 5 € pro Person. Abholung samstags ab 11 Uhr, unter der Woche nur für gebuchte Kurse geöffnet.",
 description="Keramik-Malstudio am Roßmarkt in Aschaffenburg. Du buchst online eine Malzeit mit festen Zeiten Donnerstag bis Sonntag, nach 10 bis 14 Tagen ist dein Stück abholbereit.")
mk(len(RAW)-1,"twentywaysout-obertshausen","TWENTYWAYSOUT Obertshausen","Obertshausen",HE,addr="Kapellenstraße 2, 63179 Obertshausen",
 hours="Fr Malzeiten 15:30 und 18:30 Uhr, Sa 12 und 15 Uhr, So 10 und 15 Uhr, Mo–Do geschlossen",
 **{**TW,"studio_fee":"5 € pro Person · Keramik wird separat berechnet · feste Malzeiten (ca. 2,5 Stunden) · bis 5 Personen online buchbar"},
 price_note="Die Keramik wird separat berechnet, dazu kommen 5 € pro Person. Abholung samstags 12–17:30 Uhr, unter der Woche ist das Studio geschlossen. Das Studio liegt im Kapellenhof.",
 description="Keramik-Malstudio im Kapellenhof in Obertshausen. Du buchst online eine Malzeit von Freitag bis Sonntag, nach 10 bis 14 Tagen ist dein Stück abholbereit.")
mk(10,"anker-geschirr-cuxhaven","Anker Geschirr","Cuxhaven",NI,hours="Nach Terminvereinbarung",addr="Am Feuerberg 6, 27476 Cuxhaven",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Du wählst dein Lieblingsteil und bemalst es mit eigenen Ideen oder Vorlagen. Termine nur nach Vereinbarung per Telefon (0160 90290825) oder E-Mail.",
 description="Atelier in Cuxhaven-Sahlenburg, in dem du ein Lieblingsteil aus Keramik auswählst und selbst bemalst. Termine gibt es nur nach telefonischer oder schriftlicher Vereinbarung.")
mk(85,"machbar-keramikstudio-kempten","MACHBAR Kreativ- und Keramikstudio","Kempten",BY,addr="Scheibenstraße 3, 87435 Kempten",
 hours="Mo–Fr 10:30–19 Uhr, Sa 10–18:30 Uhr",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Buchungsseite. Du buchst online über machbar.malplatz.info, telefonisch (0831 52622689) oder über das Kontaktformular. Das Studio gehört zu Hobby Lill.",
 description="Kreativ- und Keramikstudio in Kempten im Allgäu, in dem du Keramik bemalst. Termine buchst du online, telefonisch oder über das Kontaktformular.")
mk(91,"keramik-atelier-ochsenhausen","Keramik Atelier Ochsenhausen","Ochsenhausen",BW,
 tags="walk-in",
 price_note="Der Preis ist all-inclusive und enthält Keramik, Farben, Werkzeug, Glasur und Brand. Du wählst vor Ort ein Stück, Vorkenntnisse sind nicht nötig. Nicht abgeholte Stücke werden höchstens 2 Monate aufbewahrt.",
 description="Keramikatelier in Ochsenhausen, in dem du ein Stück auswählst und selbst bemalst. Glasur und Brand übernimmt das Atelier, der Preis ist all-inclusive.")
mk(111,"die-handwerkstatt-by-saskia-bergisch-gladbach","Die Handwerkstatt by Saskia","Bergisch Gladbach",NW,hours="",
 tags="reservation-only",price_from="21",
 studio_fee="Workshop «Keramik bemalen» 21 € · 2 Stunden 30 Minuten",
 price_note="Die Buchung läuft online über die Website. Ob die Rohlinge vor Ort gestellt werden, steht nicht auf der Seite.",
 description="Handwerkstatt in Bergisch Gladbach mit dem Workshop «Keramik bemalen» (21 €, 2,5 Stunden), den du online buchst.")
mk(137,"toepferwelt-handkraft-fuerholzen","Töpferwelt Handkraft","Fürholzen",BY,addr="Hetzenhauser Straße 9a, 85376 Fürholzen",hours="",
 tags="reservation-only",
 price_note="Die Website bietet Workshops «Keramik selbst bemalen» und Malboxen zum Bemalen zu Hause. Preise stehen auf den Unterseiten.",
 special_events="Workshops zum Keramik selbst bemalen und Malboxen für zu Hause.",
 description="Töpferwelt in Fürholzen bei Freising mit Workshops, in denen du Keramik selbst bemalst, sowie Malboxen für zu Hause.")
json.dump(raw,open(p,'w'),ensure_ascii=False,indent=2)
print(len(d))
