import json,sys,io,contextlib,re
sys.path.insert(0,'editor-server/scratch/outscraper-de3')
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_report3 as b
hours_de=b.hours_de
RAW=json.load(open('editor-server/scratch/outscraper-de6/_raw_dump.json',encoding='utf-8'))['N']
p='editor-server/data/studios.json'
raw=json.load(open(p)); d=raw if isinstance(raw,list) else raw['studios']
tmpl=[s for s in d if s.get('slug')=='layers-koeln'][0]; keys=list(tmpl.keys())
slugs={s['slug'] for s in d}
INS=lambda u:"ja, https://www.instagram.com/"+u+"/"
def mk(idx,slug,name,city,region,email="",addr=None,hours=None,**kw):
    r=RAW[idx]; assert slug not in slugs,slug
    s={k:"" for k in keys}
    plz=str(r['postal_code']).zfill(5)
    street=(r['street'] or '').replace('Str.','Straße').replace('str.','straße')
    s.update({"slug":slug,"name":name,"address":addr or f"{street}, {plz} {city}","city":city,
      "phone":(r['phone'] or '') if r['phone']!='None' else "","website":re.sub(r'%3F.*','',r['website']) if r['website'] else "","email":email.lower(),
      "opening_hours":hours or hours_de(r['working_hours']),"tags":"","images":"[]","image":"","custom_faq":"[]","contacted":False,"featured":False,
      "quelle_hinweis":"Outscraper (Google Maps); Aufnahme anhand der Website geprüft am 19.10.2026",
      "lat":float(r['latitude']),"lng":float(r['longitude']),"country":"DE","currency":"EUR","postcode":plz,"region":region})
    s.update(kw); slugs.add(slug); d.append(s)
PYS_NOTE="Einzelpreise der Keramik und ein Mindestumsatz stehen auf der Standortseite nicht. Das Zeitfenster um 18 Uhr ist Gästen ab 15 Jahren vorbehalten. Gruppen mit mehr als 5 Personen nutzen ein eigenes Formular."
# ---- Münster
mk(0,"layers-muenster","layers","Münster","NW","",addr="Kanalstraße 30, 48147 Münster",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events", price_from="9", price_mug="21-29", price_plate="23-45",
 studio_fee="4,90 € pro Person · ca. 2 Stunden",
 price_note="Die Studiogebühr enthält Farben, Material, Beratung, Glasieren und Brennen. Rohlinge kosten 9–49 €: Teller ab 23 €, Tassen ab 21 €, Schalen ab 15 €, Vasen ab 19 €. Kaffee und Getränke sind inklusive.",
 pickup_time="Nach ca. 7 Tagen",
 special_events="Gruppen können das Studio exklusiv buchen, zum Beispiel für Teamevents, Geburtstage, JGAs und Weihnachtsfeiern. Kinder ab ca. 4–5 Jahren mit Begleitung eines Erwachsenen, ab ca. 12 Jahren auch allein. Zuhause malen mit Keramik at Home. Eine Reservierung ist erforderlich.",
 hat_instagram=INS("layers.ms"),
 description="Keramik-Bemalstudio im Münsteraner Kreuzviertel. Du bemalst Rohlinge frei Hand, mit Abklebetechnik oder Bubbletechnik, das Team glasiert und brennt sie von Hand. Kaffee und Getränke sind inklusive, Vorkenntnisse sind nicht nötig. Reservierung ist erforderlich.")
mk(2,"keramikmalerei-artcuisine-muenster","Keramikmalerei artcuisine","Münster","NW","keramik@artcuisine.eu",
 tags="reservation-only",
 price_note="Die Preise stehen im Online-Shop und sind Endpreise. Es gibt über 200 Rohlinge. Die Farben sind bleifrei und lebensmittelecht, die fertigen Stücke spülmaschinenfest. Ein Workshop ist nicht nötig.",
 pickup_time="Ca. 4 Wochen nach dem Bemalen, bei viel Betrieb länger",
 special_events="Derzeit nur mit Voranmeldung. Reservierung, Workshops und Abholung über eigene Seiten, montags und dienstags geschlossen.",
 description="Offenes Keramik-Malstudio in der Münsteraner Innenstadt mit über 200 Rohlingen. Du bemalst deinen Rohling, das Studio glasiert und brennt ihn, die Stücke sind danach spülmaschinenfest. Derzeit ist der Besuch nur mit Voranmeldung möglich.")
# ---- Dortmund, Bocholt, Haltern
mk(12,"glasuri-dortmund","GLASURI","Dortmund","NW","info@glasuri.de",addr="Rodenbergstraße 64, 44287 Dortmund",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events", price_from="10", price_plate="20",
 studio_fee="Keine Studiogebühr · Farben, Glasur und Brand inklusive",
 price_note="Keramik ab 10 € (Eierbecher), Frühstücksteller ca. 20 €, große Vasen ca. 45 €. Es gibt über 80 Farben. Die Farben sind wasserlöslich und ungiftig.",
 pickup_time="Nach etwa einer Woche im Studio",
 special_events="Bis zu 50 Plätze für JGA, Kindergeburtstag, Firmenfeiern und Teamevents. Einen Termin vereinbarst du online über die Buchungsseite.",
 hat_instagram=INS("glasuri_malstudio"),
 description="Keramik-Malstudio in Dortmund-Aplerbeck mit Rohlingen wie Tassen, Tellern, Schalen und Figuren und über 80 Farben. Keramik bemalen für die ganze Familie in entspannter Umgebung, ohne Vorwissen. Einen Termin buchst du online.")
mk(13,"diamal-ceramic-cafe-bocholt","DIAMAL Ceramic Café","Bocholt","NW","",
 tags="birthday-parties", hat_instagram=INS("diamal_ceramiccafe"),
 price_note="Preise stehen auf einer eigenen Preisseite. Derzeit ist nur Barzahlung möglich.",
 special_events="Reservierung und Malslots, Geburtstage und Events, Gutscheine.",
 description="Ceramic Café in Bocholt, in dem du Keramik selbst bemalst. Für Anfänger und erfahrene Maler, für Freunde, Familien oder kreative Zeit allein.")
mk(14,"maleri-keramik-haltern-am-see","MALERI Keramik","Haltern am See","NW","info@maleri-keramik.de",
 tags="reservation-only, birthday-parties, hen-party", price_from="12", price_mug="14",
 studio_fee="Regalpreis ist Endpreis (Material, Farben, Glasur und Brand) · Malzeit 3 Stunden",
 price_note="Becher ab 14 €, kleine Schälchen ab 12 €, Stücke von 12 bis 60 €. Es gibt über 150 Formen. Essen und Trinken ist an den Maltischen nicht erlaubt.",
 pickup_time="Ca. 10–14 Tage nach dem Bemalen",
 special_events="Kinder sind willkommen, aber nur mit Begleitung eines Erwachsenen, das Angebot richtet sich vor allem an Erwachsene. Kindergeburtstag, Junggesellenabschied und Babyfußabdruck. Kindergärten, Kitas und Schulklassen bitte vormittags buchen. Reservierungsanfragen werden meist innerhalb von 24 Stunden beantwortet.",
 hat_instagram=INS("maleri_keramik_haltern"),
 description="Kreatives Studio im skandinavischen Stil in Haltern am See, in dem du Keramik selbst bemalst. Du wählst aus über 150 Formen, die Malzeit dauert drei Stunden, Farben sind lebensmittelecht, cadmium- und bleifrei. Das Studio glasiert und brennt die Stücke.")
# ---- Bonn
mk(18,"frau-kramer-keramikmalwerkstatt-bonn","Frau Kramer Keramikmalwerkstatt","Bonn","NW","info@frau-kramer.de",
 tags="birthday-parties, hen-party",
 price_note="Preise stehen nicht auf der Website. Das Angebot umfasst weitere Standorte (Atelier, Keramikmalsalon Südstadt), deren Stand die Website zum Teil nicht klar nennt.",
 pickup_time="Abholung zu den Öffnungszeiten, nicht vor 15 Uhr · Abholschein mitbringen",
 special_events="Kindergeburtstage, Junggesellenabschiede, Feste und Events (eigene Seiten), Gutscheine und Auftragsarbeiten. Du reservierst deinen Termin über den Button «Termin in der Werkstatt reservieren».",
 hat_instagram=INS("fraukramer"),
 description="Keramikmalwerkstatt in Bonn-Poppelsdorf, ein kreativer Ort für Freunde, Familie und Me-Time. Du bemalst Keramik, das Atelier glasiert und brennt sie. Mehrere Malzeiten pro Tag, Termin online reservierbar.")
mk(21,"keramik-auf-meine-art-bonn","Keramik auf meine Art","Bonn","NW","am@keramikaufmeineart.de",
 tags="birthday-parties, hen-party",
 price_note="Die Preise sind Komplettpreise und enthalten Rohling, Farben und Material, Zeit im Studio, Glasieren und Brennen. Die Zahlung erfolgt nur bargeldlos direkt nach dem Malen. Einzelpreise stehen auf einer eigenen Preisseite.",
 special_events="Alleine oder mit Freunden, für Geburtstage, Junggesellenabschiede, Babyfußabdrücke und Treffen mit Gleichgesinnten. Einen Termin buchst du online.",
 description="Keramikmalstudio in Bonn, in dem du deine Keramik frei nach deinen Vorstellungen gestaltest, allein oder in der Gruppe, als Geschenk oder Erinnerungsstück. Rohling, Farben, Studiozeit, Glasur und Brand sind im Preis enthalten.")
# ---- Essen
mk(39,"coco-ceramics-essen","coco ceramics","Essen","NW","info@cococeramics.de",addr="Rüttenscheider Straße 14, 45128 Essen",
 tags="reservation-only, corporate-events", price_from="12", price_mug="23-33", price_plate="19-68",
 studio_fee="Keine Studiogebühr · kein Mindestumsatz · Malslot ca. 2,5 Stunden",
 price_note="Tassen und Becher 23–33 €, Teller, Schalen und Schüsseln 19–68 €, Vasen und Dosen 22–67 €, Kannen und Krüge 30–67 €, Kleinigkeiten ab 12 €. Farben, Glasur und Brand sind im Preis enthalten, Getränke kosten extra. Nur Kartenzahlung.",
 pickup_time="Nach ca. 3 Wochen",
 special_events="Teamevents und exklusive Events. Das Studio hat 52 Plätze auf über 160 Quadratmetern. Walk-ins sind nicht möglich, die Plätze werden zugewiesen.",
 hat_instagram=INS("cococeramics.studio"),
 description="Keramik-Malstudio in Essen-Rüttenscheid, das Keramik bemalen mit Specialty Coffee und Matcha verbindet. Du suchst dir ein Stück und Farben aus, das Studio glasiert und brennt es. Reservierung ist erforderlich.")
mk(40,"mala-by-laura-essen","MALA by Laura","Essen","NW","info@mala-by-laura.de",
 tags="kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise werden laut Website im Studio genannt. Es gibt über 450 Rohlinge. Der Malkoffer (zum Bemalen zuhause) kann ab vier Keramikstücken gemietet werden und eignet sich für bis zu 15 Personen.",
 special_events="Eventraum für Junggesellinnenabschied, Geburtstag oder Kindergeburtstag. Mobiles Malen bei Firmen oder privaten Events. Termine buchst du über die Reservierungsseite.",
 hat_instagram=INS("mala_by_laura"),
 description="Keramikmalstudio in Essen-Kettwig mit über 450 Rohlingen und vielen Farben. Du gestaltest Keramik nach deinen Ideen. Daneben gibt es einen Malkoffer für zuhause, einen Eventraum und mobiles Malen für Firmen und private Anlässe.")
mk(41,"pottery-essen","Pottery Essen","Essen","NW","",
 tags="walk-in, reservation-empfohlen, corporate-events", price_from="10", price_mug="25", price_plate="18-40",
 studio_fee="Keine Studiogebühr · Malslot kostenlos · ca. 2,5 Stunden",
 price_note="Rohlinge 15–65 € (die FAQ nennt 10–60 €), eine Tasse kostet etwa 25 €, Teller 18–40 €. Es gibt über 30 Farben. Das Studio liegt im Obergeschoss, es führen ca. 20 Stufen hinauf, das Gebäude ist nicht barrierefrei.",
 pickup_time="Ca. 7 Tage nach dem Bemalen",
 special_events="Feste Malslots buchst du online, Walk-ins sind willkommen, wenn ein Platz frei ist. Firmenevents und ähnliche Veranstaltungen außerhalb der Öffnungszeiten, auf Wunsch mit Catering. Das Studio liegt in der Erlebniswelt Stockfinster, 20 Parkplätze.",
 hat_instagram=INS("potteryessen"),
 description="Keramik-Malstudio in Essen mit über 30 Farben und Hilfe durch das Team. Das Studio glasiert und brennt deine Stücke. Der Malslot ist kostenlos, du zahlst nur den Rohling. Feste Slots buchst du online, spontan vorbeikommen geht, wenn ein Platz frei ist.")
mk(42,"farbrausch-keramik-essen","Farbrausch Keramik","Essen","NW","",addr="Kahrstraße 65, 45130 Essen",
 tags="reservation-empfohlen",
 studio_fee="Preise inklusive Farbe, Glasur und Brand · Zeitfenster 12–15 und 15–18 Uhr",
 price_note="Die Preise stehen laut Website in den Instagram-Highlights. Die Farben sind schadstofffrei und wasserlöslich, die Keramik ist spülmaschinenfest. Das Atelier nutzt 100 % Ökostrom.",
 pickup_time="Fertig nach maximal 3 Wochen",
 special_events="Gruppen in geselliger Runde, Events und Gutscheine. Keramik und Farben können auch zum Bemalen mit nach Hause genommen werden. Eine Reservierung ist von Vorteil.",
 hat_instagram=INS("farbrausch_keramik"),
 description="Gemütliches Keramik-Malstudio in Essen mit Erfahrung seit 2013. Du suchst dir Keramik und Farben aus und bemalst sie, das Atelier glasiert und brennt sie. Die Farben sind schadstofffrei, die Stücke spülmaschinenfest.")
mk(43,"buntmacherei-essen","buntmacherei","Essen","NW","",
 tags="walk-in, reservation-empfohlen, kids-friendly",
 special_events="Einsteiger-Workshops für bis zu 14 Personen (montags und mittwochs ab 17:30 Uhr), Kinder malen ab 6 Jahren in der Kleingruppe, Comic-Painting, DIY-Duftkerzen-Abend und XXL-Advents-Abend. Es gibt außerdem Feiern und Events.",
 hat_instagram=INS("buntmacherei_keramik"),
 description="Offenes Keramik-Malatelier in Essen. Du kannst vorab einen Platz reservieren, Einsteiger-Workshops in kleinen Gruppen, dazu Themenabende und Kindermalen ab sechs Jahren.")
mk(44,"liebe-im-ton-essen","Liebe im Ton","Essen","NW","info@liebeimton.de",
 hours="Jeden 2. Mi 16–18:30 Uhr, Do 18–20:30 Uhr, jeden 2. Fr 18:30–21 Uhr, Sa 18:30–21 Uhr, So 15–17:30 Uhr (aktuelle Termine im Buchungskalender)",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events", price_from="8",
 studio_fee="Mindestmalwert 15 € pro Person · Rohling, Farben, Material, Werkzeug, Glasur und Brand inklusive",
 price_note="Rohlinge kosten je nach Form und Größe 8–65 €. Als Richtwert nennt das Studio ca. 25–35 € pro Person.",
 special_events="Kinder und Erwachsene, Familien, Paare, Teamausflug, Junggesellinnenabschied und Kindergeburtstag. Kreativzeit to go, Events und Specials. Eine vorherige Reservierung ist erforderlich.",
 hat_instagram=INS("liebe.im.ton"),
 description="Keramikmalstudio in Essen-Borbeck, in dem du Tassen, Teller, Schalen oder Deko nach deinen Vorstellungen bemalst. Vorkenntnisse sind nicht nötig. Für Einzelpersonen, Gruppen, Paare und Familien, Reservierung erforderlich.")
# ---- Karlsruhe
mk(25,"happy-pottery-karlsruhe","Happy Pottery","Karlsruhe","BW","",
 tags="hen-party, corporate-events", price_from="12", price_mug="13-28", price_plate="12-39",
 studio_fee="Mindestumsatz 20 € pro Einkauf · alle Leistungen (Maltechniken, Werkzeuge, Farben, Glasieren, Brennen) im Keramikpreis",
 price_note="Tassen und Becher 13–28 €, Teller und Platten 12–39 €. Die tatsächlichen Preise können abweichen. Die Abendtermine sind ab 12 Jahren.",
 special_events="Veranstaltungen und Gruppen, Familienfeiern, Junggesellinnenabschied und Teamevents. Daneben eine offene Töpferwerkstatt (Drehscheibe oder Handaufbau), ein Malkoffer zum Mitnehmen und eine zweitägige Fortbildung für alle, die ein eigenes Studio eröffnen möchten.",
 hat_instagram=INS("happypottery.de"),
 description="Töpfer- und Keramikmalstudio in Karlsruhe mit einem Malstudio für fertige Keramik und einer offenen Töpferwerkstatt. Im Malstudio gestaltest du Keramik ganz nach deinen Vorstellungen. Das Studio legt Wert auf Nachhaltigkeit, Inklusion und Barrierefreiheit.")
mk(55,"hippiekids-karlsruhe","hippiekids pottery painting","Karlsruhe","BW","info@hippiekids.de",
 tags="birthday-parties, corporate-events",
 price_note="Preise stehen nicht auf der Website. Es gibt eine eigene Seite für abholbereite Keramik.",
 special_events="Geburtstage und Feiern, geschlossene Gruppen mit Freunden, Familie, Kollegen oder Kunden mit zusätzlichen Terminen, Malboxen und Gutscheine. Weihnachtspause vom 18.12.2026 bis 10.01.2027.",
 hat_instagram=INS("hippiekids.potterypainting"),
 description="Familiengeführtes Keramik-Malstudio in Karlsruhe-Wolfartsweier, in dem du in entspannter, geselliger Atmosphäre Keramik bemalst. Fürs Bemalen braucht man keine besonderen Voraussetzungen. Termine buchst du online.")
mk(56,"blossom-kreativmanufaktur-karlsruhe","Blossom Kreativmanufaktur","Karlsruhe","BW","hallo@blsmkm.de",
 tags="reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events", price_from="10",
 studio_fee="Malen ist kostenlos, bezahlt wird nur der Rohling (ab 10 €) · Mindestumsatz 25 € pro Person",
 price_note="Im Rohlingspreis sind Farben, Glasur, Brand und dein Platz enthalten. Bezahlt wird am Tag des Besuchs. Die Glasuren sind wasserlöslich und als ungiftig zertifiziert.",
 pickup_time="Meist innerhalb von 7 Tagen nach dem Brennen · Abholung nur zu den Öffnungszeiten",
 special_events="Kindergeburtstage, Junggesellinnenabschiede, Geburtstage, private Buchungen und Firmenfeiern sowie Angebote für Unternehmen. Workshops wie Marmorieren, Flaschengärten und Resin und Keramik zuhause bemalen.",
 description="Kreativstudio in Karlsruhe-Neureut für Keramik bemalen, Workshops und Events. Du bemalst Rohkeramik ab 10 €, das Malen selbst kostet nichts, es gilt ein Mindestumsatz von 25 € pro Person. Eine Reservierung wird empfohlen.")
# ---- Munster (Lüneburger Heide)
mk(32,"paint-your-style-munster","Paint your Style Lüneburger Heide","Munster","NI","",addr="Am Hanloh 5, 29633 Munster",
 tags="reservation-empfohlen, kids-friendly, birthday-parties", hat_instagram=INS("paintyourstyle_munster"),
 price_note=PYS_NOTE+" Reservierungen für Abende per WhatsApp.",
 pickup_time="Ca. 1–3 Tage (allgemeine Angabe der Paint-your-Style-Website)",
 special_events="Kindergeburtstage mit Zeitfenster um 15:30 Uhr, dienstags bis donnerstags. Mädelsabende und Abendtermine nach Reservierung per WhatsApp. Zeitfenster 12, 15 und 18 Uhr.",
 description="Malstudio für Ideen auf Keramik in Munster in der Lüneburger Heide. Du suchst dir Keramik aus, bemalst sie selbst, und das Team glasiert und brennt sie. Geöffnet dienstags bis samstags, im November und Dezember auch sonntags.")
json.dump(raw,open(p,'w'),indent=2,ensure_ascii=False); open(p,'a').write("\n")
import collections
print(len(d), sum(1 for s in d if s.get('country')=='DE'))
