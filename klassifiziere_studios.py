"""
Klassifiziert Schweizer Keramik-Ateliers danach, ob sie Keramik-Bemalen
fuer Publikum anbieten oder nur Toepferkurse/Scheibendrehen.

Liest zu-pruefende-studios.csv (name, city, website, phone) und schreibt
studios-klassifiziert.csv mit zusaetzlichen Spalten "klassifikation" und
"begruendung".

Verarbeitet die Zeilen in Batches, damit der Fortschritt sichtbar bleibt.
Zwischenergebnisse werden nach jedem Batch gespeichert (resume-faehig).
"""

import asyncio
import csv
import re
import sys
from pathlib import Path

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

INPUT_CSV = Path("zu-pruefende-studios.csv")
OUTPUT_CSV = Path("studios-klassifiziert.csv")

BATCH_SIZE = 10
MAX_CONCURRENT = 5
PAGE_TIMEOUT_MS = 25_000
MAX_SUBPAGES = 4

# Linktext-Hinweise, die auf eine relevante Unterseite verweisen (Kurse/Angebot/...)
RELEVANT_LINK_HINTS = [
    "kurs", "angebot", "atelier", "workshop", "bemal", "malen", "töpfer",
    "toepfer", "keramik", "ceramic", "pottery", "programm", "service",
    "cours", "stage", "atelier", "peinture", "céramique", "prestation",
    "corso", "ceramica", "offerta", "servizi",
]

# Keywords, die auf Publikums-Bemalen hindeuten (mehrsprachig: DE/EN/FR/IT)
PAINTING_KEYWORDS = [
    "keramik bemalen", "keramik-bemalen", "keramikbemalen", "bemalatelier",
    "bemal-atelier", "rohlinge bemalen", "rohling bemalen", "tassen bemalen",
    "geschirr bemalen", "bemalstudio", "bemal studio", "selber bemalen",
    "bemalen und brennen", "bemalen & brennen",
    "pottery painting", "paint your own pottery", "paint a pot",
    "ceramic painting", "ceramics painting", "paint pottery",
    "peinture sur céramique", "peinture céramique", "peindre la céramique",
    "peindre votre céramique", "atelier peinture céramique",
    "pittura su ceramica", "dipingere la ceramica",
]

WHEEL_ONLY_KEYWORDS = [
    "töpferkurs", "toepferkurs", "töpfern lernen", "scheibendrehen",
    "drehscheibe", "drehkurs", "aufbaukeramik", "handaufbau",
    "wheel throwing", "pottery wheel", "throwing class", "hand building",
    "tournage", "tour de potier", "modelage", "cours de poterie",
    "tornio", "tornitura",
]

BROWSER_CONFIG = BrowserConfig(headless=True, verbose=False)

RUN_CONFIG = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    page_timeout=PAGE_TIMEOUT_MS,
    word_count_threshold=0,
    semaphore_count=MAX_CONCURRENT,
    verbose=False,
)


def find_keywords(text: str, keywords: list[str]) -> list[str]:
    text_low = text.lower()
    return [kw for kw in keywords if kw in text_low]


def classify(markdown_text: str) -> tuple[str, str]:
    painting_hits = find_keywords(markdown_text, PAINTING_KEYWORDS)
    wheel_hits = find_keywords(markdown_text, WHEEL_ONLY_KEYWORDS)

    if painting_hits:
        found = ", ".join(sorted(set(painting_hits))[:3])
        return "painting", f'Fundstelle(n) fuer Bemalen: "{found}"'

    if wheel_hits:
        found = ", ".join(sorted(set(wheel_hits))[:3])
        return "wheel_only", f'Nur Toepfer-Begriffe gefunden: "{found}", kein Hinweis auf Bemalen'

    return "unclear", "Weder Bemal- noch eindeutige Toepfer-Begriffe auf der Seite gefunden"


def pick_relevant_links(links: dict) -> list[str]:
    internal = links.get("internal", []) if isinstance(links, dict) else []
    seen = set()
    picked = []
    for link in internal:
        href = (link.get("href") or "").split("#")[0]
        text = (link.get("text") or "").lower()
        if not href or href in seen:
            continue
        combined = f"{href.lower()} {text}"
        if any(hint in combined for hint in RELEVANT_LINK_HINTS):
            seen.add(href)
            picked.append(href)
        if len(picked) >= MAX_SUBPAGES:
            break
    return picked


async def fetch_page_text(crawler: AsyncWebCrawler, url: str):
    try:
        result = await crawler.arun(url=url, config=RUN_CONFIG)
    except Exception:  # noqa: BLE001
        return None
    if not result.success:
        return None
    return result


async def fetch_and_classify(crawler: AsyncWebCrawler, row: dict) -> dict:
    website = (row.get("website") or "").strip()

    if not website:
        row["klassifikation"] = "unclear"
        row["begruendung"] = "Keine Website angegeben"
        return row

    result = await fetch_page_text(crawler, website)

    if result is None:
        row["klassifikation"] = "unclear"
        row["begruendung"] = "Website nicht erreichbar oder Ladefehler"
        return row

    text = result.markdown or ""
    klass, begruendung = classify(text) if text.strip() else ("unclear", "Startseite geladen, aber kein auswertbarer Text")

    if klass == "unclear":
        # Startseite ohne eindeutige Treffer -> relevante Unterseiten pruefen
        subpages = pick_relevant_links(result.links or {})
        extra_text_parts = []
        checked_pages = []
        for sub_url in subpages:
            sub_result = await fetch_page_text(crawler, sub_url)
            if sub_result is None:
                continue
            checked_pages.append(sub_url)
            sub_text = sub_result.markdown or ""
            extra_text_parts.append(sub_text)
            sub_klass, sub_begruendung = classify(sub_text)
            if sub_klass != "unclear":
                row["klassifikation"] = sub_klass
                row["begruendung"] = f"{sub_begruendung} (Unterseite: {sub_url})"
                return row

        if checked_pages:
            begruendung = (
                "Weder auf Startseite noch auf geprueften Unterseiten "
                f"({', '.join(checked_pages)}) eindeutige Bemal- oder Toepfer-Begriffe gefunden"
            )
        elif not text.strip():
            begruendung = "Startseite geladen, aber kein auswertbarer Text und keine relevanten Unterseiten gefunden"

    row["klassifikation"] = klass
    row["begruendung"] = begruendung
    return row


def load_rows() -> list[dict]:
    with INPUT_CSV.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_done_names() -> dict[str, dict]:
    if not OUTPUT_CSV.exists():
        return {}
    with OUTPUT_CSV.open(newline="", encoding="utf-8") as f:
        return {r["name"]: r for r in csv.DictReader(f)}


def save_rows(rows: list[dict]):
    fieldnames = ["name", "city", "website", "phone", "klassifikation", "begruendung"]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fieldnames})


async def main():
    all_rows = load_rows()
    done = load_done_names()

    results: list[dict] = []
    todo: list[dict] = []
    for row in all_rows:
        if row["name"] in done:
            results.append(done[row["name"]])
        else:
            todo.append(row)

    print(f"Gesamt: {len(all_rows)} Studios | bereits erledigt: {len(results)} | offen: {len(todo)}")

    if not todo:
        print("Alle Zeilen bereits klassifiziert.")
        save_rows(results)
        return

    async with AsyncWebCrawler(config=BROWSER_CONFIG) as crawler:
        total_batches = (len(todo) + BATCH_SIZE - 1) // BATCH_SIZE
        for batch_idx in range(total_batches):
            batch = todo[batch_idx * BATCH_SIZE : (batch_idx + 1) * BATCH_SIZE]
            print(f"\n=== Batch {batch_idx + 1}/{total_batches} ({len(batch)} Studios) ===")

            tasks = [fetch_and_classify(crawler, dict(row)) for row in batch]
            batch_results = await asyncio.gather(*tasks)

            for r in batch_results:
                print(f"  [{r['klassifikation']:10s}] {r['name']} ({r['city']}) - {r['begruendung']}")

            results.extend(batch_results)
            save_rows(results)
            print(f"Fortschritt gespeichert: {len(results)}/{len(all_rows)} in {OUTPUT_CSV}")

    counts = {"painting": 0, "wheel_only": 0, "unclear": 0}
    for r in results:
        counts[r["klassifikation"]] = counts.get(r["klassifikation"], 0) + 1

    print("\n=== Zusammenfassung ===")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print(f"\nFertig. Ergebnis in {OUTPUT_CSV}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAbgebrochen. Bisheriger Fortschritt wurde gespeichert und kann fortgesetzt werden.")
        sys.exit(1)
