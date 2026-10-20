import json,sys,io,contextlib,re
sys.path.insert(0,'editor-server/scratch/outscraper-de3')
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_report3 as b
hours_de=b.hours_de
RAW=json.load(open('editor-server/scratch/outscraper-de7/_raw_dump.json',encoding='utf-8'))['N']
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
      "opening_hours":hours or hours_de(r['working_hours']),"tags":"","images":"[]","image":"","custom_faq":"[]","contacted":False,"featured":False,
      "quelle_hinweis":"Outscraper (Google Maps); Aufnahme anhand der Website geprüft am 20.10.2026",
      "lat":float(r['latitude']),"lng":float(r['longitude']),"country":"DE","currency":"EUR","postcode":plz,"region":region})
    s.update(kw); slugs.add(slug); d.append(s)
BW,BY,NW,HE,RP,NI,BB="BW","BY","NW","HE","RP","NI","BB"
# ---------- Mannheim
mk(0,"keramikmalstudio-bunte-kuh-mannheim","Keramikmalstudio Bunte Kuh","Mannheim",BW,"muh@buntekuh-keramik.de",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events", price_from="25",
 studio_fee="Mindestumsatz 25 € pro Buchung, wird vor Ort auf die Keramik angerechnet · 2,5 Stunden Malzeit",
 price_note="Einzelpreise der Keramik stehen nicht auf der Website. Es gibt über 150 Rohlinge und 30 Sitzplätze.",
 pickup_time="Nach 1–3 Werktagen · Aufbewahrung mindestens 8 Wochen",
 special_events="Kindergeburtstag ab 8 Jahren, Junggesellinnenabschied, Teambuilding und Firmenevents (auch Weihnachtsfeier und Vereinsrunde), Geburtstage sowie Specials wie Montagsmaler und Paint & Fright. Reservierung wird am Wochenende und in den Ferien empfohlen, spontan vorbeikommen geht, solange Plätze frei sind.",
 hat_instagram=INS("keramikmalstudio_bunte_kuh"),
 description="Keramikmalstudio in Mannheim-Neckarau mit 30 Sitzplätzen und über 150 Rohlingen. Du malst 2,5 Stunden lang ganz frei und ohne Vorkenntnisse, das Studio glasiert und brennt deine Stücke. Reservierung wird empfohlen, Spontanbesuche sind möglich, solange Plätze frei sind.")
mk(151,"belle-facon-studio-mannheim","Belle Façon Studio","Mannheim",BW,
 price_note="Preise stehen nicht auf der Website. Plätze im Studio im Jungbusch sind buchbar. Das Atelier in Friedrichsfeld ist eine eigene offene Töpferwerkstatt.",
 special_events="Im Studio im Jungbusch kannst du Keramik bemalen, an der Drehscheibe töpfern oder im Handaufbau arbeiten, außerdem gibt es Events zu besonderen Anlässen.",
 description="Keramikstudio im Mannheimer Jungbusch von Anna und Peter. Hier kannst du Keramik bemalen, töpfern an der Drehscheibe und im Handaufbau. Das Atelier in Friedrichsfeld ist eine eigene offene Töpferwerkstatt.")
# ---------- Freiburg / Müllheim
KT=dict(tags="reservation-only", hat_instagram=INS("keramiktoepfle"),
 price_note="Einzelpreise der Keramik stehen nicht auf der Website. Paint & Prosecco im Café Tässle in Bad Krozingen: 39 € pro Person inklusive Rohling, Farben, Glasur, Brand, einem Glas Prosecco und Snacks. Das Studio hat etwa 80 Malplätze. Reservierungen sind ausschließlich online möglich.",
 special_events="Spätschicht (18:30–20:30 Uhr), Sonntagsmaltermine, Feiern, Keramik to go und Auftragsarbeiten sowie Paint & Prosecco.")
mk(12,"keramik-toepfle-freiburg","Keramik-Töpfle Freiburg","Freiburg im Breisgau",BW,**KT,
 description="Malstudio in Freiburg, in dem du Keramik selbst gestaltest. Keramik-Töpfle gibt es seit 2015 mit Standorten in Freiburg und Müllheim. Ein Platz wird ausschließlich online reserviert.")
mk(130,"keramik-toepfle-muellheim","Keramik-Töpfle Müllheim","Müllheim",BW,**KT,
 description="Malstudio in Müllheim im Markgräflerland, in dem du Keramik selbst gestaltest. Keramik-Töpfle gibt es seit 2015 mit Standorten in Müllheim und Freiburg. Ein Platz wird ausschließlich online reserviert.")
mk(18,"wein-und-werk-freiburg","wein & werk","Freiburg im Breisgau",BW,
 tags="reservation-only, hen-party, corporate-events", hat_instagram=INS("weinundwerk"),
 price_note="Malen & Wein ab 47,30 €, Töpfern & Wein 65 €. Einen Preis für Keramik bemalen nennt die Website nicht. Alkoholfreier Wein auf Anfrage.",
 special_events="Event-Studio mit Terminen für «Keramik bemalen & Wein», «Malen & Wein» und «Töpfern & Wein». Seiten für JGA und private Gruppen sowie für Firmenevents. Plätze werden über die Terminliste gebucht.",
 description="Event-Studio in Freiburg, in dem du bei Terminen mit Wein malst, Keramik bemalst oder töpferst. Für Freunde, JGA und Firmenevents. Die Plätze buchst du für feste Termine online.")
# ---------- Krefeld
mk(96,"ceramore-krefeld","ceramore Krefeld","Krefeld",NW,"info@ceramore.de",addr="Dionysiusplatz 8, 47798 Krefeld",
 hours="Mo geschlossen, Di–Fr 15–20:30 Uhr, Sa, So 11–19:30 Uhr",
 tags="reservation-empfohlen, birthday-parties, hen-party, corporate-events", price_from="15",
 studio_fee="Keine Kursgebühr · Malslot 2,5 Stunden · Farben, Glasur und Brand inklusive",
 price_note="Du zahlst nur das Keramikstück, je nach Rohling 15–65 €. Das Studio ist auch ein Café mit Kaffee, Tee und Softgetränken. Wertgutscheine ab 10 €.",
 pickup_time="In der Regel nach 7 Tagen",
 special_events="Geburtstage, JGA, Kindergruppen und Teamevents. Malslots um 15 und 18 Uhr (Di–Fr) sowie 11, 14 und 17 Uhr (Sa–So). Am Wochenende wird eine Vorab-Buchung empfohlen. Das Krefelder Studio eröffnet laut Website im Oktober 2026.",
 hat_instagram=INS("ceramore_"),
 description="Neuer Standort von ceramore in Krefeld (ab Oktober 2026), ein Keramikstudio mit Café. Du zahlst nur dein Keramikstück, Farben, Glasur und Brand sind inklusive. Malslots buchst du online.")
# ---------- Augsburg
mk(21,"keramia-augsburg","Keramia","Augsburg",BY,"hallo@keramia-augsburg.de",
 tags="birthday-parties, hen-party, corporate-events", hat_instagram=INS("keramia_augsburg"),
 studio_fee="2 Stunden freie Malzeit",
 price_note="Preise stehen auf der Preisseite der Website. Termine buchst du online.",
 special_events="Private Kreativräume für bis zu 12 Personen für JGA, langen Mädelsabend, Kindergeburtstag, Geburtstag, Teamevent, Jubiläum und Babyshower. Specialevents wie Wine & Painting, Easy Sunday und Baby Footprint sowie Workshops.",
 description="Kreativstudio in Augsburg zum Bemalen weißer Keramik. Du malst 2 Stunden frei, das Studio glasiert und brennt deine Stücke. Dazu gibt es private Events, Specialevents und Workshops.")
mk(46,"clay-house-augsburg-gersthofen","Clay House Augsburg","Gersthofen",BY,"studio@clayhouse-augsburg.de",
 tags="birthday-parties, hen-party, corporate-events", hat_instagram=INS("clayhouse.augsburg"),
 price_note="Preise stehen nicht auf der Website. Einen Malplatz sicherst du dir online.",
 special_events="Gruppen ab 8 Personen für Geburtstage, JGA, Team-Workshops und besondere Anlässe.",
 description="Keramikmalstudio in Gersthofen bei Augsburg, eine entspannte Auszeit voller Farben und Ideen, in der du ein Unikat mit deinen eigenen Händen erschaffst. Einen Malplatz buchst du online.")
mk(48,"keramikstudio-einzigartig-bobingen","Keramikstudio Einzigartig","Bobingen",BY,"hallo@keramikstudio-einzigartig.de",
 tags="reservation-only, birthday-parties, hen-party", hat_instagram=INS("keramikstudio_einzigartig"),
 price_note="Preise stehen nicht auf der Website. Es gibt über 200 Rohlinge. Das Studio liegt im 2. Obergeschoss eines Stadthauses und ist nicht barrierefrei, im Haushalt lebt ein Hund. Versand per DHL gegen Aufpreis.",
 special_events="Kindergeburtstag, Junggesellen- und Junggesellinnenabschied und individuelle Events. Geöffnet meist samstags oder nach Absprache, ein Tisch ist über das Buchungssystem zu buchen.",
 description="Keramikmalstudio in Bobingen von Susanne Rieger in entspannter Atmosphäre. Du suchst dir aus über 200 Rohlingen ein Stück aus und bemalst es. Wegen weniger Tische ist eine Buchung nötig.")
# ---------- Mainz / Wiesbaden
mk(22,"mal-werk-mainz","Mal-Werk","Mainz",RP,"hallo@mal-werk.com",
 tags="reservation-only", pickup_time="Meist nach ca. 12 Tagen · Abholung Mo–Sa 10–18 Uhr in der Weihergartenstraße 10",
 price_note="Preise stehen auf der Preisseite der Website. Die Glasuren sind abwaschbar, lebensmittelecht und ungiftig.",
 special_events="Feiern im Mal-Werk, Mal-Pakete und «Das machen wir auch». Bitte unbedingt vorher online reservieren.",
 description="Studio in der Mainzer Altstadt, in dem du Keramikrohlinge mit eigenen Ideen selbst bemalst. Die Stücke werden vor Ort gebrannt und sind danach lebensmittelecht. Alle Altersgruppen sind willkommen, bitte vorher online reservieren.")
mk(38,"mal-wieder-wiesbaden","mal wieder","Wiesbaden",HE,"hallo@mal-wieder-keramik.de",addr="Landgrabenstraße 2, 65199 Wiesbaden",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events", price_from="10",
 studio_fee="Glasur und Brand sind im Preis inklusive · 2–3 Stunden Malzeit",
 price_note="Mittelgroße Tassen, Schüsseln und Teller kosten 16–28 €, größere Schalen, Vasen und Kannen 30–50 €, kleine Sticker 1–2 €. Kinder brauchen immer eine Begleitperson, Begleitpersonen buchen ebenfalls einen Platz.",
 pickup_time="Ca. 1–2 Wochen · maximal 3 Monate Aufbewahrung",
 special_events="Kindergeburtstag ab 7 Jahren: Malpaket 18 € pro Kind (eine Keramik und ein Getränk, 2 Stunden, empfohlenes Alter 7–11 Jahre). Gruppen ab 20 Personen auch außerhalb der Öffnungszeiten, private Feiern, Betriebsausflüge, JGA und Geburtstage. Online-Buchung bis 10 Personen, darüber per E-Mail oder Telefon.",
 hat_instagram=INS("mal_wieder_keramik"),
 description="Keramikmalstudio mit Mal-Café und DIY-Werkstatt in Wiesbaden, mit Getränken (auch Bio und Fairtrade) und Rohkeramiken zum Bemalen. Reservierung wird empfohlen, spontan vorbeikommen geht, ein Platz ist aber nicht garantiert. Montag und Dienstag sind Ruhetage.")
mk(44,"schoen-bunt-wiesbaden","Schön Bunt Malkeramikstudio","Wiesbaden",HE,"malen@schoenbunt-keramik.de",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events", hat_instagram=INS("schoenbunt_keramik"),
 studio_fee="Brennen und Glasieren sind im Preis inbegriffen",
 price_note="Preise stehen nicht auf der Website. Die Farben sind ungiftig, lebensmittelecht und spülmaschinenfest. Montag bis Mittwoch nach Vereinbarung.",
 pickup_time="Nach ca. einer Woche",
 special_events="Kindergeburtstage, Mädelsabende und Junggesellinnenabschiede, Teamevents und Familienausflüge. Reservierung online oder telefonisch, bei mehreren Personen empfohlen, spontan ist meist ein Platz frei.",
 description="Malstudio in Wiesbaden mit großer Auswahl an Keramikrohlingen, ungiftigen und lebensmittelechten Farben. Hell und gemütlich eingerichtet für Anfänger, Profis, Kinder, Erwachsene und Gruppen. Brennen und Glasieren sind im Preis inbegriffen.")
# ---------- Heidelberg
mk(30,"der-keramikofen-heidelberg","Der Keramikofen","Heidelberg",BW,
 tags="kids-friendly, birthday-parties, hen-party, corporate-events", hat_instagram=INS("derkeramikofen"),
 price_note="Preise stehen nicht auf der Website. Abholung an der Abholstation Untere Straße 12 (Mi 15–19 Uhr, Sa und So 14–18 Uhr, die Fußzeile nennt Mi–So 15–18 Uhr).",
 special_events="Kindergeburtstag, JGA und Teambuilding (private Feiern und Firmenausflüge), Kurse, Erlebnisse und Geschenkkarten. Einen Platz reservierst du in der Malwerkstatt.",
 description="Kleines, gemütliches Keramik-Malstudio in der Heidelberger Altstadt mit offenem Malen, Events und Geschenkkarten. Du suchst dir aus den Regalen einen Rohling aus und bemalst ihn ganz nach deinen Vorstellungen.")
mk(84,"ceramic-atelier-heidelberg","Ceramic-Atelier","Heidelberg",BW,"info@ceramic-atelier.de",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events", hat_instagram=INS("ceramicatelier"),
 studio_fee="Zeitslot 2 Stunden, die Anzahl der Plätze muss reserviert werden",
 price_note="Preise stehen nicht auf der Website. Malbox zum Bemalen zuhause: online bestellen, im Atelier abholen.",
 special_events="Kindergeburtstage, Gruppen von 6 bis maximal 11 Personen, Junggesellinnenabschied und Team-Building-Events. Offene Töpferwerkstatt und Töpferkurse. Abholung Di und Fr 15:30–18 Uhr, Sa 12–14 Uhr.",
 description="Keramik-Atelier in Heidelberg-Handschuhsheim für Keramikbemalen für alle Altersgruppen, dazu offene Töpferwerkstatt, Kurse und Feiern. Das Malen im Atelier erfordert eine Reservierung.")
mk(90,"kleine-keramik-neckargemuend","Kleine Keramik","Neckargemünd",BW,
 tags="walk-in, reservation-empfohlen, birthday-parties, hen-party, corporate-events", hat_instagram=INS("kleinekeramik"),
 price_note="Preise stehen auf der Seite «So geht's». Das Studio zieht laut Website im Januar um, die Wiedereröffnung ist voraussichtlich im Februar.",
 special_events="Junggesellinnenabschied, Kindergeburtstag und Teamevent sowie besondere Kurse und Workshops. Am einfachsten buchst du deinen Platz online, spontane Besuche sind möglich, sofern noch ein Platz frei ist.",
 description="Keramik-Malstudio in gemütlicher Atmosphäre in der Altstadt von Neckargemünd. Du wählst einen Rohling und gestaltest dein Lieblingsstück ganz nach deinen Ideen. Plätze buchst du online, spontan geht es, wenn noch Platz ist.")
# ---------- Duisburg / Dinslaken / Wuppertal
mk(39,"kunst-und-zauber-duisburg","Kunst und Zauber","Duisburg",NW,"info@kunstundzauber.de",
 tags="kids-friendly, birthday-parties, hen-party, corporate-events", hat_instagram=INS("kunstundzauber_keramik"),
 price_note="Preise stehen auf der Seite «Keramikpreise». Bei den MalZeiten bitte etwa 30 Minuten nach Beginn zur Abholung kommen, während Workshops ist keine Abholung möglich.",
 special_events="Kindergeburtstag, JGA, Teambuildingevents und exklusive Abende, Workshops und Specials («Keramik meets …»), Kreativtüte und Malkoffer zum Mitnehmen. Buchung über den Buchungskalender.",
 description="Keramikmalwerkstatt in Duisburg mit MalZeiten, Workshops, Specials und Kreativtüten. Bei uns dreht sich alles um Keramik. Du bemalst Keramikstücke nach deinen eigenen Vorstellungen.")
MA=dict(tags="kids-friendly", hat_instagram=INS("marou_studio"),
 studio_fee="3 Stunden Malzeit",
 price_note="Preise stehen auf der Preisseite der Website. Kinder ab 7 Jahren können an den Töpferkursen teilnehmen, für jüngere Kinder gibt es eine Spielecke.",
 pickup_time="Ca. 3 Wochen · Versand nach Hause möglich",
 special_events="Töpferkurse und Malzeiten in Duisburg und Dinslaken, Familien und Gruppen willkommen. Malzeiten buchst du online.")
mk(40,"marou-studio-duisburg","Marou Studio Duisburg","Duisburg",NW,"duisburg@maroustudio.de",**MA,
 description="Töpfer- und Keramikstudio mitten im Pott. Im Marou Studio in Duisburg wählst du ein Keramikstück aus und bemalst es nach Lust und Laune. Dazu gibt es Töpferkurse.")
mk(149,"marou-studio-dinslaken","Marou Studio Dinslaken","Dinslaken",NW,"",**MA,
 description="Töpfer- und Keramikstudio im Zentrum von Dinslaken (seit 17.10.). Im Marou Studio wählst du ein Keramikstück aus und bemalst es nach Lust und Laune. Dazu gibt es Töpferkurse.")
mk(42,"antje-heidermann-keramik-malerei-wuppertal","Antje Heidermann Keramik Malerei","Wuppertal",NW,"info@antjeheidermann.de",
 tags="birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Abholung und Abgabe bemalter Keramik to go: Di, Do, Fr und Sa 12–18 Uhr. Die Website nennt zwei Adressen (Staasstraße 45 und Marktstraße 45), bitte vor dem Besuch prüfen.",
 special_events="Feiern, Kindergeburtstage, Junggesellinnen- und Junggesellenabschiede und Teamevents sowie Keramik to go.",
 description="Malerei- und Keramik-Atelier von Antje Heidermann in Wuppertal mit dem Angebot Keramik Malerei. Du bemalst Keramik im Atelier, die Stücke werden gebrannt. Platzreservierung über die Website.")
# ---------- Mönchengladbach / Korschenbroich
mk(53,"selbstbemalt-moenchengladbach","Selbstbemalt","Mönchengladbach",NW,
 tags="birthday-parties", hat_instagram="",
 studio_fee="Das Komplettpaket umfasst Farben, Glasur, Brand und Werkzeug",
 price_note="Preise stehen auf der Seite «Unsere Preise». Lampen-Workshop: 20 € Teilnahmegebühr inklusive Lampenanschluss, das Keramikstück kommt dazu.",
 pickup_time="Nach wenigen Tagen",
 special_events="Kindergeburtstag (auch zu Hause), Feiern und Events, Maltasche to go, Belly Bowl, Lampen-Workshop. Plätze reservierst du über die Website.",
 description="Keramik-Malstudio in Mönchengladbach-Wickrath für Anfänger und Erfahrene. Du bemalst Keramik in entspannter Atmosphäre, das Studio glasiert und brennt sie. Es gibt Kindergeburtstage, Events und Gutscheine.")
mk(54,"keramik-malstudio-korschenbroich","Keramik Malstudio Korschenbroich","Korschenbroich",NW,
 tags="reservation-only, corporate-events", price_mug="20-25", hat_instagram=INS("kreativkeramikmalen"),
 studio_fee="Keine separate Malgebühr · Preise inklusive Farben und Nachbearbeitung · ca. 2,5 Stunden",
 price_note="Viele Tassen, Teller und Schalen kosten etwa 20–25 €, der Preis richtet sich nach dem Rohling. Es gibt über 200 Formen und ca. 20 Maltechniken. Die Malkiste (Mietkit, 50 € Pfand für 7 Tage) ist derzeit nicht verfügbar.",
 pickup_time="Nach ca. 2 Wochen · Versand per Post möglich",
 special_events="Teamtreffen und Gruppen, Workshops, Feiern & Events. Tische werden über die Website gebucht.",
 description="Studio in Korschenbroich, in dem du Keramik selber bemalen kannst. Du wählst aus über 200 Rohlingen und etwa 20 Techniken wie Stempeln, Tupfen, Kratzen und Abkleben. Keine künstlerische Begabung nötig, Reservierung erforderlich.")
# ---------- Bielefeld
PS=dict(tags="reservation-only, hen-party, corporate-events", hat_instagram=INS("porzellansalon"),
 price_note="Preise stehen auf der Preisseite der Website. Es wird mit Bargeld, Girocard oder Kreditkarte gezahlt, internationale Kreditkarten werden nicht akzeptiert. Mitgebrachtes Essen ist nicht erlaubt, alkoholfreie Getränke gibt es vor Ort. Kein Versand.",
 special_events="Gruppenanfragen ab 6 Personen über ein Formular. Junggesellinnenabschiede und Firmenfeiern finden häufig statt. Keramik to go zum Bemalen zuhause.")
mk(63,"porzellansalon-sparrenburg-bielefeld","Porzellansalon Sparrenburg","Bielefeld",NW,"sparrenburg@porzellansalon.de",**PS,
 description="Kreativstudio in Bielefeld mit zehn Jahren Erfahrung, in dem du dir Keramik aussuchst, vor Ort bemalst und gebrannt abholst. Platz für 35 Personen. Plätze reservierst du über das Buchungstool.")
mk(64,"porzellansalon-cruewell-bielefeld","Porzellansalon Crüwell","Bielefeld",NW,"cruewell@porzellansalon.de",**PS,
 description="Kreativstudio in Bielefeld mit zehn Jahren Erfahrung, in dem du dir Keramik aussuchst, vor Ort bemalst und gebrannt abholst. Platz für über 30 Personen, mittwochs und donnerstags keine Abholung. Plätze reservierst du über das Buchungstool.")
# ---------- Bochum / Herne / Hattingen
RP_=dict(price_from="15", price_mug="25", price_plate="18-40",
 studio_fee="Keine Studiogebühr · Malslot kostenlos · 2,5 Stunden nach kurzer Einführung",
 price_note="Rohlinge kosten 15–65 €, Tassen ab ca. 25 €, Teller 18–40 €. Farben, Glasur und Brand sind im Preis enthalten.",
 pickup_time="Nach ca. 7 Tagen", hat_instagram=INS("ruhrpottery_nrw"))
mk(69,"ruhrpottery-bochum","Ruhrpottery Bochum","Bochum",NW,"info@ruhrpottery-bochum.de",**RP_,
 description="Keramikmalstudio am Springerplatz in Bochum, etwa zehn Gehminuten vom Bermudadreieck. Du wählst einen Rohling und malst 2,5 Stunden, das Studio glasiert und brennt das Stück bei über 1000 °C. Den Malslot reservierst du online.")
mk(102,"ruhrpottery-herne","Ruhrpottery Herne","Herne",NW,"info@ruhrpottery.com",**RP_,
 description="Keramikmalstudio in Herne, in dem du Keramik allein, mit Freunden oder der Familie gestaltest. Das Team hilft bei der Auswahl und übernimmt Glasieren und Brennen. Den Malslot reservierst du online.")
mk(70,"keramchen-bochum","Keramchen","Bochum",NW,
 tags="reservation-only, kids-friendly, hen-party, corporate-events", hat_instagram=INS("keramchen"),
 studio_fee="Malkursgebühr 5 € pro Person · 2,5 Stunden",
 price_note="Beispiele: Espressotasse 25 €, großer Becher 30 €. Ein zweiter Termin zum Weitermalen kostet 20 € extra, eine Absage am Termin oder Nichterscheinen 25 €. Kinder unter 12 Jahren nur mit Erwachsenem und sollten 2 Stunden am Tisch sitzen können. Die Kurse sind auf 14 Personen begrenzt.",
 pickup_time="Nach ca. 2 Wochen oder nach Absprache · Foto des bemalten Stücks mitbringen",
 special_events="Malkurse für Gruppen von Freunden, Junggesellinnenabschied und Teamevent. Begleitpersonen müssen ebenfalls einen Platz buchen. Termine buchst du online.",
 description="Malstudio in Bochum für kreative Malkurse im Ruhrgebiet. Du gestaltest Tassen, Teller, Schalen und viele weitere Keramikstücke individuell. Einen Termin buchst du online.")
mk(103,"potteery-hattingen","POTTEERY","Hattingen",NW,"info@die-potteery.de",
 tags="reservation-only, kids-friendly, birthday-parties, corporate-events", hat_instagram=INS("die_potteery"),
 studio_fee="Anmeldegebühr 5 € pro Person · Malzeiten 3 Stunden",
 price_note="Einzelpreise der Keramik stehen nicht auf der Website. Malzeiten: Di 15–18, Do 18–21, Fr 15–18, Sa 11–14 und 15–18, So 13–16 Uhr.",
 special_events="Just Paint Wednesday (mittwochs 11–18 Uhr, ohne Reservierung). Kindergeburtstage, Klassenausflüge und Projekte, Firmenevents, Events und Seminare. Zusätzlich ein Teefachgeschäft («Time for Tea»).",
 description="Teefachgeschäft und Keramik-Malstudio im Ruhrgebiet. Bei der POTTEERY kannst du Keramik selbst bemalen, reguläre Malzeiten sind ausschließlich mit Reservierung, mittwochs gibt es den Just Paint Wednesday ohne Reservierung.")
# ---------- Oberhausen / Mülheim
mk(135,"celines-keramik-oberhausen","Celines Keramik","Oberhausen",NW,
 price_from="20",
 studio_fee="Mindestumsatz 20 € pro Person · ca. 3 Stunden",
 price_note="Rohlinge kosten 20–65 €. Mädelsabend mit HeyNala 39 € pro Person zusätzlich zum Keramikstück. Bei späterer Absage oder Nichterscheinen 20 € pro Person, kostenlose Stornierung bis 48 Stunden vorher. Die Terminanfrage über das Formular ist unverbindlich.",
 pickup_time="Nach ca. 2 Wochen · Abholung bis 18 Uhr zu den Öffnungszeiten",
 hat_instagram=INS("celineskeramik"),
 description="Keramikmalstudio in Oberhausen mit Raum für Kreativität, Entspannung und gemeinsame Zeit, im Sommer klimatisiert, im Winter gemütlich warm. Du bemalst Keramik ohne Vorkenntnisse. Termine fragst du über das Formular an.")
mk(137,"pottzauberei-oberhausen","Pottzauberei","Oberhausen",NW,"info@pottzauberei.de",
 tags="kids-friendly, birthday-parties, hen-party, corporate-events", price_from="10",
 studio_fee="Mindestumsatz 15 € pro Person · Material, Glasur und Brand inklusive · Malzeit 2,5 Stunden",
 price_note="Rohlinge kosten ca. 10–60 €.",
 pickup_time="Ca. 2–3 Wochen nach dem Bemalen",
 special_events="Kindergeburtstag: 39 € pro Kind (ab 10 Jahren, 6–9 Kinder, ca. 2 Stunden). Junggesellinnenabschied und Firmenevents, mobile Angebote für Einrichtungen, Pottery to go, Workshops und Events.",
 hat_instagram=INS("pottzauberei"),
 description="Keramikmalstudio in Oberhausen, eine kreative Auszeit für Anfänger und erfahrene Maler. Du bemalst frei ein Stück deiner Wahl, ohne Vorkenntnisse. Dazu gibt es Kindergeburtstage, Workshops und mobile Angebote.")
mk(142,"pottery-oberhausen","Pottery Oberhausen","Oberhausen",NW,"info@pottery-oberhausen.de",
 tags="reservation-empfohlen", price_from="10", price_mug="25", price_plate="18-40",
 studio_fee="Keine Studiogebühr · Malslot kostenlos · 2,5 Stunden · Glasieren und Brand inklusive",
 price_note="Rohlinge kosten 10–60 €, eine Tasse ca. 25 €, Teller meist 18–40 €. Kinder können mitmachen, je nach Alter mit einem Erwachsenen.",
 pickup_time="Nach 7 Tagen",
 hat_instagram=INS("potteryoberhausen"),
 description="Keramikmalstudio in Oberhausen, in dem du einen Rohling aussuchst, in entspannter Atmosphäre bemalst und das Team ihn glasiert und brennt. Eine Reservierung wird empfohlen.")
mk(145,"fileli-keramik-malstudio-muelheim","Fileli Keramik Malstudio","Mülheim an der Ruhr",NW,
 tags="reservation-only", hat_instagram=INS("filelikeramik"),
 price_note="Preise stehen nicht auf der Website. Mystery Bags: 30 € (Keramik im Wert von mindestens 50 €) und 50 € (Wert mindestens 80 €).",
 special_events="Malzeit-Sessions und Specials wie Ladies Night, Mens Night und Potter Heads, Maltüte2Go und Gutscheine. Die Reservierung erfolgt über das Reservierungssystem.",
 description="Keramik-Malstudio in Mülheim an der Ruhr zum Entschleunigen und Keramik bemalen, mit oder ohne Talent. Malzeit-Sessions und Specials werden über das Reservierungssystem gebucht.")
# ---------- Xanten, Meerbusch, Bad Salzuflen, Düren, Stolberg
mk(144,"vernice-keramikmalwerkstatt-xanten","Vernice Keramikmalwerkstatt","Xanten",NW,"janaleurs@vernice-xanten.de",
 tags="reservation-only, hen-party, corporate-events", price_from="15",
 studio_fee="Mindestumsatz 20 € pro Malplatz · keine Kursgebühr · Beratung, Malen, Glasieren und Brennen inklusive",
 price_note="Die meisten Stücke kosten 15–40 €, größere bis 60 €. Absage bis 24 Stunden vorher, sonst 20 € pro Platz. Die Inhaberin wechselt zum 1. Januar 2027, Stücke bitte bis Dezember 2026 abholen.",
 pickup_time="2–14 Tage nach dem Malen · Aufbewahrung höchstens bis Ende 2026",
 special_events="Junggesellenabschiede, Firmenevents und Gruppenmalen. Kindergeburtstage gibt es 2026 nicht mehr, als Alternative MalenToGo. Reservierung per WhatsApp oder E-Mail.",
 hat_instagram=INS("vernice_keramikmalwerkstatt"),
 description="Keramikmalwerkstatt im Herzen von Xanten, in der du Rohlinge wie Tassen, Teller, Schalen, Dosen und Vasen bemalst. Du wirst selbst zum Künstler, die Inhaberin gibt Einführung und Hilfe, glasiert und brennt.")
mk(138,"meerwalt-studio-meerbusch","Meerwalt Studio","Meerbusch",NW,"kontakt@meerwalt-studio.de",
 tags="birthday-parties, corporate-events",
 studio_fee="Keine Studiogebühr · Mindest-Keramikguthaben 20 € pro Sitzplatz · Rohling, Werkzeug, Farben, Glasur und Brand inklusive",
 price_note="Der Preis steht an jedem Stück. Essen ist im Studio nicht erlaubt, Getränke gibt es. Das Studio ist vom 21.12.2026 bis 01.01.2027 geschlossen.",
 pickup_time="Nach etwa einer Woche",
 special_events="Mal-Box 2Go zum Bemalen zuhause (Mindestbestellwert 80 € für Rohlinge), Kindergeburtstage ab 6 Kindern, Firmenevents und private Feiern, optional als All-Inclusive-Paket. Termine buchst du kostenlos über den Online-Kalender.",
 description="Das Meerwalt Studio ist das erste Keramik-Malstudio in Meerbusch-Büderich, in dem Entspannung auf Kreativität trifft. Du wählst einen Rohling, bemalst ihn mit Hilfe vor Ort, das Studio glasiert und brennt ihn.")
mk(154,"keramikmalstudio-malerische-auszeit-bad-salzuflen","Malerische Auszeit","Bad Salzuflen",NW,"info@malerischeauszeit.de",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events", price_from="20.9",
 studio_fee="Keramik-Mindestumsatz 20,90 € pro Person · Malzeit bis zu 3 Stunden",
 price_note="Kostenlose Stornierung bis 48 Stunden vorher, danach 10 € pro Person. Kostenloses Parken direkt vor dem Haus. Mitgebrachte Speisen und Getränke sind nicht erlaubt.",
 special_events="Familienfreundliches Studio, Angebote für Senioren und Kurgäste, (Kinder-)Geburtstag, Junggesellinnenabschied und Gruppenevents (Sonderöffnungen ab 10 Personen auf Anfrage), Babyzeit und Hundepfoten, Malen zuhause und Keramik to Go 24/7.",
 hat_instagram=INS("malerischeauszeit"),
 description="Familienfreundliches Keramikmalstudio in Bad Salzuflen für kreative Auszeiten. Malplätze werden über das Buchungstool reserviert, Getränke und Snacks gibt es vor Ort. Auch Malen zuhause mit der Malbox to go ist möglich.")
mk(165,"maleramik-dueren","Maleramik Düren","Düren",NW,
 tags="birthday-parties, hen-party, corporate-events", price_from="20",
 studio_fee="Keine Studiogebühr · Farben, Glasur und Brand inklusive · du zahlst nur, was du bemalst",
 price_note="Die meisten Stücke kosten 20–45 €. Ab 5 Personen wird eine Anzahlung erbeten. 40 Sitzplätze, zwei Zeitfenster pro Tag. Maleramik gibt es auch in Aachen.",
 pickup_time="Nach ca. 5–7 Tagen · Benachrichtigung, sobald das Stück fertig ist",
 special_events="Geburtstage für Kinder, Erwachsene oder gemischte Gruppen, Junggesellenabschiede und Firmenfeiern/Teamevents, Set to Go und Hand- und Fußabdrücke. Buchung telefonisch oder online.",
 hat_instagram=INS("maleramik.official"),
 description="Kreatives Keramikstudio in Düren, in dem du unglasierte Rohlinge bemalst und das Studio sie glasiert und brennt. Du brauchst nur Lust auf Farbe. Ab 5 Personen wird eine Anzahlung erbeten.")
mk(167,"dein-raum-der-wuensche-stolberg","Dein Raum der Wünsche","Stolberg",NW,"hallo@deinraumderwuensche.de",
 tags="reservation-empfohlen, birthday-parties, corporate-events",
 price_note="Keramik Malabend 10 € pro Termin zuzüglich Keramikstück. Preise für das Bemalen während der Öffnungszeiten stehen nicht auf der Website. Gutscheine von 10 bis 100 €.",
 special_events="Malabende (18–21 Uhr), Kindergeburtstage, private Events und Firmenevents (individuelle Angebote), Workshops und ein Shop mit Geschenken. Plätze reservierst du über den Reservierungskalender.",
 hat_instagram=INS("deinraumderwuensche"),
 description="Kreativ-Raum in Stolberg von Nina, der Keramik bemalen, Workshops und ausgesuchte Geschenke in entspannter Atmosphäre verbindet. Du reservierst dir einen Platz während der Öffnungszeiten oder buchst einen Malabend.")
# ---------- Potsdam / Aachen
mk(41,"paint-your-style-potsdam","Paint your Style Potsdam","Potsdam",BB,"potsdam@paintyourstyle.de",
 tags="kids-friendly, birthday-parties, hen-party, corporate-events", price_from="15",
 studio_fee="Keramik-Mindestumsatz 15 € pro Person · Begleitperson ohne Malen 15 € Sitzplatz · ca. 2,5 Stunden (nach 18 Uhr 2 Stunden)",
 price_note="Einzelpreise der Keramik stehen auf der Standortseite nicht.",
 pickup_time="Ca. 1–3 Tage (allgemeine Angabe der Paint-your-Style-Website)",
 special_events="Online-Reservierung bis 4 Personen, größere Gruppen, Kindergeburtstage, Schul- und Kita-Ausflüge, Junggesellenabschiede und Firmenevents nur per E-Mail.",
 description="Malstudio für Ideen auf Keramik in Potsdam. Du suchst dir Keramik aus, bemalst sie selbst, und das Team glasiert und brennt sie. Geöffnet dienstags bis freitags 13–20 Uhr, am Wochenende ab 10:30 Uhr.")
mk(111,"farbenfleck-aachen","Farbenfleck Aachen","Aachen",NW,
 tags="walk-in, reservation-empfohlen, birthday-parties, hen-party, corporate-events", price_from="20",
 studio_fee="Keine Studiogebühr · Farben, Glasur und Brand inklusive · du zahlst nur, was du bemalst",
 price_note="Die meisten Stücke kosten 20–45 €. Ab 5 Personen wird eine Anzahlung erbeten. 40 Sitzplätze, zwei Zeitfenster pro Tag. Farbenfleck Aachen ist rechtlich eigenständig und hat keine Verbindung zu Farbenfleck Düren.",
 pickup_time="Nach ca. 5–7 Tagen",
 special_events="Geburtstage für Kinder, Erwachsene und gemischte Gruppen, Junggesellenabschiede (optional mit Glitzer und Prosecco) und Firmenfeiern/Teamevents. Spontanbesuche sind erlaubt, Zeitslots online oder telefonisch.",
 hat_instagram=INS("farbenfleck.official"),
 description="Keramik-Mal-Studio im Zentrum von Aachen, in dem du unglasierte Keramikrohlinge bemalst. Das Studio glasiert und brennt sie. Hier wird nichts bewertet, nur bestaunt. Spontan vorbeikommen geht, Zeitslots buchst du online oder telefonisch.")
json.dump(raw,open(p,'w'),indent=2,ensure_ascii=False); open(p,'a').write("\n")
print(len(d), sum(1 for s in d if s.get('country')=='DE'))
