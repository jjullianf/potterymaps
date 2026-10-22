"""
Liest die (unveraenderten) Outscraper-Exporte nur lesend ein, ruft fuer jeden Betrieb in
Frage kommender Orte die Website (+ einige Unterseiten) ab und sucht Belege fuer
"Keramik selbst bemalen". Ergebnis: evidence.json (Schnipsel pro Betrieb).
"""
import json, re, ssl, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from html import unescape
from pathlib import Path

HERE = Path(__file__).parent
RAW = json.loads((HERE / "_raw_dump.json").read_text(encoding="utf-8"))
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "Mozilla/5.0 (potterymaps research)"}

POS = re.compile(
    r"(selbst(?:ständig|staendig)?\s+bemal|bemal(?:en|st|t)\b|rohling|keramikmal|keramik\s+mal|mal-?\s?caf|"
    r"paint\s+your|pottery\s+painting|mal-?atelier|malstudio|mal-?workshop|farbe\s+aussuch|glasier)",
    re.I,
)
NEG = re.compile(r"(drehscheibe|aufbaukeramik|töpferkurs|toepferkurs|töpfern\b|kurs(?:e)?\b|verkauf|shop\b)", re.I)
SUBHINT = re.compile(r"(bemal|mal|keramik|workshop|angebot|kurs|preis|kontakt|impressum|ueber|über|about|studio|cafe|café|pottery)", re.I)


def fetch(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            raw = r.read(600_000)
            ct = r.headers.get_content_charset() or "utf-8"
            return r.geturl(), raw.decode(ct, errors="ignore")
    except Exception as e:  # noqa: BLE001
        return None, f"ERR {type(e).__name__}: {e}"


def text_of(html):
    html = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
    html = re.sub(r"(?s)<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", unescape(html))


def snippets(text, rx, n=5, width=90):
    out, last = [], -1000
    for m in rx.finditer(text):
        if m.start() - last < 200:
            continue
        last = m.start()
        out.append(text[max(0, m.start() - width): m.end() + width].strip())
        if len(out) >= n:
            break
    return out


def check(rec):
    url = rec.get("website")
    if not url or url == "None":
        return {"error": "keine Website in den Daten"}
    url = url.split("?")[0] if "utm_" in url else url
    final, html = fetch(url)
    if final is None:
        return {"error": html, "url": url}
    pages = {final: text_of(html)}
    links = re.findall(r'href=["\']([^"\'#]+)["\']', html)
    base = urllib.parse.urlparse(final)
    seen = {final}
    for l in links:
        u = urllib.parse.urljoin(final, l)
        p = urllib.parse.urlparse(u)
        if p.netloc != base.netloc or u in seen or re.search(r"\.(jpg|png|pdf|css|js|jpeg|webp|svg)$", p.path, re.I):
            continue
        if SUBHINT.search(p.path) and len(pages) < 6:
            seen.add(u)
            f2, h2 = fetch(u, 12)
            if f2:
                pages[f2] = text_of(h2)
    alltext = " ".join(pages.values())
    home = pages[final]
    counts = {w: len(re.findall(w, alltext, re.I)) for w in ["bemal", "rohling", "töpfer|toepfer", "drehscheibe", "kurs", "verkauf|shop|kaufen", "galerie", "leipzig", "malen|mal-"]}
    return {
        "excerpt": home[:700],
        "counts": counts,
        "all_urls": list(pages),
        "url": final,
        "pages": list(pages),
        "pos": snippets(alltext, POS, 6),
        "neg": snippets(alltext, NEG, 3, 60),
        "title": (re.search(r"(?is)<title>(.*?)</title>", html) or [None, ""])[1].strip()[:120],
        "emails": sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", alltext + " " + html)))[:6],
    }


def main():
    jobs = []
    for tag, recs in RAW.items():
        for i, r in enumerate(recs):
            if r.get("name") in (None, "None"):
                continue
            jobs.append((tag, i, r))
    with ThreadPoolExecutor(8) as ex:
        results = list(ex.map(lambda j: check(j[2]), jobs))
    out = {f"{t}:{i}": {"name": r["name"], **res} for (t, i, r), res in zip(jobs, results)}
    (HERE / "evidence.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("fertig", len(out))


if __name__ == "__main__":
    main()
