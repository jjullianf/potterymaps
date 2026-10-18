import re, sys, json, urllib.parse
sys.path.insert(0,'.')
from check_sites import fetch, text_of
EMAIL=re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
BAD=("sentry","wixpress","example.","godaddy","schema.org","w3.org","cloudflare","googleapis","gstatic",".png",".jpg",".svg",".webp","2x@","domain.")
def emails_in(html, text):
    found=set()
    for m in re.findall(r'mailto:([^"\'?\s<>]+)',html,re.I): found.add(urllib.parse.unquote(m).strip())
    for m in EMAIL.findall(text): found.add(m)
    out=set()
    for e in found:
        e=e.strip(".,;)(").lower()
        if EMAIL.fullmatch(e) and not any(b in e for b in BAD): out.add(e)
    return out
def find(url):
    f,h=fetch(url)
    if not f: return {"error":h[:80]}
    pages={f:h}
    base=urllib.parse.urlparse(f)
    for l in re.findall(r'href=["\']([^"\'#]+)["\']',h):
        u=urllib.parse.urljoin(f,l); p=urllib.parse.urlparse(u)
        if p.netloc!=base.netloc or u in pages: continue
        if re.search(r"(impressum|kontakt|contact|datenschutz|imprint|agb)",p.path,re.I) and len(pages)<5:
            f2,h2=fetch(u,12)
            if f2: pages[f2]=h2
    res={}
    for u,hh in pages.items():
        for e in emails_in(hh,text_of(hh)): res.setdefault(e,[]).append(u)
    return res
if __name__=="__main__":
    raw=json.load(open("_raw_dump.json",encoding="utf-8"))
    C=[("KOELN",[1,2,3,5,6,8,9,10,11]),("LEIPZIG",[0,1,3,4,16])]
    out={}
    for tag,idxs in C:
        for i in idxs:
            r=raw[tag][i]; u=r["website"].split("%3F")[0].split("?")[0]
            res=find(u); out[f"{tag}:{i}"]={"name":r["name"],"site":u,"emails":res}
            print(tag,i,r["name"][:40],"->",{e:[x.split('/',3)[-1][:25] for x in s] for e,s in res.items()} if "error" not in res else res)
    json.dump(out,open("emails_C.json","w"),ensure_ascii=False,indent=1)
