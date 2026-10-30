import json
for line in open('/root/.claude/projects/-home-claude/3fb3d98f-d07a-5505-a04d-ced931eb45d4.jsonl'):
  if 'CBSR 그림 라이브러리 2단계 보고' not in line: continue
  try: o=json.loads(line)
  except: continue
  for c in (o.get('message',{}).get('content') or []):
    if isinstance(c,dict) and c.get('type')=='tool_use' and 'CBSR 그림 라이브러리 2단계 보고' in c['input'].get('command',''):
      cmd=c['input']['command']
start=cmd.index("python3 - <<'E'\n")+len("python3 - <<'E'\n"); end=cmd.rindex("\nE")
s=cmd[start:end]
s=s.replace("| ② | **범용 소품·장소·사람 장면**에 낱말이 붙어 있으면 그 낱말이 카드에 있을 때만 | g27_14 성벽, g21_10 글 쓰는 손 등 |","| ② | **범용 사람 장면**에 낱말이 붙어 있으면 그 낱말이 카드에 있을 때만. **범용 소품·장소**는 낱말이 있거나 맞는 태그가 둘 이상일 때만 | g27_14 성벽, g21_10 글 쓰는 손 등 |")
open('rep2.py','w').write(s); print(len(s))