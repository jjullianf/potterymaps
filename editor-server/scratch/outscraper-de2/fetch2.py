import sys,re,html,urllib.request,ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
def get(u):
    r=urllib.request.Request(u,headers={"User-Agent":UA,"Accept":"text/html,*/*","Accept-Language":"de"})
    with urllib.request.urlopen(r,timeout=20,context=ctx) as x: return x.geturl(),x.read(700000).decode('utf-8','ignore')
for u in sys.argv[1:]:
    try:
        f,h=get(u)
        t=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>',' ',h);t=re.sub(r'(?s)<[^>]+>',' ',t);t=re.sub(r'\s+',' ',html.unescape(t))
        print("==",u,"->",f,len(t)); 
        for m in re.finditer(r'(selbst\s+bemal|bemalen|bemalst|Rohling|paint)',t,re.I):
            print("  +",t[max(0,m.start()-80):m.end()+120]); break
        print("  TXT:",t[:500])
    except Exception as e: print("==",u,"ERR",e)
