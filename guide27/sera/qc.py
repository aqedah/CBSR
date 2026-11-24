import sys,re,json,importlib
sys.path.insert(0,'..'); from bq import B,AB
def chk(mod,books):
    W=importlib.import_module(mod).W
    norm=lambda s:re.sub(r'[\s,.?!·]','',s)
    T=norm(''.join(''.join(''.join(c) for c in B[AB[b]-1]) for b in books))
    txt=json.dumps(W,ensure_ascii=False)
    bad=[m for m in re.findall(r'\\"([^"\\]+)\\"',txt) if not all(norm(p) in T for p in m.split('…'))]
    print(mod,'인용 확인 안 된 것:',bad or '없음')
chk(sys.argv[1],sys.argv[2].split(','))
