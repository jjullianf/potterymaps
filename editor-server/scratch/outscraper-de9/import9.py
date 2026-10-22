import json,sys,io,contextlib,re
sys.path.insert(0,'editor-server/scratch/outscraper-de3')
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_report3 as b
hours_de=b.hours_de
RAW=json.load(open('editor-server/scratch/outscraper-de9/_raw_dump.json',encoding='utf-8'))['N']
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
NW,TH,HE,BB,BW,ST,NI="NW","TH","HE","BB","BW","ST","NI"
KID="kids-friendly, birthday-parties"
mk(4,"keramikwelt-weimar","RUHEKOSMOS Keramikwelt Weimar","Weimar",TH,"info@keramikwelt-weimar.de",addr="Röhrstraße 25a, 99423 Weimar",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Es gibt über 100 verschiedene Rohlinge. Termine reservierst du online.",
 special_events="Kindergeburtstage ab 7 Jahren, Junggesellinnenabschiede und Firmenevents.",
 description="Keramikmalstudio in Weimar mit über 100 verschiedenen Rohlingen, die du selbst bemalst. Termine reservierst du online, auch für Kindergeburtstage, JGA und Firmenevents.")
mk(11,"tonwerkstatt-oberweimar","Tonwerkstatt Oberweimar","Weimar (Lahn)",HE,"info@tonwerkstatt-oberweimar.de",hours="",
 price_note="Preise stehen nicht auf der Website. Die Malnachmittage finden zu festen Terminen statt, die auf der Website und bei Instagram stehen.",
 special_events="Kreative Malnachmittage, Malbox zum Ausleihen (Anfrage per E-Mail) und Kindergeburtstage.",
 hat_instagram=INS("tonwerkstatt_oberweimar"),
 description="Tonwerkstatt in Weimar (Lahn) bei Marburg mit kreativen Malnachmittagen, bei denen du Keramikrohlinge bemalst. Dazu gibt es eine Malbox zum Ausleihen und Kindergeburtstage.")
mk(12,"potteria-neuss","Potteria","Neuss",NW,"info@keramikbemalen-neuss.de",
 hours="Do 18–21 Uhr, Sa 11–14 Uhr, dazu unregelmäßige Termine an anderen Tagen",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Zum aktiven Malen meldest du dich online an, weil die Plätze begrenzt sind. Rohkeramik und Farben gibt es auch zum Kauf vor Ort.",
 special_events="Kindergeburtstage, Geburtstage für Erwachsene, Mädelsabende, Junggesellinnenabschiede, Babypartys, Teamevents und Weihnachtsfeiern. Die Event-Potteria bietet Platz für bis zu 12 Personen.",
 hat_instagram=INS("potterianeuss"),
 description="Keramikbemalen in Neuss zu festen Mal-Terminen, die du online buchst. Neben dem freien Malen gibt es Kindergeburtstage, Mädelsabende und Teamevents für bis zu 12 Personen.")
mk(13,"einmalig-keramikmalstudio-willich","einMalig Keramikmalstudio","Willich",NW,"einmalig-events@outlook.de",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="15",
 studio_fee="Keine Zusatzgebühr · 2,5 Stunden · Rohkeramik, Farben, Glasur und Brand inklusive",
 price_note="Keramik gibt es ab 15 €. Plätze buchst du über das Buchungstool.",
 pickup_time="Nach ca. einer Woche",
 special_events="Kindergeburtstage ab Grundschulalter für 8–12 Kinder (Pakete zu 20, 25 oder 30 € pro Kind), Junggesellenabschiede und Firmenfeiern. Ab 25 Personen sind auch Termine außerhalb der Öffnungszeiten möglich.",
 hat_instagram=INS("einmalig_das_keramikmalstudio"),
 description="Keramikmalstudio in Willich bei Krefeld. Du bemalst Rohkeramik in 2,5 Stunden, Farben, Glasur und Brand sind im Preis enthalten. Plätze buchst du online.")
mk(14,"maltastisch-koeln","Maltastisch","Köln",NW,addr="Berrenrather Straße 220, 50939 Köln",
 hours="Mo geschlossen, Di 15–20:30 Uhr, Mi, Do 16–18:30 Uhr, Fr, So 12–17:30 Uhr, Sa 12–20:30 Uhr",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties",price_from="20",
 studio_fee="Mindestumsatz 20 € pro Person · meist 2–2,5 Stunden",
 price_note="Die meisten Stücke kosten 20–40 €, besondere bis 65 €. Getränke und Kuchen sind nicht enthalten. Reservierung wird empfohlen, spontan vorbeikommen geht.",
 pickup_time="Nach ca. 7–14 Tagen, Di–Fr · fertige Stücke werden maximal 10 Wochen aufbewahrt",
 special_events="Kindergeburtstage mittwochs und donnerstags, Gruppen ab 8 Personen über das Kontaktformular, exklusive Studiomiete für geschlossene Gesellschaften ab 20 Personen.",
 hat_instagram=INS("mal_tastisch"),
 description="Keramik-Malstudio in Köln-Sülz mit Café-Atmosphäre. Du bemalst einen Rohling in 2 bis 2,5 Stunden, Glasur und Brand übernimmt das Studio. Reservierung wird empfohlen, Spontanbesuche sind möglich.")
mk(17,"angemalt-keramik-malstuebchen-magdeburg","AnGemalt Keramik-Malstübchen","Magdeburg",ST,
 price_note="Preise stehen nicht auf der Website. Farben, Glasur und Brand sind im Preis enthalten. Es gibt über 150 Rohlinge.",
 pickup_time="Nach ca. 10–14 Tagen",
 description="Keramik-Malstübchen in Magdeburg mit über 150 Rohlingen, die du selbst bemalst. Glasur und Brand sind im Preis enthalten, deine Stücke sind nach 10 bis 14 Tagen abholbereit.")
mk(25,"cafe-apfel-mit-stiel-magdeburg","Café Apfel mit Sti(e)l","Magdeburg",ST,hours="Fr–So 14–18 Uhr (April bis Oktober)",
 price_note="Preise stehen nicht auf der Website. Für Herbst und Winter gilt ein Reservierungshinweis.",
 special_events="Töpfern, Keramik bemalen und Teamevents am Pechauer See.",
 hat_instagram=INS("apfelmitstil"),
 description="Café am Pechauer See bei Magdeburg, in dem du Keramik bemalen und töpfern kannst. Im Sommerhalbjahr ist freitags bis sonntags von 14 bis 18 Uhr geöffnet.")
mk(26,"poppys-jena","Poppys","Jena",TH,
 price_note="Preise stehen nicht auf der Website. Für Kinder gibt es Termine wie «Halloween Keramik bemalen» mit Buchungslink.",
 special_events="Kindertermine zu Jahreszeiten-Themen, zum Beispiel Herbstteller gestalten und Halloween Keramik bemalen, sowie Gruppen-Reservierungen.",
 hat_instagram=INS("poppys.jena"),
 description="Keramik bemalen in Jena für Kinder und Erwachsene. Es gibt Kindertermine zu Jahreszeiten-Themen, Gruppen reservieren separat.")
mk(29,"kabuff-keramik-malstudio-jena","Kabuff Keramik Malstudio","Jena",TH,"kontakt@kabuff-jena.de",
 hours="Mo, Di, So geschlossen, Mi, Do 13–18 Uhr, Fr, Sa 10–19:30 Uhr",
 tags="reservation-only",price_from="5",
 studio_fee="Anzahlung 10 € bei der Buchung, wird auf die Keramik angerechnet · 2-Stunden-Slot",
 price_note="Rohlinge kosten 5–70 €. Gebucht wird online.",
 pickup_time="Innerhalb von 1–2 Wochen · Versand per DHL gegen Aufpreis möglich",
 hat_instagram=INS("kabuffjena"),
 description="Keramik-Malstudio im Kabuff in der Jenaer Innenstadt. Du buchst online einen 2-Stunden-Slot, wählst einen Rohling zwischen 5 und 70 € und bemalst ihn selbst.")
KE=dict(hours="Mo, So und Feiertage geschlossen, Di, Do, Sa 11–14 und 15–18 Uhr, Mi, Fr 15–18 Uhr",
 tags="kids-friendly, birthday-parties, corporate-events",
 price_note="Preise stehen nicht auf der Website. Du reservierst deinen Platz über eine Anfrage auf der Website.",
 special_events="Kindergeburtstage, Firmenfeiern, Ladies-Abende, thematische Workshops sowie Geburtstags- und Privatevents.",
 hat_instagram=INS("keramika_malstudio"))
mk(36,"keramika-malstudio-lange-bruecke-erfurt","Keramika Das Malstudio Lange Brücke","Erfurt",TH,"info@keramika-malstudio.de",**KE,
 description="Keramikmalstudio an der Langen Brücke in Erfurt. Du suchst dir einen Rohling aus, bemalst ihn selbst, danach wird er glasiert und gebrannt. Es gibt einen zweiten Standort in der Warsbergstraße.")
mk(35,"keramika-malstudio-warsbergstrasse-erfurt","Keramika Das Malstudio Warsbergstraße","Erfurt",TH,"info@keramika-malstudio.de",**KE,
 description="Keramikmalstudio in der Warsbergstraße nahe dem Gothaer Platz in Erfurt. Du bemalst einen Rohling selbst, danach wird er glasiert und gebrannt. Es gibt einen zweiten Standort an der Langen Brücke.")
mk(37,"beawi-kreativcafe-erfurt","BeAwi KreativCafé","Erfurt",TH,"info@kreativcafe-erfurt.de",
 hours="Mo–Do 14–18 Uhr, Fr, Sa 11–14 und 15–18 Uhr, So 14–18 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 studio_fee="Beim Kindergeburtstag Mindestumsatz 15 € pro Kind, eine Begleitperson ist kostenfrei",
 price_note="Offenes Malen: Du reservierst einen Platz, wählst einen Rohling und bemalst ihn in deinem Tempo. Die Zeiten gelten für den Kreativteil, das Café hat eigene Zeiten. Der Malkoffer toGo kostet 39 € Servicegebühr zuzüglich Rohkeramik.",
 special_events="Kindergeburtstag ab 8 Jahren mit Waffeln und Limonade, JGA mit Kaffee-und-Kuchen-Paket, Teamevents und Schulklassen (Mo–Do 10–12 Uhr, max. 25 Kinder). Für 15–20 Personen gibt es das EventCafé in der Bergstraße.",
 hat_instagram=INS("beawi.kreativcafe"),
 description="Kreativcafé in Erfurt mit offenem Malen: Du reservierst einen Platz, wählst einen Rohling und bemalst ihn in deinem Tempo. Für Kindergeburtstage, JGA und Teamevents gibt es eigene Angebote.")
mk(43,"andreas-auszeit-keramik-atelier-erfurt","Andrea's Auszeit Keramik Atelier","Erfurt",TH,hours="",
 tags="reservation-only, kids-friendly, birthday-parties",
 price_note="Preise stehen nicht auf der Website. Termine nach Absprache.",
 special_events="Kindergeburtstage laut Website.",
 description="Keramik-Atelier in Erfurt-Gispersleben, in dem du nach Terminabsprache Keramik bemalst.")
mk(39,"be-mal-keramikstudio-paderborn","Be-mal Keramikstudio","Paderborn",NW,"info@be-mal.de",
 hours="Mo, Di, So geschlossen, Mi 16–19 Uhr, Do, Fr 15:30–19 Uhr, Sa 10:30–19 Uhr",
 tags="reservation-only, kids-friendly, hen-party, corporate-events",
 studio_fee="Samstags buchbar 10:30–13, 13:30–16 und 16:30–19 Uhr",
 price_note="Einzelpreise stehen nicht auf der Website. Gruppen ab 12 Personen zahlen außerhalb der Öffnungszeiten nach Vereinbarung 33 € pro Person, Keramik bis 28 € ist inbegriffen. Gebucht wird ausschließlich online.",
 pickup_time="Nach einigen Tagen",
 special_events="Geburtstage, Junggesellinnenabschiede, Klassen- und Betriebsausflüge sowie Firmenfeiern.",
 description="Keramikstudio in Paderborn-Schloß Neuhaus, in dem du vorgefertigte Keramik bemalst. Du buchst ausschließlich online, nach einigen Tagen ist dein Stück gebrannt.")
mk(40,"marys-keramik-cafe-borchen","Mary's Keramik Café","Borchen",NW,
 hours="Mo, So und Feiertage geschlossen, Di, Mi 14:30–19 Uhr, Do 14:30–21:30 Uhr, Fr 11–19 Uhr, Sa 10–16 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="10",
 studio_fee="Begleitpersonen ohne Malen zahlen 25 € Sitzplatzpauschale · feste Malzeiten von etwa 2,5–3 Stunden",
 price_note="Keramik kostet 10–80 € (Regalpreise, inklusive Farbe und Brand, zuzüglich Verzehr). Du reservierst Mal-Plätze, Malabende sind nur mit Reservierung möglich.",
 pickup_time="Nach 8 Tagen während der Öffnungszeiten, bis 18 Uhr",
 special_events="Kindergeburtstage als Rundum-sorglos-Paket, JGA-Pakete, Keramik Café to Go für Firmenevents und Gruppenevents dienstags und mittwochs vormittags.",
 description="Keramik Café in Borchen bei Paderborn. Hier kann jeder spielerisch Keramik bemalen, du reservierst feste Mal-Plätze. Kindergeburtstage, JGA und Firmenevents gibt es als Pakete.")
mk(42,"bali-keramik-bad-lippspringe","BaLi Keramik","Bad Lippspringe",NW,"info@bali-keramik.de",hours="Nur nach Vereinbarung, vorher telefonisch oder per WhatsApp melden",
 price_note="Preise für das Bemalen stehen nicht auf der Website. Es gibt viele Keramiken auf Lager, die du abholen und nach deinen Wünschen bemalen kannst. Das Studio bietet auch einen Brennservice.",
 description="Keramik-Brennservice in Bad Lippspringe, bei dem du Keramiken abholen und nach deinen Wünschen bemalen kannst. Du meldest dich vorher telefonisch oder per WhatsApp.")
mk(52,"studionoseven-recklinghausen","StudioNo7","Recklinghausen",NW,"info@studionoseven.de",addr="Herner Straße 5, 45657 Recklinghausen",
 hours="Mi–Fr 14–19 Uhr, Sa, So 10:30–19 Uhr, Mo, Di auf Anfrage",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Plätze reservierst du über die Terminslots.",
 description="Keramik-Malstudio in Recklinghausen, in dem du Keramik bemalst. Plätze reservierst du online über die Terminslots.")
mk(71,"al-farbrica-tuebingen","al farbrica","Tübingen",BW,"info@al-farbrica.de",addr="Haaggasse 13, 72070 Tübingen",
 hours="Mo geschlossen, Di–Fr 10–18 Uhr, Sa 10–16 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Termine finden nur nach Absprache statt, gebucht wird online. Der Standort in der Bachgasse 24 ist bis 15.11.2026 geschlossen, gebrannte Keramik wird immer in der Haaggasse abgeholt.",
 special_events="Geburtstagsfeiern einschließlich Kindergeburtstag, Junggesellinnenabschied, Teamevents und Geschenke zu Anlässen wie Hochzeit und Jubiläum.",
 hat_instagram=INS("alfarbrica"),
 description="Keramik selbst bemalen in der Tübinger Altstadt. Termine gibt es nur nach Absprache und werden online gebucht. Für Geburtstage, JGA und Teamevents gibt es eigene Angebote.")
mk(82,"keramiktraeume-by-nele-kaufungen","Keramikträume by Nele","Kaufungen",HE,
 tags="reservation-only",price_from="8",
 studio_fee="Ca. 2 Stunden · Farben, Glasur und Brand inklusive",
 price_note="Keramik kostet ca. 8–80 € je nach Form und Größe. Online-Terminbuchung für bis zu 4 Personen.",
 pickup_time="Nach etwa 1–2 Wochen",
 hat_instagram=INS("keramiktraeume"),
 description="Keramik-Malstudio in Kaufungen bei Kassel. Du buchst online einen Termin für bis zu 4 Personen und bemalst in etwa 2 Stunden einen Rohling, Farben, Glasur und Brand sind inklusive.")
mk(81,"paint-your-style-kassel","Paint your Style Kassel","Kassel",HE,
 tags="reservation-only, kids-friendly, birthday-parties",
 price_note="Preise stehen auf der Standortseite nicht. Online-Reservierung, Gruppen ab 6 Personen per Formular. Feste Zeitfenster um 12, 15 und 18 Uhr, der 18-Uhr-Slot ist Gästen ab 15 Jahren vorbehalten.",
 special_events="Kindergeburtstage dienstags bis donnerstags um 15:30 Uhr.",
 description="Malstudio für Ideen auf Keramik in Kassel. Du reservierst online ein festes Zeitfenster, suchst dir Keramik aus und bemalst sie, das Team glasiert und brennt sie.")
mk(86,"mao-mao-keramik-heilbronn","Mao Mao Keramik Heilbronn","Heilbronn",BW,"heilbronn@maomao-keramik.de",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Wunschtermine buchst du online.",
 special_events="Die Website nennt Wine & Design, Teamevents, JGA und Kindergeburtstage über einen Event-Kalender.",
 hat_instagram=INS("maomao.keramik"),
 description="Keramikatelier von Mao Mao in Heilbronn, in dem du Keramik bemalst. Termine buchst du online.")
mk(85,"mal-mit-herz-heilbronn","Mal mit Herz","Heilbronn",BW,"info@mal-mit-herz.de",
 hours="Mo, So geschlossen, Di, Do 12–14:30 und 16:30–19 Uhr, Mi, Fr 12–14:30 und 16–18:30 Uhr, Sa 11:30–14 und 15–17:30 Uhr",
 tags="reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="15",
 studio_fee="Buchungsfenster von ca. 2,5 Stunden · bei Events Mindestkauf 20 € (Geburtstag) bzw. 25 € (JGA, Firmenfeier) pro Person",
 price_note="Über 170 Rohlinge für 15–60 €. Farben, Werkzeuge und Brennen sind im Preis enthalten. Reservierung wird empfohlen.",
 pickup_time="Nach etwa 4 Wochen abholbereit, abholbar innerhalb von 6 Wochen · nicht abgeholte Werke werden gespendet",
 special_events="Kindergeburtstag ab 8 Jahren (max. 8 Personen), Junggesellenabschied (max. 8 Personen) und Firmenfeiern, jeweils online buchbar.",
 hat_instagram=INS("mal_mit_herz"),
 description="Keramikmalstudio in Heilbronn mit über 170 Rohlingen. Du buchst ein Zeitfenster von etwa 2,5 Stunden, Farben, Werkzeug und Brennen sind im Preis enthalten.")
mk(90,"keramigos-neckarsulm","Keramigos Neckarsulm","Neckarsulm",BW,"hallo@keramigos-neckarsulm.de",
 tags="reservation-only, birthday-parties, hen-party, corporate-events",
 studio_fee="Mindestumsatz 15 € pro reserviertem Platz · 2 Stunden Malzeit",
 price_note="Es gibt über 100 Rohlinge. Gruppenpreis ab 7 Personen: 36 € pro Person, alles inklusive. Etageren kosten 15 € (2-stöckig) bzw. 20 € (3-stöckig) zuzüglich der gewählten Keramik.",
 pickup_time="Wenige Tage nach der Malzeit · Etageren nach 14 Tagen",
 special_events="Geburtstage, JGA, Team- und Firmenevents, Babypartys, Weihnachtsfeiern, Schulklassen, Vereine und Familienfeiern.",
 hat_instagram=INS("keramigos_neckarsulm"),
 description="Keramikmalstudio in Neckarsulm mit über 100 Rohlingen. Du buchst online eine Malzeit von 2 Stunden. Für Gruppen, Geburtstage und Firmenevents gibt es eigene Angebote.")
mk(93,"keramikkunst-ulm","Keramikkunst Ulm","Ulm",BW,hours="",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="18",
 studio_fee="Für das Studio als Gruppe Buchungsgebühr 100 € zuzüglich Rohlinge (Fr und Sa)",
 price_note="Keramik gibt es ab 18 €, die größten Stücke kosten bis 65 €. Bei zwei bemalten Teilen gibt es 5 € Rabatt. Malslots buchst du über die Buchungsplattform.",
 pickup_time="An festen Abholterminen, meist samstags · bei mobilen Workshops werden die fertigen Stücke geliefert",
 special_events="Mobile Events: Kindergeburtstage (30 oder 35 € pro Kind), Gruppen ab 6 Personen wie JGA und Firmenfeiern (45–55 € pro Person) sowie Events in Cafés, Bars, Restaurants und Vinotheken auf Anfrage.",
 hat_instagram=INS("keramikkunst.ulm"),
 description="Keramikmalstudio in Ulm mit mobilem Angebot: Du bemalst Keramik im Studio oder lässt das Team zu dir kommen, etwa für Kindergeburtstag, JGA oder Firmenfeier.")
mk(92,"mal-mal-keramik-ulm","mal.mal Keramik","Ulm",BW,
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Termine reservierst du online.",
 pickup_time="Etwa 1–3 Tage nach dem Bemalen im Studio",
 special_events="Kindergeburtstage, JGA und Firmenfeiern.",
 hat_instagram=INS("malmalkeramik.de"),
 description="Keramikmalstudio in Ulm. Du reservierst online einen Termin und holst dein Stück etwa 1 bis 3 Tage nach dem Bemalen im Studio ab.")
mk(122,"atelier-animo-ulm","Atelier ANIMO!","Ulm",BW,
 tags="reservation-only, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Spontan frei gewordene Termine werden täglich auf Instagram gepostet. Am ersten Freitag im Monat wird bis 21 Uhr gemalt.",
 pickup_time="Ca. 1–2 Wochen",
 special_events="JGA mit Sekt-Empfang und exklusiven Tischen für Gruppen sowie Teamevents mit Catering aus dem Café.",
 description="Keramik-Malatelier mit Café in Ulm. Du reservierst online, spontan frei werdende Plätze stehen täglich auf Instagram. Am ersten Freitag im Monat wird bis 21 Uhr gemalt.")
mk(123,"1000grad-keramik-bemalen-westerstetten","1000Grad Keramik bemalen","Westerstetten",BW,"1000grad-ulm@gmx.de",
 hours="Mo, So geschlossen, Di–Fr 14:15–18 Uhr, Sa 11:15–18 Uhr",
 tags="reservation-only",
 price_note="Preise stehen auf der Unterseite «Rohkeramik». Termine buchst du online.",
 pickup_time="Ca. 14 Tage nach dem Malen · Aufbewahrung bis zu 12 Wochen, du bekommst eine E-Mail, sobald die Keramik fertig ist",
 hat_instagram=INS("1000grad_keramikbemalen"),
 description="Keramikmalstudio in Westerstetten bei Ulm. Du buchst online einen Termin und bekommst eine E-Mail, sobald deine Keramik nach etwa 14 Tagen fertig gebrannt ist.")
mk(114,"lust-und-laune-ludwigsburg","Lust & Laune","Ludwigsburg",BW,
 hours="Mo, Di, So geschlossen, Mi, Do, Fr 12–20 Uhr, Sa 11–19 Uhr",
 tags="reservation-empfohlen, kids-friendly, birthday-parties",
 studio_fee="Ab 5 Personen Mindestumsatz 25 € pro Person (Mi–Fr ab 17:30 Uhr, Sa ganztags, gültig ab 1.4.2026)",
 price_note="All-inklusive-Preise mit Rohling, Aufenthalt, Farbe, Glasur und Brand. Eine Tischreservierung wird empfohlen. Malbeginn und Abholung sind bis 18 Uhr möglich.",
 special_events="Kindergeburtstage und Gruppenangebote, samstags für Kinder von 9–14 Jahren.",
 description="Keramikmalstudio in Ludwigsburg. Du bemalst einen Rohling zum All-inklusive-Preis mit Farbe, Glasur und Brand. Eine Tischreservierung wird empfohlen.")
mk(115,"herzgemacht-kreativstudio-ludwigsburg","herzgemacht KreativStudio","Ludwigsburg",BW,"hallo@herzgemacht-kreativstudio.de",
 hours="Mo 12–20 Uhr, Di geschlossen, Mi 15–20 Uhr, Do 12–21 Uhr, Fr 12–20 Uhr, Sa 11–19 Uhr, So 11–16 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="3.50",
 studio_fee="Servicepauschale 10 € pro Person (bis 18 Jahre 5 €) · 2 Stunden Malzeit",
 price_note="Keramik kostet 3,50–49 € inklusive Farben, Glasur und Brand. Die Servicepauschale kommt dazu. Du buchst über «Erlebnis buchen».",
 special_events="Geburtstage, JGA, Babypartys und Firmenevents.",
 hat_instagram=INS("herzgemacht_kreativstudio"),
 description="Kreativstudio in Ludwigsburg, in dem du zwei Stunden lang Keramik bemalst. Farben, Glasur und Brand sind inklusive, dazu kommt eine kleine Servicepauschale. Buchung online.")
mk(117,"toepfertante-esslingen","Töpfertante","Esslingen am Neckar",BW,"info@toepfertante.com",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Gebucht wird online. Außerdem gibt es einen Standort in Göppingen.",
 pickup_time="Nach 1–2 Wochen, spätestens 4 Wochen nach dem Bemaltermin abholen",
 special_events="Kindergeburtstage, Junggesellinnenabschiede, Team- und Firmenevents sowie Babyshower.",
 hat_instagram=INS("toepfer_tante"),
 description="Keramikmalstudio in der Esslinger Altstadt. Du buchst online einen Termin, nach 1 bis 2 Wochen ist dein Stück gebrannt. Für Kindergeburtstage, JGA und Teamevents gibt es eigene Angebote.")
mk(119,"pinselstrich-pohlheim","Pinselstrich","Pohlheim",HE,"info@pinselstrich-pohlheim.de",
 hours="Mo, Di geschlossen, Mi, Do 15–19 Uhr, Fr 14–20 Uhr, Sa, So 11–20 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Das Studio ist weit im Voraus ausgebucht. Stornierte Termine erscheinen im Online-Kalender, oft etwa 2 Tage vorher.",
 pickup_time="Nach ein paar Tagen · Versand möglich",
 special_events="Kindergeburtstage, Junggesellinnenabschiede sowie Firmen- und Privatfeiern.",
 hat_instagram=INS("pinselstrich_pohlheim"),
 description="Keramikstudio in Pohlheim bei Gießen, in dem du Keramik selbst bemalst. Termine buchst du online, sie sind oft weit im Voraus ausgebucht, kurzfristige Absagen erscheinen im Kalender.")
mk(128,"keramik-cafe-brandenburg","Keramik Café","Brandenburg an der Havel",BB,
 tags="walk-in, reservation-empfohlen, birthday-parties, hen-party",
 studio_fee="Zeitfenster von 2,5 Stunden",
 price_note="Preise stehen nicht auf der Website. Reservierungen sind über die Website oder per E-Mail möglich, spontane Besuche gehen, ein freier Platz ist aber nicht garantiert.",
 pickup_time="Etwa 1 Woche nach dem Bemalen",
 special_events="Kindergeburtstage, Junggesellenabschiede und Gruppenevents. Gruppen reservieren nur per E-Mail oder Kontaktformular.",
 description="Keramik Café in Brandenburg an der Havel mit Zeitfenstern von 2,5 Stunden. Reservieren geht online oder per E-Mail, spontan vorbeikommen ist bei freien Plätzen möglich.")
json.dump(raw,open(p,'w'),ensure_ascii=False,indent=2)
print(len(d))
