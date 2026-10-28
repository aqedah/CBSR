# 그림 목록(웹)에서 관리자가 고른 보관/삭제/되살리기를 Firestore config/photos 에서 읽어 옵니다
import json,urllib.request,os
KEY="AIzaSyAdq9kfpqC0yaEEGZ7_o4Ox44R-1mxszOg"; PRJ="cbsr-21238"
TOK=os.path.join(os.path.dirname(__file__),'.fb_refresh')
def post(u,d,h=None):
  r=urllib.request.Request(u,data=json.dumps(d).encode(),headers={'Content-Type':'application/json',**(h or {})}); return json.load(urllib.request.urlopen(r,timeout=20))
def token():
  if os.path.exists(TOK):
    try:
      r=urllib.request.Request(f"https://securetoken.googleapis.com/v1/token?key={KEY}",data=f"grant_type=refresh_token&refresh_token={open(TOK).read().strip()}".encode(),headers={'Content-Type':'application/x-www-form-urlencoded'})
      return json.load(urllib.request.urlopen(r,timeout=20))['id_token']
    except Exception: pass
  j=post(f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={KEY}",{"returnSecureToken":True}); open(TOK,'w').write(j['refreshToken']); return j['idToken']
def get():
  t=token()
  r=urllib.request.Request(f"https://firestore.googleapis.com/v1/projects/{PRJ}/databases/(default)/documents/config/photos",headers={'Authorization':'Bearer '+t})
  try: j=json.load(urllib.request.urlopen(r,timeout=20))
  except urllib.error.HTTPError as e:
    if e.code==404: return {}
    raise
  f=j.get('fields',{}).get('map',{}).get('mapValue',{}).get('fields',{})
  return {k:v.get('stringValue') for k,v in f.items()}
if __name__=='__main__': print(json.dumps(get(),ensure_ascii=False))
