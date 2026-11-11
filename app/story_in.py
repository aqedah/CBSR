# 스토리 작업실(story_edit.html)이 GitHub에 저장한 날별 원고(ux/story_in/날번호.json)를 ux/story_cards.json에 합칩니다.
# 파일 하나가 하루 원고: {"n":305,"plan":"2026-365","label":"…","at":시각,"A":{type,spine,cards,kwq,qt}}
# 같은 날의 옛 원고는 _backup["305A_날짜"]에 보관한 뒤 덮어씁니다. 합친 파일은 지웁니다(빌드가 원본 보관 단계에서 커밋).
import json,os,glob,time
R=os.path.dirname(os.path.abspath(__file__)); os.chdir(R)
IN=sorted(glob.glob('ux/story_in/*.json'))
if not IN: raise SystemExit(0)
SC='ux/story_cards.json'
d=json.load(open(SC,encoding='utf-8'))
bk=d.setdefault('_backup',{})
for f in IN:
    try: e=json.load(open(f,encoding='utf-8'))
    except Exception as x: print('story_in 읽기 실패',f,x); continue
    n=str(e.get('n') or os.path.splitext(os.path.basename(f))[0]); A=e.get('A') or e
    if not isinstance(A,dict) or not isinstance(A.get('cards'),list): print('story_in 형식 아님',f); continue
    if n in d and not n.startswith('_'):
        old=d[n].get('A',d[n]) if isinstance(d[n],dict) else d[n]
        bk[f'{n}A_{time.strftime("%Y-%m-%d")}']=old
    d[n]={'A':A}
    os.remove(f); print('story_in 반영:',n,e.get('label',''))
json.dump(d,open(SC,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
