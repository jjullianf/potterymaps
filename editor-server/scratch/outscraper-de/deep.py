import re, sys, urllib.parse
sys.path.insert(0,'.')
from check_sites import fetch, text_of
def pages(url, maxp=8, hint=r"(bemal|mal|keramik|ceramic|workshop|angebot|kurs|preis|about|ueber|über|offene|werkstatt|studio|shop|termine|event)"):
    f,h=fetch(url)
    if not f: return {}, h
    out={f:text_of(h)}
    base=urllib.parse.urlparse(f)
    for l in re.findall(r'href=["\']([^"\'#]+)["\']',h):
        u=urllib.parse.urljoin(f,l); p=urllib.parse.urlparse(u)
        if p.netloc!=base.netloc or u in out or re.search(r"\.(jpg|png|pdf|css|js|jpeg|webp|svg|ico)$",p.path,re.I): continue
        if re.search(hint,p.path,re.I) and len(out)<maxp:
            f2,h2=fetch(u,12)
            if f2: out[f2]=text_of(h2)
    return out,None
def hits(url, pat, n=4, w=130):
    pg,err=pages(url)
    if err: print("   FETCH FAIL",err[:70]); return
    alltxt=" ".join(pg.values())
    print("   pages:",[u.split('/',3)[-1][:28] for u in pg])
    cnt=len(re.findall(pat,alltxt,re.I)); print("   Treffer gesamt:",cnt)
    last=-999;c=0
    for m in re.finditer(pat,alltxt,re.I):
        if m.start()-last<350: continue
        last=m.start(); print("   ·",alltxt[max(0,m.start()-w):m.end()+w]); c+=1
        if c>=n: break
if __name__=="__main__":
    todo=[("Maki Pottery (bereinigte URL)","https://www.makipottery.de/","bemal|selbst|Rohling|paint|workshop"),
     ("mala Keramikstudio","https://malapottery.com/","bemal|paint|offene werkstatt|workshop"),
     ("Keramikkeller Leipzig","http://www.keramikkeller-leipzig.de/","bemal|Kurs|Töpfer|Glasur"),
     ("KILIAN KERAMIK workshops","http://www.kiliankeramik.com/","workshop|bemal|paint|töpfer|pottery")]
    for n,u,p in todo:
        print("###",n); hits(u,p)
