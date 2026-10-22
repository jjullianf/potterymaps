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
SH="SH"
mk(40,"sylt-keramik-westerland","Sylt Keramik","Westerland",SH,"malen@syltkeramik.de",addr="Strandstraße 5, 25980 Westerland",hours="",
 tags="reservation-empfohlen, kids-friendly",price_from="9",
 studio_fee="Meist 2 Stunden · Einführung, Farben, Pinsel, Stempel und Siebdruckfolien inklusive",
 price_note="Rohlinge kosten 9–59 €, die meistgewählten Teile (Tassen, Schälchen, kleine Teller) 20–25 € all inclusive. Mehr als 400 Rohkeramiken. Lange Malabende Di, Mi und Do 20–23 Uhr nur mit Terminbuchung, Eintritt 10 € zuzüglich Keramik.",
 pickup_time="Meist am nächsten Öffnungstag ab 18 Uhr",
 special_events="Lange Malabende mit Getränken, Snacks und Musik sowie die KeramikMalBox zum Bemalen zu Hause.",
 hat_instagram=INS("syltkeramik"),
 description="Keramikatelier in Westerland auf Sylt mit über 400 Rohkeramiken. Du bemalst etwa 2 Stunden, meist am nächsten Öffnungstag ab 18 Uhr ist dein Stück gebrannt. Dazu gibt es lange Malabende und eine KeramikMalBox.")
json.dump(raw,open(p,'w'),ensure_ascii=False,indent=2)
print(len(d))
