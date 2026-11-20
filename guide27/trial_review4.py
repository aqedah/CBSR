# 체험판 목사님 원고 칸 고침(11-20 밤, 목사님이 골라 정함): GPT 문장 연결 검토 가운데 338 성경 전체로, 317·347·322·341·326·362 해설.
# 원고 json(trial_wN.json)과 작업대 원고(trial26_qt.json)에 같은 바꿈을 겁니다. 다시 돌려도 결과가 같습니다.
import json,os
R=os.path.dirname(os.path.abspath(__file__))
RP={
338:[('주는 사람은 잃지 않습니다. 하나님이 채우시기 때문입니다(9:8).','하나님은 은혜를 넉넉히 주셔서 우리가 선한 일을 넉넉히 하게 하십니다(9:8).')],
317:[('2:42–47에는 주목할 만한 큰 사건이 등장하지 않습니다. 대신 초대교회가 날마다 반복한 생활을 보여줍니다.','2:42–47은 기사와 표적이 나타나는 가운데, 성도들이 날마다 이어 간 생활을 보여 줍니다.')],
347:[('하와는 전해 들은 말씀에 더하고 빼다가 속았지요(2:14; 창 3:3). 이것은 남녀의 문제가 아닙니다.','하와가 한 말은 하나님이 하신 명령과 다릅니다(창 2:17; 3:3). 바울은 하와가 속았다고 말합니다(2:14). 바울이 짚는 것은 남녀의 문제가 아닙니다.')],
322:[('누가 옳은지를 따지기 전에, 하나님이 무엇을 하셨는지를 먼저 듣지요(15:8, 12).','논쟁 가운데 하나님이 이방인에게 하신 일을 듣고, 선지자들의 말씀에 비추어 판단하지요(15:7–15).')],
341:[('성령을 따라 사는 삶에서는 이 성품들이 함께 맺힙니다. 하나씩 골라 기르는 것이 아니지요.','성령을 따라 사는 삶 전체에서 이 성품들이 함께 맺힙니다.')],
326:[('그렇다면 누가는 왜 바울의 재판 결과를 적는 대신 이 장면에서 책을 마쳤을까요? 1:8의 땅 끝까지가 아직 남아 있기 때문입니다.','누가는 바울의 재판 결과를 적는 대신 이 장면에서 책을 마칩니다. 책은 거침없이 전해지는 말씀으로 끝나, 땅 끝을 향한 증언(1:8)을 생각하게 합니다.')],
362:[('즉, 십사만 사천은','두 모습을 같은 백성으로 읽으면, 십사만 사천은')],
}
def walk(o,a,b):
    if isinstance(o,str): return o.replace(a,b)
    if isinstance(o,list): return [walk(x,a,b) for x in o]
    if isinstance(o,dict): return {k:walk(v,a,b) for k,v in o.items()}
    return o
hit={n:0 for n in RP}
for w in range(1,8):
    F=os.path.join(R,f'trial_w{w}.json'); L=json.load(open(F))
    for i,D in enumerate(L):
        for a,b in RP.get(D['no'],[]):
            s=json.dumps(D,ensure_ascii=False); L[i]=D=walk(D,a,b)
            if json.dumps(D,ensure_ascii=False)!=s: hit[D['no']]+=1
    json.dump(L,open(F,'w'),ensure_ascii=False,indent=1)
Q=os.path.join(R,'..','app','site_src','trial26_qt.json'); J=json.load(open(Q))
for n,ps in RP.items():
    x=J['qt'][str(n)]
    for a,b in ps:
        y=walk(x,a,b); ok=json.dumps(y,ensure_ascii=False)!=json.dumps(x,ensure_ascii=False) or b in json.dumps(x,ensure_ascii=False)
        assert ok,(n,a); J['qt'][str(n)]=x=y
json.dump(J,open(Q,'w'),ensure_ascii=False,indent=1)
print('원고 json에서 바뀐 날',hit)
