# 쉬운 말 고치기 적용: {day: {spine|kwq|obs|lookN|cN.h|cN.sub|cN.lab: 새 문장}}
import json,sys
def apply(D,E):
    for d,ch in E.items():
        A=D[d]
        if 'A' in A and 'cards' not in A: A=A['A']
        for k,v in ch.items():
            if k=='spine': A['spine']=v
            elif k=='kwq': A.setdefault('kwq',{})['q']=v
            elif k=='obs': A['qt']['obs']['q']=v
            elif k.startswith('look'): A['qt']['obs']['look'][int(k[4:])]['n']=v
            elif k.startswith('c'):
                i,f=k[1:].split('.'); A['cards'][int(i)][f]=v
            else: raise KeyError(k)
if __name__=='__main__':
    f,e=sys.argv[1],sys.argv[2]; D=json.load(open(f)); apply(D,json.load(open(e))); json.dump(D,open(f,'w'),ensure_ascii=False,indent=1); print('ok')
