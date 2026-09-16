"""
Traegt die recherchierten E-Mail-Adressen in das neue 'email'-Feld ein.
Holt den aktuellen Stand ueber die laufende Server-API (GET /api/state),
aendert AUSSCHLIESSLICH das email-Feld der betroffenen Studios und
schreibt den Stand ueber PUT /api/state zurueck (der Server legt dabei
automatisch ein Backup der vorherigen Version an).
"""
import json
import urllib.request

BASE = "http://localhost:4000"

# slug -> E-Mail (leer/None = keine gefunden, Feld bleibt unveraendert leer)
EMAILS = {
    "unique-keramik-malatelier-aarberg": "unique.keramik@icloud.com",
    "paint-it-easy-ceramics-studio-ceramic-painting-keramik-bemalen-basel": "hello@paintiteasy.ch",
    "ceramix-toepferstudio-und-pottery-painting-bern": "hello@ceramix.ch",
    "fenetre-a-l-art-keramik-bemalen-keramik-cafe-bern": "info@fenetrealart.ch",
    "fabrika-azteka-peinture-sur-ceramique-biel-bienne": "info@fabrika-azteka.ch",
    "kreativ-art-box-burgdorf": "kreativartbox@gmail.com",
    "atelier-herzton-batterkinden": "info@atelierherzton.ch",
    "selbergmalt-ch-buelach": "hoi@selbergmalt.ch",
    "maison-ceramique-cortaillod": "",
    "keramikum-ceramic-painting-studio-zwicky-duebendorf-duebendorf": "keramikum.studio@gmail.com",
    "ceramique-cafe-fribourg-fribourg": "",
    "noon-cafe-ceramique-geneva": "noon.cafeceramique@gmail.com",
    "atelier-seestern-keramik-bemalen-in-kaltbrunn-region-rapperswil-kaltbrunn": "info@atelier-seestern.ch",
    "keramikmalerei-jasmin-agner-kriens": "info@keramikmalerei.ch",
    "kreativ-pause-keramik-bemalen-laufenburg-laufenburg": "info@kreativ-pause.com",
    "hello-frances-pottery-painting-keramikmalen-lucerne": "info@hellofrances.ch",
    "siya-ceramics-i-siya-keramik-i-pottery-painting-lucerne": "siyaconceptstore@hotmail.com",
    "moon-clay-painting-studio-lucerne": "studio@moonandclay.ch",
    "valou-ceramics-montreux": "valou.ceramics@gmail.com",
    "auerhand-offenes-atelier-murgenthal": "info@auerhand.ch",
    "keramikstudio-kreativ-live-oberhofen": "info@kreativ-live.ch",
    "tom-s-tonwerk-ostermundigen": "tomstonwerk@gmail.com",
    "pinselstrich-ceramic-cafe-rueti": "",
    "two-room-club-keramikstudio-workshop-space-solothurn": "info@tworoomclub.ch",
    "spazio-keramikmalstudio-coffee-more-sursee": "mail@spazio-sursee.ch",
    "creative-you-ceramic-painting-studio-thalwil-thalwil": "info@creative-you.ch",
    "levin-art-studio-ehem-the-rainbow-club-winterthur": "info@levinartstudio.ch",
    "janella-keramikatelier-wuerenlingen": "atelier@janella.ch",
    "hello-frances-keramikmalen-paint-your-own-pottery-zofingen": "info@hellofrances.ch",
    "creative-you-ceramic-painting-studio-zug-zug": "info@creative-you.ch",
    "atelier-alfar-zuerich": "hola@atelier-alfar.com",
    "keramik-mal-cafe-zuerich": "",
    "loki-studio-zurich-oerlikon-zuerich": "hey@lokistudio.ch",
    "paint-it-easy-zuerich-creative-cafe-keramik-bemalen-zuerich": "hello@paintiteasy.ch",
    "paintlounge-paintevents-malstudio-zuerich": "info@paintevents.ch",
    "siya-ceramics-i-siya-keramik-i-pottery-painting-zuerich": "siyaconceptstore@hotmail.com",
    "ceramic-malbar-gmbh-zuerich": "info@ceramic-malbar.com",
    "bisquerie-keramik-bemalen-in-zuerich-saentisstrasse-7-8008-zuerich-zuerich": "hello@bisquerie.ch",
    "craft-room-red-fox-liestal": "redfoxliestal@gmail.com",
    "craft-room-red-fox-basel": "redfoxliestal@gmail.com",
    "ceramigas-keramik-selbst-bemalen-basel": "hello@ceramigas.ch",
    "herzart-winterthur-winterthur": "info@herzart.ch",
    "herzart-weisslingen-weisslingen": "info@herzart.ch",
    "lavendear-studio-luzern": "lavendear-studio@outlook.com",
    "teig-ton-atelier-st-gallen": "",
    "tonwerk-keramik-st-gallen": "",
}


def main():
    state = json.load(urllib.request.urlopen(f"{BASE}/api/state"))
    studios = state["studios"]

    slugs_in_state = {s["slug"] for s in studios}
    missing = set(EMAILS) - slugs_in_state
    if missing:
        print("WARNUNG: folgende slugs aus EMAILS nicht im State gefunden:", missing)

    found_count = 0
    empty_count = 0
    for s in studios:
        if s["slug"] in EMAILS:
            email = EMAILS[s["slug"]]
            s["email"] = email
            if email:
                found_count += 1
            else:
                empty_count += 1

    req = urllib.request.Request(
        f"{BASE}/api/state",
        data=json.dumps(state).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="PUT",
    )
    result = json.loads(urllib.request.urlopen(req).read())
    print("Server-Antwort:", result)
    print(f"\nE-Mail gefunden: {found_count} Studios")
    print(f"Keine E-Mail gefunden (Feld leer): {empty_count} Studios")
    print(f"Gesamt bearbeitet: {found_count + empty_count} von {len(studios)} Studios")


if __name__ == "__main__":
    main()
