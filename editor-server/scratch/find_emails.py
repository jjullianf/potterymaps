"""
Besucht fuer jedes Studio mit gesetzter Website die Startseite sowie
wahrscheinliche Kontakt-/Impressum-Unterseiten und sucht nach einer
E-Mail-Adresse (mailto:-Links, sichtbarer Text, einfache Cloudflare-
Verschleierung). Ergebnis wird als JSON-Datei pro Studio abgelegt -
keine automatische Aenderung an studios.json, das macht ein separater
Schritt nach manueller Pruefung.
"""

import asyncio
import json
import re
from pathlib import Path

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

STUDIOS_JSON = Path("/Users/julianfrick/Desktop/keramik-directory/editor-server/data/studios.json")
OUT_DIR = Path("/Users/julianfrick/Desktop/keramik-directory/editor-server/scratch/email-results")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SUBPAGE_HINTS = [
    "kontakt", "contact", "impressum", "imprint", "legal", "mentions-legales",
    "ueber-uns", "about", "faq",
]

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')
BAD_DOMAINS = (
    "sentry.io", "wixpress.com", "example.com", "godaddy.com", "schema.org",
    "w3.org", "cloudflare.com", "gstatic.com", "googleapis.com", "google.com",
    ".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".css", ".js",
)

BROWSER_CONFIG = BrowserConfig(headless=True, verbose=False)
RUN_CONFIG = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    page_timeout=25_000,
    delay_before_return_html=2.0,
    word_count_threshold=0,
    semaphore_count=5,
    verbose=False,
)


def clean_url(url: str) -> str:
    url = url.strip()
    if url and not url.startswith("http"):
        url = "https://" + url
    if "%3F" in url:
        url = url.split("%3F")[0]
    return url


def extract_emails(text: str) -> list[str]:
    found = set()
    for m in EMAIL_RE.findall(text or ""):
        low = m.lower()
        if any(bad in low for bad in BAD_DOMAINS):
            continue
        if low.startswith(("2x", "1x", "3x")):  # Wix-Bildnamen wie 2x@2x.png-Reste
            continue
        found.add(m.rstrip(".,;)"))
    return sorted(found)


def pick_subpages(links: dict, base_href: str) -> list[str]:
    internal = links.get("internal", []) if isinstance(links, dict) else []
    seen = {base_href}
    picked = []
    for link in internal:
        href = (link.get("href") or "").split("#")[0]
        text = (link.get("text") or "").lower()
        if not href or href in seen:
            continue
        combined = f"{href.lower()} {text}"
        if any(hint in combined for hint in SUBPAGE_HINTS):
            seen.add(href)
            picked.append(href)
        if len(picked) >= 4:
            break
    return picked


async def fetch_one(crawler: AsyncWebCrawler, row_idx: int, slug: str, name: str, website: str) -> dict:
    website = clean_url(website)
    data = {"row": row_idx, "slug": slug, "name": name, "website": website,
            "emails_by_page": {}, "error": None}

    try:
        home = await crawler.arun(url=website, config=RUN_CONFIG)
    except Exception as exc:  # noqa: BLE001
        data["error"] = f"Fehler beim Laden: {exc}".splitlines()[0][:300]
        return data

    if not home.success:
        data["error"] = f"nicht erreichbar: {(home.error_message or '').splitlines()[0][:300]}"
        return data

    html_raw = home.html or ""
    mailtos = re.findall(r'mailto:([^"\'?\s]+)', html_raw, re.I)
    page_emails = set(extract_emails(home.markdown or "")) | set(extract_emails(" ".join(mailtos)))
    if page_emails:
        data["emails_by_page"][website] = sorted(page_emails)

    if not page_emails:
        subpages = pick_subpages(home.links or {}, website)
        for sub_url in subpages:
            try:
                sub = await crawler.arun(url=sub_url, config=RUN_CONFIG)
            except Exception:
                continue
            if not sub.success:
                continue
            sub_html = sub.html or ""
            sub_mailtos = re.findall(r'mailto:([^"\'?\s]+)', sub_html, re.I)
            sub_emails = set(extract_emails(sub.markdown or "")) | set(extract_emails(" ".join(sub_mailtos)))
            if sub_emails:
                data["emails_by_page"][sub_url] = sorted(sub_emails)
                break

    return data


async def main():
    state = json.loads(STUDIOS_JSON.read_text(encoding="utf-8"))
    studios = state["studios"]

    rows = []
    for idx, s in enumerate(studios):
        website = (s.get("website") or "").strip()
        if website:
            rows.append((idx, s["slug"], s.get("name", ""), website))

    print(f"{len(rows)} Studios mit Website zu pruefen")

    async with AsyncWebCrawler(config=BROWSER_CONFIG) as crawler:
        batch_size = 10
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            print(f"\n=== Batch {i // batch_size + 1} ({len(batch)} Studios) ===")
            tasks = [fetch_one(crawler, idx, slug, name, website) for idx, slug, name, website in batch]
            results = await asyncio.gather(*tasks)
            for res in results:
                out_path = OUT_DIR / f"{res['slug']}.json"
                out_path.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
                if res["error"]:
                    status = f"FEHLER: {res['error']}"
                elif res["emails_by_page"]:
                    all_emails = sorted({e for lst in res["emails_by_page"].values() for e in lst})
                    status = f"gefunden: {', '.join(all_emails)}"
                else:
                    status = "keine E-Mail gefunden"
                print(f"  {res['name'][:45]:45s} | {status}")

    print(f"\nFertig. Einzelergebnisse in {OUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
