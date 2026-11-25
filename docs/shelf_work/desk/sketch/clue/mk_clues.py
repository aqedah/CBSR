# 서고 이야기의 물건 셋(11-25): 열쇠 꾸러미(하나만 탐), 반쯤 탄 장부 쪽지, 그을린 서가에 들어온 책 한 권
import math, random
H='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
D='<defs><filter id="r"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter><radialGradient id="ch" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#1a0f08"/><stop offset=".7" stop-color="#2b1a0e"/><stop offset="1" stop-color="#4a2e18" stop-opacity="0"/></radialGradient></defs>'
def key(x,y,ang,col,burnt=False):
    g='<g transform="translate(%g %g) rotate(%g)">'%(x,y,ang)
    st='#2a1a0e' if not burnt else '#0b0604'
    g+='<circle cx="0" cy="0" r="11" fill="none" stroke="%s" stroke-width="6"/>'%col
    g+='<circle cx="0" cy="0" r="11" fill="none" stroke="%s" stroke-width="1.2"/>'%st
    g+='<rect x="-3.2" y="10" width="6.4" height="66" rx="2" fill="%s" stroke="%s" stroke-width="1.2"/>'%(col,st)
    g+='<path d="M3 58h12v6h-6v6h6v6H3z" fill="%s" stroke="%s" stroke-width="1.2"/>'%(col,st)
    if burnt: g+='<ellipse cx="0" cy="38" rx="9" ry="40" fill="url(#ch)" opacity=".7"/>'
    return g+'</g>'
k=H+D+'<g filter="url(#r)"><circle cx="100" cy="46" r="26" fill="none" stroke="#6b5232" stroke-width="7"/><circle cx="100" cy="46" r="26" fill="none" stroke="#2a1a0e" stroke-width="1.4"/>'
k+=key(78,70,22,'#b8945a')+key(100,74,0,'#1c120b',True)+key(122,70,-22,'#a9864e')+'</g></svg>'
open('clue_key.svg','w').write(k)
random.seed(5)
edge=[]; 
for i in range(0,41):
    yy=18+i*4.1; xx=150+random.uniform(-14,10)+ (8*math.sin(i*.9))
    edge.append((xx,yy))
pts='M30 18 L'+' L'.join('%.1f %.1f'%e for e in edge)+' L30 182 Z'
L=H+D+'<g filter="url(#r)"><path d="%s" fill="#e8d6ad" stroke="#5a4226" stroke-width="1.5"/>'%pts
L+='<path d="%s" fill="none" stroke="#1a0f08" stroke-width="9" opacity=".75"/>'%('M'+' L'.join('%.1f %.1f'%e for e in edge))
for i in range(9):
    y=36+i*15; L+='<line x1="40" y1="%d" x2="138" y2="%d" stroke="#8a6c44" stroke-width=".8"/>'%(y+4,y+4)
    w=random.randint(50,92) if i<8 else 70
    L+='<path d="M44 %d q6 -5 12 0 t12 0 t12 0 t12 0 t12 0 t12 0" fill="none" stroke="#3a2614" stroke-width="1.6" transform="scale(%.2f 1) translate(%d 0)"/>'%(y,w/90,0)
L+='<rect x="74" y="148" width="58" height="12" fill="#2b1a0e" opacity=".8" rx="3"/><ellipse cx="128" cy="150" rx="26" ry="18" fill="url(#ch)" opacity=".8"/></g></svg>'
open('clue_ledger.svg','w').write(L)
B=H+D+'<g filter="url(#r)"><rect x="70" y="28" width="60" height="150" rx="5" fill="#7a2f22" stroke="#2a120c" stroke-width="2"/><rect x="70" y="28" width="12" height="150" fill="#5e2219"/><rect x="76" y="50" width="48" height="5" fill="#d9b56a"/><rect x="76" y="150" width="48" height="5" fill="#d9b56a"/><rect x="88" y="80" width="30" height="44" rx="3" fill="#e8d6ad" stroke="#5a4226"/><path d="M95 94h16M95 102h16M95 110h12" stroke="#5a4226" stroke-width="2"/></g></svg>'
open('clue_book.svg','w').write(B)
print('ok')
