import json,sys,io,contextlib,re
sys.path.insert(0,'editor-server/scratch/outscraper-de3')
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_report3 as b
hours_de=b.hours_de
RAW=json.load(open('editor-server/scratch/outscraper-de5/_raw_dump.json',encoding='utf-8'))['N']
p='editor-server/data/studios.json'
raw=json.load(open(p)); d=raw if isinstance(raw,list) else raw['studios']
tmpl=[s for s in d if s.get('slug')=='layers-koeln'][0]; keys=list(tmpl.keys())
slugs={s['slug'] for s in d}
INS=lambda u:"ja, https://www.instagram.com/"+u+"/"
def mk(idx,slug,name,city,region,email="",addr=None,**kw):
    r=RAW[idx]; assert slug not in slugs,slug
    s={k:"" for k in keys}
    street=(r['street'] or '').replace('Str.','Straße').replace('str.','straße')
    plz=str(r['postal_code']).zfill(5)
    s.update({"slug":slug,"name":name,"address":addr or f"{street}, {plz} {city}","city":city,
      "phone":(r['phone'] or '') if r['phone']!='None' else "","website":re.sub(r'%3F.*','',r['website']) if r['website'] else "","email":email.lower(),
      "opening_hours":hours_de(r['working_hours']),"tags":"","images":"[]","image":"","custom_faq":"[]","contacted":False,"featured":False,
      "quelle_hinweis":"Outscraper (Google Maps); Aufnahme anhand der Website geprüft am 19.10.2026",
      "lat":float(r['latitude']),"lng":float(r['longitude']),"country":"DE","currency":"EUR","postcode":plz,"region":region})
    s.update(kw); slugs.add(slug); d.append(s); return s
HH,FR,MU="Hamburg","Frankfurt am Main","München"
# ---------------- HAMBURG ----------------
mk(0,"smileandpeace-hamburg","smileandpeace",HH,"HH","hello@smileandpeace.com",addr="Steinheimplatz 10, 22767 Hamburg",
 hat_instagram=INS("smileandpeace.keramik"),
 price_note="Preise stehen nicht auf der Website. Das Studio hat in Hamburg zusätzlich Getränke und Snacks und einen zweiten Standort in Grömitz.",
 special_events="Malen-to-go zum Mitnehmen. Termine reservierst du über die Reservierungsseite des Hamburger Standorts. Workshops gibt es vor allem in Grömitz.",
 description="Keramik-Malstudio und Töpferstudio in Hamburg, das Keramik bemalen, Töpfern und kreative Workshops anbietet, mit Getränken und Snacks vor Ort. Ein Ort, der Menschen Freude machen soll. Das Studio hat einen zweiten Standort in Grömitz.")
mk(1,"die-malbucht-hamburg","Die Malbucht",HH,"HH",
 tags="walk-in, reservation-empfohlen, birthday-parties, hen-party, corporate-events",
 pickup_time="Nach 7 Tagen, manchmal früher · nach 6 Monaten werden nicht abgeholte Stücke gespendet",
 price_note="Preise stehen nicht auf der Website. Es gibt eine große Auswahl an Rohlingen, Farben, Schablonen und Stempeln an einer Farbbar.",
 special_events="Kindergeburtstag (eigene Seite), Junggesellinnenabschied sowie Teamevents und Firmenfeiern als eigenes Angebot. Spontane Besuche sind möglich, vorher anrufen wird empfohlen, eine Online-Reservierung sichert den Platz.",
 hat_instagram=INS("diemalbucht"),
 description="Keramik-Malstudio in Hamburg, in dem du einen Rohling aussuchst, an der Farbbar bemalst und nach dem Glasieren und Brennen abholst. Für Einzelgäste, Paare und größere Runden, mit Angeboten für Junggesellinnenabschiede, Teamevents und Kindergeburtstage.")
mk(2,"die-keramikmaler-hamburg","Die Keramikmaler",HH,"HH","heidrun.schmuck@diekeramikmaler.de",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 pickup_time="Nach 2–3 Tagen",
 price_note="Die Rohlinge stammen größtenteils aus Italien. Für mobile Termine fällt ein Aufpreis für Fahrt und Transport an.",
 special_events="Kindergeburtstag zum Festpreis von 20 € pro Kind (Auswahl aus Rohlingen), ca. 2 Stunden. Außerdem Junggesellinnenabschiede, Gruppen, Malstunden mit Freunden, Kollegen oder Familie, Events für Firmen, Kitas und Schulen sowie Fuß- und Handabdrücke von Kleinkindern. Termine nur nach Absprache, auch zu dir nach Hause.",
 description="Kreativangebot von Heidrun Schmuck in Hamburg-Iserbrook: Du bemalst Keramikrohlinge mit Pinsel und Farbe, das Team glasiert und brennt sie. Die Werkstatt hat kein Ladengeschäft und ist nur nach Terminabsprache geöffnet, auf Wunsch kommt sie auch zu dir.")
mk(3,"keramikmalstuebchen-hamburg","KeramikMalStübchen",HH,"HH",
 tags="birthday-parties",
 price_note="Preise stehen nicht auf der Website. Du kannst Becher, Teller, Schalen, Tierchen und andere Gebrauchskeramik bemalen.",
 special_events="Feiern im Stübchen, Keramik to go, «Wir malen für Sie» und Gutscheine.",
 description="Keramik-Malstübchen in Hamburg-Blankenese in liebevoll eingerichteten Räumen. Du bemalst Becher, Teller, Schalen, Tierchen und andere Gebrauchskeramik in entspannter Atmosphäre. Termine kannst du reservieren.")
mk(5,"vivilou-kreativstudio-hamburg","Vivilou Kreativstudio",HH,"HH","kontakt@vivilou-kreativstudio.de",
 tags="birthday-parties, hen-party",
 pickup_time="Einige Tage später",
 special_events="Kindergeburtstage und Gruppen ab 8 Personen (auch JGA) plant das Studio individuell. Daneben Schmuckworkshops und eine Keramikbox.",
 hat_instagram=INS("vivilou.kreativstudio"),
 description="Kreativstudio in Hamburg-Neustadt, in dem du Keramik (Tassen, Teller, Schalen, Hundenäpfe und mehr) bemalen oder Schmuck aus Glas-, Süßwasserperlen und Edelsteinen gestalten kannst. Das Studio brennt deine Keramik, einen Termin buchst du online.")
mk(7,"porzellanfraeulein-hamburg","Porzellanfräulein",HH,"HH",
 tags="kids-friendly, birthday-parties, hen-party, corporate-events", price_from="3.5", price_mug="19.50-26", price_plate="12-49",
 studio_fee="Keine Studiogebühr · Alles-Inklusive-Preise (Keramik, Farben, Glasur und Brand)",
 price_note="Becher 19,50–26 €, Teller 12–49 €, Kinderkram 3,50–22 €.",
 special_events="Kindergeburtstag, Junggesellenabschied, Teambuilding, Einladungskarten, Babyfußabdruck und Zuhause malen.",
 hat_instagram=INS("porzellanfraeulein"),
 description="Keramik-Mal-Laden in Hamburg-Winterhude, in dem du Keramik selbst bemalst, vor Ort oder zuhause. Für Einzelgäste, Paare, JGA und Geburtstage. Du kannst reservieren.")
mk(8,"ceramic-stars-hamburg","Ceramic Stars",HH,"HH",
 tags="birthday-parties, hen-party, corporate-events", price_from="10", price_mug="19-26", price_plate="12-49",
 studio_fee="Mindestumsatz 20 € pro Person · Preis je Stück inklusive Kursgebühr, Farben, Material und Brand",
 price_note="Preise ab 10 €: Tassen und Becher 19–26 €, Teller 12–49 €, Untersetzer und Fliesen 5–19 €, Vasen 12–59 €, Krüge 18–42 €, Dosen 22–38 €, Teekannen 48 €.",
 pickup_time="Nach 2 Wochen",
 special_events="Geburtstage, JGA, Betriebsveranstaltungen, Babyshower und Teambuilding. Ab 6 Personen wird ein Tisch gedeckt, eigene Snacks und Kuchen sind erlaubt.",
 hat_instagram=INS("ceramic.stars.hamburg"),
 description="Keramik-Malstudio in Hamburg-Eimsbüttel mit über 150 Teilen und mehr als 80 Farben. Du suchst dir ein Stück aus, bemalst es, und das Atelier brennt es. Keine Vorerfahrung nötig. Termine buchst du über den Online-Kalender.")
mk(9,"made-by-you-hamburg","Made by you Hamburg",HH,"HH","info@madebyyou.de",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties", price_from="12",
 studio_fee="Keine Studiogebühr · Alles-Inklusive-Preise (Rohling, Farben, Glasur und Brand)",
 price_note="Ab-Preise: Becher und Tassen 15 €, Teller und Platten 15 €, Schalen 13 €, Krüge 17 €, Vasen 17 €, Dosen 15 €, Figuren 12 €, Spardosen 20 €. Es gibt über 300 Formen und über 60 lebensmittelechte Farbtöne.",
 special_events="Kindergeburtstage, Gruppen-Events, Keramik to go (zuhause bemalen, im Studio brennen). Am Wochenende besser anmelden, sonst einfach kommen und malen.",
 description="Keramik-Malstudio in Hamburg-Eimsbüttel, in dem du einfach kommen und malen kannst, am Wochenende besser mit Anmeldung. Über 300 Formen, Pinsel, Stempel und Schablonen, bei schönem Wetter auch draußen.")
mk(12,"malmalkeramik-hamburg","MalmalKeramik",HH,"HH","malmal@malmalkeramik-hamburg.de",
 tags="birthday-parties, hen-party, corporate-events", price_from="13", price_mug="19-36", price_plate="13-37",
 price_note="Becher 19–36 € (je nach Größe), Teller 13–37 €, Schalen 15–35 €, Etagere 69 €, Krug 47 €.",
 pickup_time="Einige Tage später",
 special_events="Gruppenangebote für Junggesellen- und Junggesellinnenabschied, Geburtstag, Teamevents und Abende mit Freunden, Firmenfeier und Malen im Garten. Der Außer-Haus-Service stellt Material für Feiern zuhause bereit.",
 description="Keramik-Malstudio in Hamburg, in dem du vorgefertigte Keramik nach deinen eigenen Vorstellungen bemalst, zur Entspannung, für persönliche Geschenke, Feiern und Gruppen. Nach dem Glasieren und Brennen holst du die Stücke ab.")
KC="Keramik selbst bemalen, Clay Club für Erwachsene und Kids Club für Kinder. Termine buchst du über die Website."
mk(13,"kunst-club-heussweg-hamburg","Kunst Club Heußweg",HH,"HH",tags="kids-friendly",
 price_note="Clay Club 75 €, Kids Club Probestunde 28 €. Einen Preis für Keramik selbst bemalen nennt die Website nicht.",
 special_events=KC,
 description="Kunst Club in Hamburg-Eimsbüttel mit den Angeboten Keramik selbst bemalen, Clay Club (Töpfern) und Kids Club für Kinder. Du buchst deinen Platz online.")
mk(24,"kunst-club-grindel-hamburg","Kunst Club Grindel",HH,"HH",tags="kids-friendly",
 price_note="Clay Club 75 €, Kids Club Probestunde 28 €. Einen Preis für Keramik selbst bemalen nennt die Website nicht.",
 special_events=KC,
 description="Kunst Club im Hamburger Grindelviertel mit den Angeboten Keramik selbst bemalen, Clay Club (Töpfern) und Kids Club für Kinder. Du buchst deinen Platz online.")
mk(16,"flame-n-go-hamburg","Flame n Go",HH,"HH","info@flame-n-go.de",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events", price_from="3.5",
 studio_fee="Rohlinge ab 3,50 €, Farben und Brennen inklusive",
 pickup_time="Etwa 7–10 Werktage · ist der Ofen früher voll, meldet sich das Team",
 special_events="Gruppen-Events bis 30 Personen für JGA, Familienfeiern und Vereinsausflüge, auf Wunsch wird die untere Etage gemietet. Geburtstage für Kids und Erwachsene, Teambuilding, Schulklassen und Kitas auch montags und dienstags nach Absprache. Digitales Mal-Studio zum Üben.",
 hat_instagram=INS("flamengo.keramik"),
 description="Zweistöckiges Keramikstudio in Hamburg-Schnelsen mit Hunderten Rohlingen, Farben und Anleitung durch das Team. Spontan vorbeikommen geht unter der Woche, ein Tisch kann angefragt werden. Für Einzelne, Freundesgruppen, Familien und Firmen.")
mk(29,"keramikkiste-hamburg","Keramikkiste",HH,"HH","info@keramik-kiste.de",addr="Bergstedter Chaussee 120, 22395 Hamburg",
 tags="reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events", price_from="10", price_mug="13-22", price_plate="13-28",
 studio_fee="Alle Preise inklusive Rohkeramik, Farben, Utensilien, Glasur und Brand · ca. 1,5–2 Stunden",
 price_note="Becher und Tassen 13–22 €, Teller 13–28 €, Schalen und Schüsseln 13–59 €, Tiere zum Hinstellen 10–15 €.",
 pickup_time="Ca. 3 Wochen je nach Saison, der Termin wird am Maltag genannt · nicht abgeholte Stücke werden nach 6 Monaten entsorgt · beim Korb zum Mitnehmen ca. 1 Woche nach dem Brennen",
 special_events="Kindergeburtstage (bis 2,5 Stunden), Geburtstage, Junggesellen- und Junggesellinnenabschiede und Firmenfeiern mit bis zu 46 Plätzen. Die Preise für Feiern richten sich nach Teilnehmerzahl, Sortiment und Getränken, Groupon-Coupons gelten nicht dafür. Außerdem Geschenkekiste und Korb zum Mitnehmen.",
 description="Keramik-Malstudio in Hamburg-Bergstedt, in dem du mit Pinseln und Techniken wie Blubbern, Siebdruck, Kratzen und Schablonen kreativ wirst. Eine Reservierung per Telefon oder E-Mail wird empfohlen.")
mk(34,"lieblingsstueck-hamburg","Lieblingsstück",HH,"HH",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise der Keramik stehen nicht auf der Website. Workshops (Strand und Meer, Marmorieren, Konfetti) kosten 7 € Workshopgebühr plus Keramikstück plus Getränke. Late Night Malen donnerstags 20–22:30 Uhr.",
 special_events="Kindergeburtstage und Kindergruppen sonntags 14–16 Uhr, bis 3 Monate im Voraus buchbar. Außerdem Familienfeiern, Weihnachtsfeiern, Junggesellenabschiede, Klassenausflüge und Firmenevents, auf Anfrage auch außerhalb der Öffnungszeiten. Keramik @ Home.",
 hat_instagram=INS("lieblingsstueck_hamburg"),
 description="Keramikmalstudio in Hamburg-Bergedorf, in dem du Teller, Tassen, Schalen, Figuren und Bilderrahmen bemalst, mit Schablonen und Aufklebern, ohne Vorkenntnisse, und dazu Kaffee oder Tee trinkst. Die Malzeiten sind fest und müssen reserviert werden.")
mk(25,"keramikstube-rosengarten","Keramikstube Rosengarten","Rosengarten","NI","keramikstube.rosengarten@gmail.com",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Bei kurzfristiger Absage fällt eine Stornogebühr von 15 € pro Platz an. Es gibt über 100 Keramikstücke zur Auswahl.",
 pickup_time="Am Donnerstag nach dem Glasurbrand zwischen 17 und 19 Uhr, in der Regel am Donnerstag der folgenden Woche",
 hat_instagram=INS("keramikstube.rosengarten"),
 description="Kreativstudio zum Bemalen von Keramik in Rosengarten (Landkreis Harburg). Du wählst aus über 100 Keramikstücken und Farben, das Studio übernimmt Glasur und Brand. Auch Anfänger sind willkommen. Einen Tisch buchst du über das Kontaktformular.")
mk(100,"pottery-and-pearls-elmshorn","Pottery & Pearls","Elmshorn","SH","info@keramikperlenwerkstatt.de",
 tags="birthday-parties", price_from="3.5",
 studio_fee="Bis zu 3 Stunden Kreativzeit · Getränke, kostenlose Parkplätze und persönliche Einführung inklusive",
 price_note="Preise laut Website von 3,50 € bis 44 €.",
 special_events="Kindergeburtstage, Veranstaltungen und Gruppen, mobile Keramikangebote und Keramik für zuhause. Reservierung online oder telefonisch.",
 hat_instagram=INS("pottery_and_pearls"),
 description="Entspanntes Keramikstudio in Elmshorn, in dem du unglasierte Stücke bemalst und das Studio sie glasiert und brennt. Du hast bis zu drei Stunden Kreativzeit, dazu gibt es Getränke und eine persönliche Einführung.")
# ---------------- FRANKFURT ----------------
mk(20,"coloria-frankfurt","Coloria",FR,"HE","",
 tags="kids-friendly, corporate-events",
 price_note="Folgebuchungen für Gruppen kosten 60 € pro zusätzlicher Stunde. Wer nicht fertig wird, zahlt ab dem zweiten Besuch 7 € pro Sitzung und Stück. Einzelpreise der Keramik stehen nicht auf der Website.",
 special_events="Töpfern für Kinder, Events, Feiern, Gruppen und Teamevents. Keramik malen, Töpfern, Drehen-Schnupperkurse, mehrwöchige Kurse und Freie Werkstatt.",
 hat_instagram=INS("coloriafrankfurt"),
 description="Keramikkunstschule in Frankfurt, seit 2004. Hier kannst du Keramik malen, formen, drehen oder einfach ausprobieren, allein, mit Freunden, Familie oder in Gruppen. Die Reservierung online gilt für Keramik malen.")
mk(21,"keramiklabor-frankfurt","Keramiklabor Frankfurt",FR,"HE","info@keramiklabor-frankfurt.com",addr="Textorstraße 11, 60594 Frankfurt am Main",
 tags="hen-party", price_from="14", price_mug="15-30", price_plate="16-38",
 price_note="Tassen 17–30 €, Becher 15–26 €, Teller 16–38 €, Schüsseln 22–50 €, Dosen 18–32 €, Kannen 20–42 €, Sonstiges (Figuren, Küchenartikel, Schilder, Fliesen, Napfe) 14–60 €. Das Studio ist ab 16.10.2026 an der neuen Adresse Textorstraße 11, Fotos und Online-Einträge zeigen noch den alten Standort.",
 special_events="JGA und Geburtstagsfeier, Events, Töpferkurse, Belly Bowls und Töpferfortbildungen. Termine für Keramik bemalen buchst du online.",
 hat_instagram=INS("keramiklaborfrankfurt"),
 description="Kreativstudio in Frankfurt zum Bemalen von Keramik mit Geschirr und anderen Rohlingen, dazu Töpferworkshops und Fortbildungen. Du buchst eine kreative Auszeit online.")
mk(22,"paint-your-style-frankfurt","Paint your Style Frankfurt",FR,"HE","",
 tags="reservation-empfohlen",
 price_note="Einzelpreise der Keramik und ein Mindestumsatz stehen auf der Standortseite nicht. Das Zeitfenster um 18 Uhr ist Gästen ab 15 Jahren vorbehalten. Kindergeburtstage und Partys bietet der Standort laut Website nicht mehr an.",
 pickup_time="Ca. 1–3 Tage (allgemeine Angabe der Paint-your-Style-Website)",
 special_events="Reservierung per E-Mail oder Telefon, am Wochenende Zeitfenster um 11, 14:30 und 18 Uhr, unter der Woche freie Zeiten.",
 description="Malstudio für Ideen auf Keramik in Frankfurt (Landgrafenstraße 13). Du suchst dir Keramik aus, bemalst sie selbst, und das Team glasiert und brennt sie. Eine Reservierung per Mail oder Telefon wird empfohlen. Mittwoch ist Ruhetag.")
mk(37,"pintoyo-frankfurt","Pintoyo",FR,"HE","info@pintoyo.de",
 price_from="15", price_mug="15-30", price_plate="16-55",
 studio_fee="Preise inklusive Keramik, Farbglasuren und Brand · kostenlose Einführung, auch auf Englisch",
 price_note="Teller 16–55 €, Tassen 15–30 €, kleine Schalen 16–26 €. Lampen-Workshop ca. 50–70 € pro Lampe.",
 pickup_time="Ca. 1 Woche nach dem Bemalen",
 special_events="Workshops und Events (Zeiten z. B. 18–21:30 Uhr). Du buchst einen Tisch zu den Öffnungszeiten.",
 hat_instagram=INS("pintoyo.keramikwerkstatt"),
 description="Kreativwerkstatt für Keramikbemalung in Frankfurt-Bornheim mit Rohkeramik, Farbglasuren, Werkzeugen und Techniken. Auf Wunsch gibt es eine kostenlose Einführung, auch auf Englisch.")
mk(65,"made-by-you-frankfurt","Made by you Frankfurt",FR,"HE","info@madebyyou-frankfurt.de",
 tags="kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Es gibt über 300 Rohlinge zur Auswahl.",
 pickup_time="Abholung während der Öffnungszeiten bis 30 Minuten vor Ladenschluss",
 special_events="Geburtstage für Kinder, JungesellInnen-Abschiede, Firmenfeiern, Partybox, Brennservice sowie Töpferworkshops und -kurse. Tischreservierungen zum Malen über die Website.",
 description="Keramik-Mal-Studio in Frankfurt-Bornheim, in dem du aus über 300 Rohlingen deinen Liebling aussuchst und ganz individuell gestaltest. Geöffnet Dienstag bis Sonntag von 12 bis 20 Uhr.")
mk(67,"keramikzauber-frankfurt","KeramikZauber Frankfurt",FR,"HE","mail@keramikzauber-frankfurt.de",
 tags="walk-in, reservation-empfohlen, birthday-parties, hen-party",
 special_events="Gruppen und Events für Geburtstage und Junggesellenabschiede, Themenabende und Gutscheine. Die Reservierung wird empfohlen, spontane Gäste sind willkommen, wenn Plätze frei sind.",
 hat_instagram=INS("keramikzauber.frankfurt"),
 description="Entspanntes Keramik-Malstudio in Frankfurt, in dem du ohne Vorerfahrung dein Stück aussuchst und bemalst. Eine Reservierung wird empfohlen, spontane Gäste sind willkommen, wenn Plätze frei sind.")
mk(68,"studio-dalla-frankfurt","Studio Dalla",FR,"HE","hi@studiodalla.de",
 tags="kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Einen Preis für das Keramik bemalen nennt die Website nicht. Töpfern Handaufbau 45 € pro Person. Alle Preise inklusive 19 % MwSt.",
 special_events="Kindergeburtstag in drei Paketen: Rosemarie ab 20 € pro Kind (Töpfern 40 €), Pablo ab 30 € (Töpfern 50 €), Yoko ab 60 € (Töpfern 70 €), 2 Stunden. Außerdem Teamevents, JGA, Familienevents, Dalla Mal Club (Kids und Teens ab 4/5 Jahren, 1,5 Stunden) und Ferienangebote wie ein Comic-Workshop ab 8 Jahren.",
 hat_instagram=INS("studiodalla_"),
 description="Kreativstudio im Frankfurter Nordend mit Keramik bemalen, Malkursen, Töpfern, kreativen Workshops und Events für Kinder, Erwachsene und Gruppen. Vor Ort wählst du aus ausgesuchten Rohlingen und arbeitest frei oder mit Anleitung.")
mk(94,"werkraum-hanau","Werkraum","Hanau","HE","info@werkraum-hanau.de",
 price_note="Preise für das Keramik bemalen stehen nicht auf der Website. Der Lino-Print-Workshop kostet 49 € (Material inklusive).",
 special_events="Workshops (z. B. Lino-Print, PRINTLAB), Specialty Coffee, ein Shop und Ausstellungen. Termine buchst du über das Buchungssystem.",
 hat_instagram=INS("werkraum.hanau"),
 description="Kreativer Treffpunkt in der Hanauer Innenstadt mit Keramik bemalen, Workshops, Specialty Coffee, Shop und Ausstellungen. Das Keramikbemalen ist Mittwoch bis Samstag möglich, Montag und Dienstag sind Ruhetage.")
mk(95,"keramiktraum-bad-homburg","keramiktraum","Bad Homburg","HE","hallo@keramik-traum.com",addr="Obergasse 17, 61348 Bad Homburg",
 price_note="Preise für das Keramik bemalen stehen nicht auf der Website. Workshops: Kristallglasuren 15 €, Blubbern 10 €, Farbverlauf 10 € (jeweils inklusive Begrüßungssekt und Materialien, zuzüglich Keramikstück). After-Work-Malen mittwochs bis 21 Uhr.",
 special_events="Workshops (18:15–21 Uhr), After-Work-Malen, Feiern und Gutscheine.",
 description="Keramikmalstudio in Bad Homburg, gegründet 2023, im Herzen der Stadt. Du bemalst Keramik, dazu gibt es Workshops wie Kristallglasuren, Blubbern und Farbverlauf und mittwochs After-Work-Malen.")
mk(96,"keramik-studio-altmannsberger-dietzenbach","Keramik-Studio Altmannsberger","Dietzenbach","HE","keramik.altmannsberger@t-online.de",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Das Studio öffnet nur für mindestens 2 Personen. Zeitfenster 11–14 und 15–18 Uhr.",
 special_events="Geburtstage, Junggesellen- und Junggesellinnenabschiede, Teambuilding, Hochzeiten und Abschiede. Mittwoch und Donnerstag sind für Großgruppen von Schulen, Firmen und Kindergärten reserviert. Zuhause malen. Termine bitte schriftlich.",
 description="Keramik-Malstudio in Dietzenbach von Ingo und Gaby Altmannsberger. Du bemalst allein, zu zweit, in Gruppen oder mit der Familie, als Geschenk oder zur Feier. Geöffnet Freitag bis Sonntag, Termine bitte schriftlich.")
mk(97,"lonia-keramik-darmstadt","Lonia Keramik","Darmstadt","HE","info@lonia-keramik.de",
 tags="hen-party, corporate-events",
 price_note="Preise für das Keramik bemalen stehen auf einer eigenen Preisseite. Tee und Erfrischungen sind inklusive. Zur Abholung bitte Tüte und Polstermaterial mitbringen.",
 pickup_time="Ca. 4 Wochen nach dem Bemalen",
 special_events="Teambuilding für Firmen, Junggesellinnenabschiede und Geburtstage, Afterwork-Events und «Wine & Design». Gebucht wird über das Reservierungssystem.",
 hat_instagram=INS("lonia_keramik"),
 description="Keramik-Kreativstudio in Darmstadt nahe dem Hauptbahnhof mit unbemalter Keramik, Glasuren, Werkzeugen und einer Einführung. Für Familien, Freunde und Teambuilding, mit Tee und Erfrischungen.")
# ---------------- MÜNCHEN ----------------
mk(38,"isa-keramikbemalen-muenchen","ISA Keramikmalstudio",MU,"BY",
 tags="kids-friendly, birthday-parties, hen-party",
 pickup_time="Abholung Di–Fr",
 special_events="Kindergeburtstage, Gruppen und Events, JGA sowie Schulklassen und Kindergärten. Termine buchst du online.",
 hat_instagram=INS("isa.muenchen"),
 description="Kreatives Keramik-Malstudio in München, ein Ort zum Wohlfühlen, Ausprobieren und Spaß haben. Termine buchst du online, außerdem gibt es Angebote für Gruppen, Schulklassen und Kindergärten.")
mk(39,"froh-und-bunter-muenchen","froh + bunter",MU,"BY","info@froh-und-bunter.de",addr="Sebastiansplatz 11, 80331 München",
 tags="reservation-empfohlen, corporate-events", price_from="20",
 studio_fee="Mindestumsatz 20 € pro Person, auch für Begleitpersonen · 2 Stunden",
 price_note="Einzelpreise stehen auf den Produktseiten. Kinder unter 14 Jahren nur mit einem Erwachsenen, keine Kinder unter 7 Jahren und keine Kinderwagen. Afterwork-Workshops 60 €. Malbox zuhause mit Versand für 10 € (Deutschland) oder 25 € (EU).",
 special_events="Bis 5 Personen online buchbar, größere Gruppen per E-Mail. Afterwork-Painting-Workshops am Abend, Teamevents, Weihnachtsfeiern und Malbox für Kindergeburtstage zuhause. Reservierung bis zu 2 Monate im Voraus.",
 hat_instagram=INS("frohundbunter"),
 description="Kreativstudio nahe dem Münchner Viktualienmarkt, seit rund 20 Jahren tagsüber zum Keramik bemalen und abends für Afterwork-Workshops, kürzlich von Elif und Saffet übernommen. Du suchst dir einzigartige Keramik aus, für dich oder als Geschenk.")
mk(40,"the-purrfect-studio-muenchen","The Purrfect Studio",MU,"BY","info@the-purrfect-studio.com",
 tags="reservation-only, kids-friendly, corporate-events",
 price_note="Preise stehen nicht auf der Website. Das Studio ist mobil: samstags im OGM-Loft (Heimeranstraße 70), sonntags in der Tulbeckstraße 39, für Einzelevents auch an anderen Orten, auch privat und im Freien.",
 pickup_time="Glasieren und Brennen dauern ca. 3 Tage",
 special_events="Teamevents und private Gruppenfeiern, Workshops, Matcha und Mocktails. Du reservierst deinen Platz über das Buchungssystem.",
 hat_instagram=INS("the.purrfect.studio"),
 description="Mobiles Keramikstudio in München, das Keramik bemalen mit Matcha und Mocktails verbindet. Für Kinder und Erwachsene, samstags und sonntags an festen Orten, außerdem für Teamevents und private Gruppenfeiern.")
mk(42,"frau-farbenfroh-muenchen","Frau Farbenfroh",MU,"BY","reservierung@frau-farbenfroh.com",
 tags="kids-friendly", price_from="10",
 studio_fee="Mindestumsatz 20 € pro Person, auch für Begleitpersonen · 2,5 Stunden",
 price_note="Kleine Stücke 10–29 €, größere 30–60 €, Farben, Glasur und Brennen inklusive. Kinder ab 6 Jahren sind willkommen, bis 14 Jahre in Begleitung eines Erwachsenen.",
 pickup_time="Nach ca. 5 Tagen · fertige und unfertige Stücke werden bis zu 6 Wochen aufbewahrt",
 special_events="Online-Reservierung bis 6 Personen, ab 7 Personen per E-Mail. Fußabdrücke von Kindern bis 12 Monate mit ungiftigen Farben.",
 hat_instagram=INS("frau_farbenfroh_keramik"),
 description="Keramik-Studio in München-Haidhausen mit über 300 Rohlingen, in dem du Keramik selbst bemalst. Eine kreative Auszeit zum Abschalten und Gestalten, Farben, Glasur und Brennen sind im Preis inklusive.")
PYSM=dict(tags="reservation-empfohlen, kids-friendly, birthday-parties",
 price_note="Einzelpreise der Keramik und ein Mindestumsatz stehen auf der Standortseite nicht. Das Zeitfenster um 18 Uhr ist Gästen ab 15 Jahren vorbehalten. Gruppen mit mehr als 5 Personen nutzen ein eigenes Formular.",
 pickup_time="Ca. 1–3 Tage (allgemeine Angabe der Paint-your-Style-Website)",
 special_events="Kindergeburtstage mit Zeitfenster um 15:30 Uhr, dienstags bis donnerstags. Zeitfenster 12, 15 und 18 Uhr. Reservierung online über Reservino.")
mk(43,"paint-your-style-muenchen-maxvorstadt","Paint your Style München Maxvorstadt",MU,"BY",**PYSM,hat_instagram=INS("paintyourstyle_muenchen"),
 description="Malstudio für Ideen auf Keramik in München-Maxvorstadt. Du suchst dir Keramik aus, bemalst sie selbst, und das Team glasiert und brennt sie. Geöffnet dienstags bis samstags, im November und Dezember auch sonntags.")
mk(51,"paint-your-style-muenchen-schwabing","Paint your Style München Schwabing",MU,"BY",**PYSM,
 description="Malstudio für Ideen auf Keramik in München-Schwabing. Du suchst dir Keramik aus, bemalst sie selbst, und das Team glasiert und brennt sie. Geöffnet dienstags bis samstags, im November und Dezember auch sonntags.")
mk(53,"paint-your-style-muenchen-harras","Paint your Style München Harras",MU,"BY",**PYSM,
 description="Malstudio für Ideen auf Keramik am Harras in München. Du suchst dir Keramik aus, bemalst sie selbst, und das Team glasiert und brennt sie. Geöffnet dienstags bis samstags, im November und Dezember auch sonntags.")
mk(44,"die-keramikothek-muenchen","Die Keramikothek",MU,"BY","hallo@diekeramikothek.de",
 tags="kids-friendly, birthday-parties", price_from="9",
 studio_fee="Mindestumsatz 20 € pro Person · 2,5 Stunden pro Buchung",
 price_note="Kleine Stücke 9–29 €, größere 30–60 €, inklusive Keramik, Farbe, Glasur und Brand. Sitzplätze werden nur für Malende reserviert. Kinder ab 7 Jahren empfohlen, unter 13 Jahren mit Erwachsenen.",
 pickup_time="Fertige Stücke werden bis zu 4 Wochen aufbewahrt · zuhause bemalte Stücke ca. 10 Tage nach Abgabe zum Brennen",
 special_events="Geburtstagsfeiern, Events und Gruppen ab 6 Personen (per E-Mail). Kinderfreundliche Farben und einfache Motive.",
 hat_instagram=INS("die_keramikothek"),
 description="Kreativstudio an der Münchner Freiheit, in dem Menschen jeden Alters gemeinsam Keramik bemalen, für Familienzeit, Geburtstage, Events oder zur Entspannung. Reservierung online.")
mk(45,"maloase-muenchen","MalOase",MU,"BY",
 tags="kids-friendly, birthday-parties, hen-party, corporate-events", price_from="15",
 studio_fee="Mindestwert 15 € pro Person · Malslot maximal 2,5 Stunden",
 price_note="Es gibt einen Mindestwert von 15 € pro Person. Einzelpreise stehen nicht auf der Website.",
 special_events="Gruppen ab 7 Personen (auch JGA und Firmenfeiern) per E-Mail, Kindergeburtstage, Kurse für Schulen und Kindergärten, Baby-Fuß- und Handabdrücke sowie Themenabende und Workshops. Die MalOase nutzt 100 % Ökostrom.",
 description="Keramik-Malstudio in München-Laim mit offenen Malslots, Gruppenevents, Kursen für Schulen und Kindergärten sowie Themenabenden. Du gestaltest dein eigenes Keramikkunstwerk und buchst online.")
mk(46,"keramikunst-pinselstrich-muenchen","Keramikunst & Pinselstrich",MU,"BY","info@keramik-pinsel.de",
 tags="kids-friendly, birthday-parties", price_from="21",
 studio_fee="Mindestwert 21 € pro Reservierung beim Malen · nicht malende Gäste zahlen 21 € Sitzplatz · 2 Stunden Malzeit",
 price_note="Zahlung nur bar oder per EC-Karte. Kinder unter 13 Jahren nur mit einem Erwachsenen.",
 special_events="Kindergeburtstage und Feiern für Erwachsene (eigene Seiten), Galerie.",
 description="Studio in München-Berg am Laim, in dem du Keramik deiner Wahl selbst bemalst. Die Malzeit beträgt 2 Stunden, es gibt eine Galerie und Feiern für Kinder und Erwachsene. Eine Reservierung wird empfohlen.")
mk(48,"dipinto-di-blu-muenchen","dipinto di blu Keramikmalstudio",MU,"BY","kontakt@dipintodiblu.de",
 pickup_time="Wenige Tage später",
 price_note="Preise stehen nicht auf der Website. Die fertige Keramik ist spülmaschinenfest, aber nicht mikrowellengeeignet.",
 special_events="Events, Gutscheine und Sortiment mit Tellern, Tassen, Schalen und Vasen. Tisch reservierst du über die Website.",
 hat_instagram=INS("dipintodiblu_keramikmalstudio"),
 description="Keramikmalstudio in München-Neuhausen. Du suchst dir ein unbemaltes Stück (Teller, Tassen, Schalen, Vasen), malst es nach deinen Ideen, und das Studio glasiert und brennt es.")
mk(49,"keramuc-muenchen","KeraMuc",MU,"BY","info@keramuc.de",
 pickup_time="Glasieren und Brennen dauern ca. 3 Tage, du kannst die Keramik selbst abholen oder abholen lassen",
 price_note="Preise stehen nicht auf der Website.",
 description="Keramik-Studio in München, in dem du dich an deinen Platz setzt, Pinsel und Farben schnappst und loslegst. Kreativ entspannen und schöne Dinge gestalten. Du reservierst einen Platz über die Website.")
mk(50,"kreativhuette-muenchen","Kreativhütte",MU,"BY",
 tags="reservation-empfohlen", price_from="16",
 studio_fee="Keine Studiogebühr · Komplettpreise (Keramik, Farben, Werkzeug, Glasur und Brand) · ca. 2,5 Stunden",
 price_note="Preise ab: Tassen, Teller und Müslischüsseln 19,50 €, Tierfiguren und Spardosen 16 €, Platten und Schalen 21,50 €, Dosen 19,50 €, Vasen 21,50 €. Es ist nur eine Auswahl der Rohlinge gezeigt, einzelne Stücke können mehr oder weniger kosten.",
 pickup_time="Eine Woche nach Abgabe der bemalten Keramik",
 special_events="Lange Nacht des Malens am ersten und dritten Donnerstag im Monat (19–22 Uhr, mit Prosecco). Malboxen für zuhause zur Vorbestellung und Gutscheine.",
 hat_instagram=INS("kreativhuette"),
 description="Studio in München, in dem du dir eine Keramik und Farben aussuchst und in entspannter Atmosphäre bemalst, mit Hilfe bei Techniken und Farbwahl. Sitzungen dauern 2,5 Stunden, keine Vorkenntnisse nötig, eine Reservierung wird empfohlen.")
mk(60,"pottery-and-painting-planegg","Pottery and Painting","Planegg","BY","sabinehaugg@potteryandpainting.com",
 tags="reservation-only, birthday-parties, hen-party, corporate-events",
 price_note="Der Preis richtet sich nach der Keramik und enthält den Brand. Alle Farben und Materialien sind im Preis enthalten, eine Anleitung zu Farben und Techniken ist inklusive. Das Sortiment umfasst rund 300 Artikel.",
 pickup_time="Nach wenigen Tagen · Abholzeiten telefonisch oder per E-Mail erfragen",
 special_events="Kindergeburtstage, Junggesellinnenabschied, Teambuilding und Babyfußabdruck auf Keramik. Silent Thursday jeden 2. Donnerstag im Monat, 17–20 Uhr. Eine Terminbuchung ist erforderlich.",
 description="Keramikmalstudio in Planegg bei München mit rund 300 Artikeln. Du nimmst dir so viele Farben, wie du möchtest, und bemalst deine Rohlinge nach deinen Vorstellungen, das Studio glasiert und brennt sie. Eine Terminbuchung ist erforderlich.")
json.dump(raw,open(p,'w'),indent=2,ensure_ascii=False); open(p,'a').write("\n")
import collections
print(len(d), sum(1 for s in d if s.get('country')=='DE'))
print(collections.Counter(s['city'] for s in d if s.get('country')=='DE').most_common())
