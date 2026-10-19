import sys,re,html,urllib.request,urllib.parse,ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
def get(u):
    r=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0 (potterymaps research)"})
    with urllib.request.urlopen(r,timeout=20,context=ctx) as x: return x.geturl(),x.read(800000).decode('utf-8','ignore')
u=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 3500
f,h=get(u)
links=[]
for l in re.findall(r'href=["\']([^"\'#]+)["\']',h):
    a=urllib.parse.urljoin(f,l)
    if urllib.parse.urlparse(a).netloc==urllib.parse.urlparse(f).netloc and a not in links and not re.search(r'\.(jpg|png|css|js|pdf|svg|webp)',a): links.append(a)
t=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>',' ',h);t=re.sub(r'(?s)<[^>]+>',' ',t);t=re.sub(r'\s+',' ',html.unescape(t))
print(t[:n]); print("LINKS:",links[:40])
