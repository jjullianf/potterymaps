import json,sys,io,contextlib,re
sys.path.insert(0,'editor-server/scratch/outscraper-de3')
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_report3 as b
hours_de=b.hours_de
RAW=json.load(open('editor-server/scratch/outscraper-de10/_raw_dump.json',encoding='utf-8'))['N']
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
BW,BY,NI,SH,MV,SN,BB,RP,SL,BE="BW","BY","NI","SH","MV","SN","BB","RP","SL","BE"
mk(2,"ton4you-offenburg","TON4YOU","Offenburg",BW,addr="Ortenaustraße 48, 77656 Offenburg",hours="",
 tags="reservation-only, hen-party",
 price_note="Preise stehen nicht auf der Website. Du wählst ein handgefertigtes Keramikstück aus und bemalst es. Termine stehen unter «freie Kurstermine».",
 special_events="Junggesellinnenabschiede und kleine Teamevents.",
 hat_instagram=INS("ton4youoffenburg"),
 description="Keramikwerkstatt in Offenburg-Elgersweier, in der du ein handgefertigtes Keramikstück auswählst und selbst bemalst. Neben Töpferkursen gibt es Angebote für JGA und kleine Teamevents.")
mk(4,"keramik-malstudio-ohneisser-offenburg","Keramik Malstudio Ohneisser","Offenburg",BW,addr="Okenstraße 326A, 77652 Offenburg",hours="Termine nach Vereinbarung",
 tags="reservation-only, hen-party",price_from="15",
 studio_fee="Gruppen: 100 € für 4 Personen, ab der 5. Person je 20 € zusätzlich · ca. 2,5 Stunden",
 price_note="Rohlinge kosten ab 15 € (Müslischale, Tasse, Teller), Schüssel ab 18 €, Krug und Kuchenplatte ab 25 €. Termine werden über das Kontaktformular mit Wunsch- und Alternativtermin vereinbart.",
 pickup_time="Nach ca. 3–6 Tagen",
 special_events="Keramik-Bemal-Workshops für Gruppen, zum Beispiel Junggesellenabschiede und Geburtstage.",
 description="Keramik Malstudio im Offenburger Ortsteil Bohlsbach, angebunden an einen Keramikbedarf. Du bemalst in etwa 2,5 Stunden einen Rohling, Termine vereinbarst du über das Kontaktformular.")
mk(5,"herzenston-keramikmalstudio-ohlsbach","Herzenston Keramikmalstudio & Geschenke","Ohlsbach",BW,
 tags="reservation-only, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Keramikmalen ist nur mit Terminvereinbarung möglich.",
 special_events="Geburtstagsfeiern, Firmenevents, Junggesellinnenabschiede und Mädelsabende.",
 description="Keramikmalstudio mit Geschenkladen in Ohlsbach bei Offenburg. Du bemalst Keramik nach Terminvereinbarung, auch für Geburtstage, JGA und Firmenevents.")
mk(20,"tuscherei-schwerin","Tuscherei","Schwerin",MV,"kontakt@tuscherei.de",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Das Keramikbemalen ist nach Angabe der Website das Herzstück. Reservierung über einen Link.",
 special_events="Workshops mit Ton und Farbe, Babybauchschalen und MondayClayClub.",
 description="Keramikbemalstudio in Schwerin. Das Keramikbemalen ist das Herzstück des Ateliers, daneben gibt es Workshops mit Ton und Farbe sowie Babybauchschalen.")
mk(29,"mal-mal-cottbus","mal mal","Cottbus",BB,"hallo@malmal-cottbus.de",
 hours="Mo geschlossen, Di–Fr 14–19 Uhr, Sa 11:30–19 Uhr, So gelegentlich eine Malzeit",
 tags="reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",
 studio_fee="Ca. 2 Stunden Malzeit",
 price_note="Preise stehen nicht auf der Website. Reservierung über die Website wird empfohlen.",
 pickup_time="Ein paar Tage nach dem Bemalen",
 special_events="Kidsparty, Teamevents, JGA und Weihnachtsfeiern.",
 hat_instagram=INS("malmal_cottbus"),
 description="Keramikmalstudio in Cottbus. Du hast etwa 2 Stunden, um deinen Rohling zu bemalen, und holst ihn ein paar Tage später gebrannt ab. Reservieren geht über die Website.")
mk(38,"farbton-keramikmalstudio-wolfsburg","FarbTon Keramikmalstudio","Wolfsburg",NI,"info@farbton-studio.de",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Termine buchst du online.",
 special_events="Geburtstage und andere Veranstaltungen, das Angebot wird gemeinsam zusammengestellt.",
 hat_instagram=INS("farbton.keramik"),
 description="Keramikmalstudio in Wolfsburg, in dem du Keramik selbst bemalst. Termine buchst du online, für Geburtstage und andere Feiern wird ein Angebot abgesprochen.")
mk(39,"die-pinselei-wolfsburg","Die Pinselei","Wolfsburg",NI,
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Du buchst deine kreative Auszeit online und wirst per E-Mail benachrichtigt, sobald dein Stück fertig ist.",
 special_events="Gruppen-Angebote (Details auf der Website).",
 description="Keramik-Malstudio in Wolfsburg. Du buchst online eine kreative Auszeit und bekommst eine E-Mail, sobald dein bemaltes Stück fertig ist.")
mk(50,"shinkeramik-birkenfeld","shinkeramik","Birkenfeld",BW,
 price_note="Preise und Ablauf des Bemalens stehen nicht auf der Startseite. Die Website führt eine Kategorie «Keramik bemalen».",
 hat_instagram=INS("shin_keramik"),
 description="Keramikatelier in Birkenfeld bei Pforzheim mit Töpferkursen und der Möglichkeit, Tassen und Keramik zu bemalen.")
mk(51,"porzellinchen-oeschelbronn","Porzellinchen","Niefern-Öschelbronn",BW,"info@porzellinchen.de",
 tags="reservation-only, kids-friendly, birthday-parties",
 price_note="Preise stehen nicht auf der Website. Freie Termine buchst du über ein Buchungstool.",
 hat_instagram=INS("porzellinchen86"),
 description="Keramikmalstudio in Niefern-Öschelbronn bei Pforzheim. Freie Termine buchst du online, es gibt auch Kindergeburtstage.")
mk(52,"luenekeramik-lueneburg","LüneKeramik","Lüneburg",NI,"malen@luenekeramik.de",
 tags="reservation-only",price_from="9",
 studio_fee="Ca. 2 Stunden",
 price_note="Rohlinge kosten 9–59 €, beliebte Teile wie Tassen, Schälchen und kleine Teller 20–25 € inklusive Material und Brennvorgängen. Termine buchst du online.",
 pickup_time="Meist am nächsten Öffnungstag ab 18 Uhr",
 special_events="Angebote für Gruppen und Events (Details auf der Website).",
 hat_instagram=INS("luene_keramik_"),
 description="Keramikmalstudio in Lüneburg, in dem du in etwa zwei Stunden einen Rohling bemalst. Material und Brand sind im Preis enthalten, Termine buchst du online.")
mk(53,"porzellanperle-lueneburg","Porzellanperle","Lüneburg",NI,"info@porzellanperle.de",
 tags="reservation-only, hen-party, corporate-events",
 price_note="Preise stehen auf der Seite «Fragen & Antworten». Online-Buchung möglich.",
 pickup_time="Nach ca. 1–2 Wochen",
 special_events="Junggesellenabschiede, Firmenfeiern und Teambuilding.",
 hat_instagram=INS("porzellanperle"),
 description="Keramik selbst bemalen in Lüneburg. Termine buchst du online, nach ein bis zwei Wochen ist dein Stück gebrannt. Es gibt Angebote für JGA und Teambuilding.")
mk(55,"maly-kreativzeit-ravensburg","Maly Kreativzeit","Ravensburg",BW,"info@maly-kreativzeit.de",hours="",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Plätze buchst du über «Platz buchen».",
 special_events="Kindergeburtstage, Junggesellenabschiede, Firmenevents, Geburtstage und Babyshower, auch außerhalb der regulären Öffnungszeiten.",
 description="Keramikmalstudio in Ravensburg. Du buchst online einen Platz, für Kindergeburtstage, JGA, Firmenevents und Babyshower gibt es eigene Termine.")
mk(56,"punkt-und-strich-ravensburg","Punkt und Strich Keramik Malstudio","Ravensburg",BW,"hallo@punktundstrich.studio",
 hours="Mo, Di, So geschlossen, Mi, Do 17–19:30 Uhr, Fr 15–17:30 und 18:30–21 Uhr, Sa 12–14:30 und 15:30–18 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Website. Bei Events sind Material, Glasur und Brennen immer inklusive. Spontane Besuche ohne Slot werden nicht angenommen.",
 pickup_time="Nach rund 1–2 Wochen, das Studio meldet sich",
 special_events="Kindergeburtstag, JGA, Geburtstag für Erwachsene, Team-Event sowie Schul- und Kita-Ausflüge.",
 hat_instagram=INS("punktundstrich_ravensburg"),
 description="Keramik Malstudio in Ravensburg mit festen Zeitfenstern, die du vorab reservierst. Spontane Besuche ohne Slot sind nicht möglich. Es gibt eigene Angebote für Kindergeburtstag, JGA und Team-Events.")
mk(57,"marie-kunst-und-keramik-ravensburg","MARIE Kunst und Keramik","Ravensburg",BW,hours="",
 price_note="Preise stehen nicht auf der Startseite. Der Seitentitel nennt Keramik bemalen und Kunstkurse.",
 description="Atelier in Ravensburg mit Keramik bemalen und Kunstkursen.")
mk(60,"erb-stuecke-ravensburg","ERB-STÜCKE","Ravensburg",BW,"erb-stuecke@email.de",hours="",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Plätze und Wunschtermine fragst du per E-Mail an, die aktuellen Bemal-Termine stehen auf der Website.",
 description="Keramikatelier in Ravensburg mit Terminen zum Keramik bemalen. Plätze fragst du tagesaktuell per E-Mail an.")
mk(62,"keramikmalstube-goerlitz","Keramikmalstube","Görlitz",SN,hours="",
 price_note="Preise stehen nicht auf der Website. Es gibt einen Malnachmittag, bei dem du dein Lieblingsstück selbst bemalst.",
 special_events="Malnachmittag zum Selbstbemalen.",
 description="Keramikmalstube in Görlitz mit einem Malnachmittag, bei dem du dein Lieblingsstück selbst bemalst.")
mk(83,"junik-keramikstudio-baden-baden","JUNIK Keramikstudio","Baden-Baden",BW,
 hours="Mo, Di geschlossen, Mi, Do 12–20 Uhr, Fr 14–22 Uhr, Sa 12–20 Uhr, So 10–16 Uhr",
 tags="reservation-only, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Startseite. Das Studio ist klimatisiert und barrierefrei, mit ebenerdigem Zugang und behindertengerechter Toilette. Eine Stunde früher wird geschlossen, wenn niemand mehr im Malstudio ist.",
 pickup_time="Abholung Mi, Do, Sa 12–19 Uhr, Fr 14–21 Uhr",
 special_events="Junggesellenabschiede, Firmenfeiern und Geburtstage.",
 description="Keramikstudio in Baden-Baden, in dem du aus vielen Rohkeramiken auswählst und selbst bemalst. Plätze reservierst du online, das Studio ist klimatisiert und barrierefrei.")
mk(36,"madame-kunterbunt-friedrichshafen","Madame Kunterbunt","Friedrichshafen",BW,
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Startseite. Kaffee- und Teespezialitäten gibt es vor Ort.",
 special_events="Gruppen- und Firmenevents, Junggesellinnenabschied, Kindergeburtstag sowie Kita- und Schulausflüge.",
 description="Keramikmalstudio mit Café in Friedrichshafen für Anfänger und Fortgeschrittene. Es gibt Kaffee und Tee, dazu eigene Angebote für Gruppen, JGA, Kindergeburtstage und Schulausflüge.")
mk(7,"kritzelei-flensburg","Kritzelei","Flensburg",SH,addr="Große Straße 56, 24937 Flensburg",
 hours="Mo 13–19 Uhr (in den Ferien 10–19 Uhr), Di 10–19 Uhr, Mi–Sa 10–22 Uhr, So 10–19 Uhr",
 tags="reservation-empfohlen, birthday-parties",
 price_note="Preise stehen auf der Unterseite «Preise». Du reservierst deinen Malplatz im Voraus. Mittwoch bis Samstag gibt es den «Langen Malabend» bis 22 Uhr mit einem Glas Sekt.",
 pickup_time="Meist 10–14 Tage, in der Saison länger · fertige Keramik wird 3 Monate aufbewahrt · Versand gegen Aufpreis",
 special_events="Malangebote für Gruppen, Langer Malabend, Keramik2Go, Gutscheine sowie die Clay Station nebenan für Töpferkurse.",
 description="Keramikmalstudio in zentraler Lage in der Flensburger Großen Straße. Für Neue gibt es eine Einführung, nach 10 bis 14 Tagen ist dein Stück gebrannt. An langen Malabenden ist bis 22 Uhr geöffnet.")
mk(89,"mahlzeit-keramikstudio-weyhausen","Mahlzeit Keramikstudio","Weyhausen",NI,hours="",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Startseite. Das Keramikstudio gehört zu einem Hotel mit Restaurant. In den Herbstferien ist täglich um 9:30 und um 17 Uhr geöffnet. Das Keramikfrühstück mit Buffet kostet 19,90 € pro Person und findet einmal im Monat statt.",
 special_events="Kindergeburtstag, Junggesellenabschied, Gruppenbuchung, Babyfußabdrücke, Schulen und Kitas, Workshops und das Keramikfrühstück.",
 description="Keramikstudio im Hotel Mahlzeit in Weyhausen bei Wolfsburg und Gifhorn. Du buchst online einen Malplatz. Einmal im Monat gibt es das Keramikfrühstück mit Buffet.")
mk(99,"nami-keramikatelier-nuernberg","nãmi Keramikatelier","Nürnberg",BY,"info@nami-keramik.de",hours="Nur am Wochenende, genaue Zeiten nach Buchungskalender",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party",price_from="10",
 studio_fee="Keine Zusatzgebühr bei regulären Malsessions · 2 Stunden, danach bis zu 30 Minuten Verlängerung · bei Special-Events Eventpauschale",
 price_note="Kleine Schalen kosten etwa 10 €, große Platten und Schüsseln bis 60 €, Teller und Tassen 25–30 €. Farben, Glasur und Brand sind enthalten. Reservierung wird besonders am Wochenende empfohlen, spontan geht es bei freien Plätzen.",
 pickup_time="Nach ca. 25 Tagen",
 special_events="Malsessions, Events und Workshops sowie private Feiern wie Geburtstag, JGA und Babyshower.",
 description="Keramikatelier in Nürnberg mit Malsessions am Wochenende. Farben, Glasur und Brand sind im Preis enthalten. Reservieren wird empfohlen, spontan geht es bei freien Plätzen.")
mk(100,"atelier-pipoka-erlangen","Atelier pipoka","Erlangen",BY,hours="",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Startseite. Du wählst weiße Keramikrohlinge, Farben, Pinsel, Stempel und Schablonen stehen bereit. Eine Reservierung ist erforderlich.",
 pickup_time="Ca. 2 Wochen nach dem Malen · bei Kit-Kasa zum Mitnehmen am nächsten Tag",
 special_events="Kit-Kasa-Angebot zum Bemalen zu Hause.",
 hat_instagram=INS("atelier_pipoka"),
 description="Keramikatelier in Erlangen. Du wählst einen weißen Rohling und gestaltest ihn mit Farben, Stempeln und Schablonen. Eine Reservierung ist nötig, nach etwa 2 Wochen ist dein Stück fertig.")
mk(104,"zino-keramik-wuerzburg","Zino Keramik","Würzburg",BY,"info@zinokeramik.de",hours="",
 tags="reservation-only",
 price_note="Preise stehen nicht auf der Website. Du buchst deinen Platz über die Buchungsseite.",
 hat_instagram=INS("zinokeramik.studio"),
 description="Keramikstudio in der Würzburger Altstadt, in dem du Keramik bemalst. Deinen Platz buchst du online.")
mk(105,"tonart-kreativraum-wuerzburg","TonArt Kreativraum","Würzburg",BY,"info@tonart-wue.de",hours="",
 tags="reservation-only, corporate-events",
 price_note="Preise stehen nicht auf der Website. Termine vereinbarst du vorab per E-Mail oder Telefon.",
 special_events="Einzeldrehstunden, Gruppenevents und eine mobile Werkstatt.",
 description="Kreativraum in der Würzburger Altstadt, in dem du nach Terminabsprache Keramik bemalen oder an der Drehscheibe arbeiten kannst.")
mk(107,"werkxsalon-ingolstadt","werkxsalon Ingolstadt","Ingolstadt",BY,"ingolstadt@werkxsalon.de",
 hours="Mo 14–18 Uhr, Do 14–16:30 und 18–20:30 Uhr, Fr 11–13:30 und 14:30–17 Uhr, Sa 10–12:30 und 13:30–16 Uhr, Di, Mi, So geschlossen",
 tags="reservation-only, kids-friendly, birthday-parties",
 price_note="Preise stehen nicht auf der Website. Reserviert wird über die Reservierungsseite. Das Studio hat einen weiteren Standort in Starnberg.",
 pickup_time="Nach ca. 5–6 Tagen",
 special_events="Einzel- und Gruppentermine, Feiern und Geburtstage sowie Kindergeburtstage.",
 description="Keramikstudio in der Ingolstädter Altstadt. Du reservierst online einen Termin, nach etwa 5 bis 6 Tagen ist dein Stück glasiert und gebrannt.")
mk(108,"keramik-bemalen-landshut","Keramik bemalen Landshut","Landshut",BY,
 hours="Mo geschlossen, Di–Fr 12–19 Uhr, Sa 10–19 Uhr",
 tags="reservation-empfohlen, kids-friendly, birthday-parties",
 price_note="Preise stehen nicht auf der Website. Eine Malplatz-Reservierung wird immer empfohlen. Spontan frei gewordene Termine stehen auf Instagram und Facebook.",
 pickup_time="Etwa 1 Woche (laut Gästebewertung, nicht offiziell angegeben)",
 special_events="Kindergeburtstage und Keramik zum Mitnehmen (Malprojekt außerhalb des Studios).",
 hat_instagram=INS("keramik.bemalen.landshut"),
 description="Keramikmalstudio in der Landshuter Altstadt. Eine Reservierung wird empfohlen, spontan frei werdende Termine stehen auf Instagram. Keramik zum Mitnehmen gibt es auch.")
mk(113,"oclay-passau","Oclay","Passau",BY,"info@oclay.de",hours="",
 price_note="Preise stehen nicht auf der Startseite. Die Kurse sind unter «Kurse» gelistet.",
 special_events="Kreativ-Workshops mit Töpfern an der Drehscheibe, freiem Modellieren und Keramik bemalen für Einzelpersonen, private Gruppen und Teambuilding.",
 hat_instagram=INS("oclay_simply_original"),
 description="Kreativstudio in der Passauer Altstadt mit Workshops, in denen du an der Drehscheibe töpferst, frei modellierst oder Keramik bemalst.")
mk(116,"malmal-trier","malmal Trier","Trier",RP,
 hours="Mo, So geschlossen, Di, Do–Sa 11–18:30 Uhr, Mi 13:30–21 Uhr",
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="8",
 studio_fee="Feste Zeitfenster: 11–13:15, 13:30–15:45 und 16–18:30 Uhr",
 price_note="Keramik kostet 8 € (Eierbecher) bis 47 € (große Schale), Rohkeramik, Farben, Hilfsmittel, transparente Glasur und Brand sind inklusive. Spontan geht es, die Website empfiehlt aber immer zu reservieren.",
 pickup_time="Nach ca. 4 Werktagen",
 special_events="Geburtstagsfeiern, Privat- und Firmenevents, Schulausflüge, Junggesellenabschiede, Babyfußabdrücke und Erinnerungsteller.",
 hat_instagram=INS("malmal_trier"),
 description="Keramikmalstudio in der Trierer Innenstadt mit festen Zeitfenstern. Der Preis enthält Rohkeramik, Farben, Glasur und Brand, nach etwa 4 Werktagen ist dein Stück fertig. Reservieren wird empfohlen.")
mk(117,"cuplenz-koblenz","CupLENZ","Koblenz",RP,"info@cuplenz.de",
 hours="Mo geschlossen, Di, Mi 13:30 und 16:15 Uhr, Do 10:30, 13:30 und 16:15 Uhr, Fr 13:30, 16:15 und 18:45 Uhr, Sa 11, 13:30 und 16:15 Uhr, So 11 und 13:30 Uhr",
 tags="reservation-only",
 studio_fee="Begleitpersonen ohne Malen zahlen 20 € Platzgebühr · ca. 2 Stunden pro Malzeit",
 price_note="Preise stehen nicht auf der Startseite. Jeder reservierte Platz ist ein Malplatz. Die Zeiten sind Startzeiten der Sessions, sei 10 Minuten vorher da.",
 pickup_time="Nach einigen Tagen",
 special_events="Individuelle Anfragen über das Kontaktformular und eine Malkiste für unterwegs.",
 description="Keramikbemalbar in der Koblenzer Altstadt. Du reservierst einen Malplatz für etwa 2 Stunden, wählst deinen Rohling und das Studio glasiert und brennt ihn.")
mk(119,"laedjen-kunst-und-keramik-koblenz","LÄDJEN Kunst & Keramik by blumenkindjen","Koblenz",RP,
 hours="Mo geschlossen, Di–Sa 10–18 Uhr",
 tags="reservation-only",
 price_note="Open Pottery Painting im LÄDJEN kostet 15 €. Dazu gibt es Specials wie Second Chance Paint (30 €), Sprizz & Paint (20 €), Matcha & Paint (50 €) und Cake & Paint (70 €). Gebucht wird über die Website.",
 special_events="Open Pottery Painting und Specials wie Sprizz & Paint, Matcha & Paint und Cake & Paint.",
 hat_instagram=INS("blumenkindjen.art"),
 description="Laden und Studio für Kunst und Keramik in der Koblenzer Altstadt. Beim Open Pottery Painting bemalst du Keramik, dazu gibt es Specials mit Sprizz, Matcha oder Kuchen.")
mk(125,"loveelin-art-lahnstein","LOVEELIN ART","Lahnstein",RP,"info@loveelinart.de",hours="",
 tags="reservation-only",
 price_note="Pro Person reservierst du einen Sitzplatz und zahlst nur die Keramik. Pottery Painting ist als offener und privater Workshop gelistet.",
 special_events="Pottery Painting als offener und privater Workshop.",
 description="Atelier in Lahnstein bei Koblenz mit Pottery-Painting-Workshops. Pro Person reservierst du einen Sitzplatz und zahlst nur die Keramik.")
mk(134,"malbar-saarbruecken","Malbar Saarbrücken","Saarbrücken",SL,"info@malbar-saarbruecken.de",
 hours="Mo geschlossen, Di, Mi 12–19 Uhr, Do, Fr 12–21 Uhr, Sa 10:30–20:30 Uhr, So 10:30–17 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party",
 price_note="Preise stehen nicht auf der Website. Reserviert wird online. Es gibt einen zweiten Standort in der Cecilienstraße mit leicht anderen Zeiten.",
 special_events="JGA, Kindergeburtstag, Schulausflug und Gruppenevents. Weihnachtsartikel können je nach Standort vor Ort bis 16.12. bemalt werden.",
 hat_instagram=INS("malbar_saarbruecken"),
 description="Keramikmalstudio in der Saarbrücker Nauwieserstraße mit zweitem Standort in der Cecilienstraße. Plätze reservierst du online, auch für JGA, Kindergeburtstage und Gruppenevents.")
mk(138,"mal-mal-kueche-ruhpolding","Mal mal Küche","Ruhpolding",BY,"malmalkueche@funwerk-chiemgau.de",
 hours="Mo 14–19 Uhr, Di, Mi 10–18 Uhr, Do 10–14 Uhr, Fr 14–21 Uhr, Sa 14–18 Uhr (13.10. bis 08.11.2026), ab 09.11. nur Fr 14–21 und Sa 14–18 Uhr",
 tags="walk-in, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="5",
 studio_fee="Keine Zusatzgebühr · so viel Zeit, wie du magst",
 price_note="Tassen und Becher ab 15 €, Teller ab 14 €, Schalen ab 17 €, Küchenkram ab 12 €, Kinderkram und Figuren ab 5 €, alles inklusive Farben, Hilfsmittel, Glasur und Brand. Spontanbesuch während der Öffnungszeiten ist möglich. Eine Stunde vor Ladenschluss schließt das Geschäft, wenn niemand mehr malt.",
 pickup_time="Nach 2–4 Werktagen · Versand per Post für Urlaubsgäste möglich",
 special_events="Feiern wie Geburtstag, JGA und Firmenfeier, Kindergeburtstag ab Klasse 2 in der Mal mal Küche oder zu Hause mit Geburtstagsbox, Unterschriftenteller und Mal-Boxen für zuhause.",
 hat_instagram=INS("by_funwerk_chiemgau"),
 description="Keramikmalstudio in Ruhpolding im Chiemgau. Du kannst spontan vorbeikommen und hast so viel Zeit, wie du magst. Urlaubsgäste können sich ihre fertige Keramik zuschicken lassen.")
mk(137,"tausendschoene-lieblingsstuecke-rosenheim","Tausendschöne Lieblingsstücke","Rosenheim",BY,addr="Innstraße 12, 83022 Rosenheim",
 hours="Mo, Di geschlossen, Mi, Do 14:30–20 Uhr, Fr 10–13 und 14:30–18 Uhr, Sa 9:30–19:30 Uhr, So 10:30–13:30 und 14:30–18 Uhr",
 tags="reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",
 studio_fee="Mindestumsatz 20 € pro Gast, auch für Nicht-Maler · Kinder unter 9 Jahren: Mi und Do eine Begleitperson frei",
 price_note="Einzelpreise stehen nicht auf der Startseite. Lange Nächte freitags 19–22 Uhr ab November bis Januar, Teilnahme ab 15 Jahren. Termine werden online gebucht.",
 special_events="Kindergeburtstage ab 8 Jahren (max. 6 Kinder, Mi–Fr nachmittags), Junggesellinnenabschied, Firmenfeiern, Feiern mit Freunden, Gruppen ab 15 Personen nach Absprache und Keramikmalen to go mit Party- oder Mini-Malbox.",
 description="Keramikmalstudio in Rosenheim. Pro Gast gilt ein Mindestumsatz von 20 €, Termine buchst du online. Neben dem Studio gibt es Keramikmalen to go mit Party- und Mini-Malbox.")
mk(142,"la-fabrique-regensburg","La Fabrique","Regensburg",BY,"lafabrique@gmx.de",
 hours="Kernzeiten Do–So 12–15 Uhr, Maltermine Do 16 und 19 Uhr, Fr 13 und 16 Uhr, Sa 10, 13 und 16 Uhr, So 10 und 13 Uhr",
 tags="reservation-only, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Ein Besuch kostet im Schnitt 25–35 € je nach Rohling. Der Besuch ist nur mit Reservierung per E-Mail oder Telefon möglich.",
 pickup_time="Nach ca. 2–3 Wochen",
 special_events="Kindergeburtstage, Sondergruppen, Teambuilding, Firmenfeier, Betriebsausflug, Weihnachtsfeier, Junggesellenabschied, Kommunions- oder Firmungsfeier, Seniorentreffen und Stammtisch der Farblustigen.",
 hat_instagram=INS("la_fabrique_regensburg"),
 description="Keramikmalstudio in Regensburg mit festen Maltermine zwischen Donnerstag und Sonntag. Du reservierst per E-Mail oder Telefon, nach 2 bis 3 Wochen ist dein Stück glasiert und gebrannt.")
mk(145,"hantwerck-regensburg","hantwerck","Regensburg",BY,hours="",
 price_note="Preise stehen nicht auf der Startseite. Die Website nennt Keramik zuhause bemalen sowie die Kurse «Keramik bemalen 1» und «Keramik bemalen 2».",
 special_events="Kurse Keramik bemalen 1 und 2, Keramik zuhause bemalen.",
 hat_instagram=INS("hantwerck.keramik"),
 description="Keramikatelier in der Regensburger Altstadt mit Kursen zum Keramik bemalen und der Möglichkeit, Keramik zuhause zu bemalen.")
mk(149,"paint-me-bayreuth","Paint me","Bayreuth",BY,
 tags="walk-in, reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",
 price_note="Preise stehen nicht auf der Startseite. Ein Termin wird empfohlen, spontan vorbeikommen geht ebenfalls. Es gibt eine kurze Einführung.",
 special_events="Kindergeburtstage (auch Teenie- und Erwachsenengeburtstage), JGA, Teamevents, Gutscheine und Workshop-Abende zu besonderen Themen.",
 description="Keramikmalstudio am Kirchplatz in Bayreuth. Du kannst einen Termin buchen oder spontan vorbeikommen. Es gibt eine kurze Einführung sowie Angebote für Geburtstage, JGA und Teamevents.")
mk(159,"kunstcafe-erlangen","Kunstcafé","Erlangen",BY,
 hours="Mo, Di geschlossen, Mi, Sa 10–18 Uhr, Do, Fr 10–20 Uhr, So 14–17 Uhr",
 tags="walk-in, reservation-empfohlen",
 studio_fee="Mindestens 2 Stunden einplanen, bis zu 3 Stunden zum Gestalten",
 price_note="Preise stehen nicht auf der Website, das Brennen ist im Preis der Rohkeramik enthalten. Man kann immer vorbeikommen, in Stoßzeiten wird reserviert. Kreativworkshops nur nach Voranmeldung.",
 pickup_time="Nach etwa 2 Wochen",
 description="Kunstcafé in Erlangen, in dem du Keramik bemalst. Spontan vorbeikommen ist immer möglich, in Stoßzeiten wird eine Reservierung empfohlen. Donnerstag und Freitag ist bis 20 Uhr geöffnet.")
mk(164,"color-me-keramikmalstudio-bamberg","Color me Keramikmalstudio","Bamberg",BY,
 hours="Abholung fertiger Keramik: Mo 10–12 und 17:30–19:30 Uhr, Mi, Do, Fr 17:30–19:30 Uhr, Sa 11–13 Uhr, Di Ruhetag. Die Malplatz-Uhrzeiten unterscheiden sich davon.",
 tags="reservation-empfohlen, kids-friendly, birthday-parties, hen-party, corporate-events",price_from="10",
 studio_fee="Studiogebühr plus Keramikpreis · Platz für 2 Stunden reserviert · Stornierung bis 48 Stunden vorher kostenlos",
 price_note="Tassen, Teller und Müslischalen ab 10 €, Salatschalen und Teekannen ab 25 €. Die Betrag der Studiogebühr steht auf der Seite «Malkurse und Preise».",
 pickup_time="14 Tage nach dem Maltermin, du bekommst eine E-Mail bei Buchung über die Plattform",
 special_events="Geburtstagsfeier, Firmenfeier, JGA und Babyshower. Zusätzlich «Malen am Vormittag» jeden zweiten Donnerstag 10–12 Uhr, Keramik zu Hause bemalen per Online-Shop mit Click & Collect.",
 description="Keramikmalstudio in Bamberg seit 2019. Du reservierst einen Malplatz für 2 Stunden, die fertige Keramik kannst du nach 14 Tagen abholen. Es gibt keine Töpferkurse.")
mk(26,"crazypaint-keramik-und-cafe-berlin","crazypaint Keramik und Café","Berlin",BE,hours="",
 tags="reservation-empfohlen",
 price_note="Preise und Öffnungszeiten stehen auf eigenen Unterseiten. Vor allem am Wochenende, in den Ferien und vor Feiertagen wird es schnell voll. Für größere Gruppen oder Feiern per E-Mail oder Telefon Kontakt aufnehmen.",
 special_events="Veranstaltungen und Kurse, Details auf der Website.",
 description="Keramik und Café in Berlin-Treptow-Köpenick, in dem du Keramik bemalst. Am Wochenende und in den Ferien wird eine Reservierung empfohlen.")
json.dump(raw,open(p,'w'),ensure_ascii=False,indent=2)
print(len(d))
