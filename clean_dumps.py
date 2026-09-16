"""
Wandelt die rohen crawl4ai-JSON-Dumps in kompakte, lesbare Text-Dateien um:
entfernt Bilder/Base64/lange URLs, dedupliziert wiederkehrende Nav-Zeilen
zwischen Unterseiten einer Site, kuerzt auf das Wesentliche.
"""
import json
import re
from pathlib import Path

DUMP_DIR = Path("/private/tmp/claude-501/-Users-julianfrick-Desktop-keramik-directory/66778423-d814-45c6-8ec0-1bc3dbb2e937/scratchpad/studio-dumps")
CLEAN_DIR = Path("/private/tmp/claude-501/-Users-julianfrick-Desktop-keramik-directory/66778423-d814-45c6-8ec0-1bc3dbb2e937/scratchpad/studio-clean")
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

IMG_RE = re.compile(r'!\[[^\]]*\]\([^)]*\)')
LINK_RE = re.compile(r'\[([^\]]*)\]\([^)]*\)')
MULTI_BLANK_RE = re.compile(r'\n{3,}')


def clean_text(md: str) -> str:
    md = IMG_RE.sub('', md)
    md = LINK_RE.sub(r'\1', md)
    lines = [ln.rstrip() for ln in md.split('\n')]
    lines = [ln for ln in lines if ln.strip()]
    return '\n'.join(lines)


def process(json_path: Path):
    data = json.loads(json_path.read_text(encoding='utf-8'))
    out_lines = [f"# {data['name']}", f"Website: {data['website']}"]
    if data.get('error'):
        out_lines.append(f"FEHLER: {data['error']}")
    if data.get('social'):
        out_lines.append(f"Social: {data['social']}")

    seen_lines = set()
    for url, md in data.get('pages', {}).items():
        cleaned = clean_text(md)
        page_lines = []
        for ln in cleaned.split('\n'):
            key = ln.strip().lower()
            if len(key) > 15 and key in seen_lines:
                continue
            if len(key) > 15:
                seen_lines.add(key)
            page_lines.append(ln)
        page_text = '\n'.join(page_lines).strip()
        if page_text:
            out_lines.append(f"\n## Seite: {url}\n{page_text}")

    out_path = CLEAN_DIR / json_path.name.replace('.json', '.txt')
    out_path.write_text('\n'.join(out_lines), encoding='utf-8')
    return out_path, len('\n'.join(out_lines))


if __name__ == '__main__':
    total = 0
    for jp in sorted(DUMP_DIR.glob('row_*.json')):
        p, size = process(jp)
        total += size
        print(f"{p.name}: {size} Zeichen")
    print(f"\nGesamt: {total} Zeichen in {CLEAN_DIR}")
