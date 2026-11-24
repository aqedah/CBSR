# v2_content.py의 새 틀 원고를 w*.py에 넣습니다.
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from v2_content import V2, MARKS_1124
R = lambda x: repr(x)
def items(name, L):
    return f' {name}=[\n' + ''.join(f'  {R(x) if isinstance(x,str) else "dict(" + ", ".join(f"{k}={R(v)}" for k,v in x.items()) + ")"},\n' for x in L) + ' ],\n'
for k, D in V2.items():
    p = os.path.join(H, f'w{k}.py'); s = open(p).read()
    a = s.index('\n obs=['); b = s.index('\n note=')
    new = '\n' + items('obs', D['obs']) + items('god', D['god']) + f" apply=dict(lead={R(D['apply']['lead'])}, fu={R(D['apply']['fu'])}),"
    s = s[:a] + new + s[b:]
    if k == '1124':
        a = s.index('\n marks=['); b = s.index('\n obs=[')
        s = s[:a] + '\n' + items('marks', MARKS_1124['marks']) + items('looks', MARKS_1124['looks'])[:-1] + s[b:]
    if 'whole' in D:
        if "W['whole']" in s: s = s[:s.index("W['whole']")]
        s = s.rstrip() + '\nW[\'whole\'] = [\n' + ''.join(f" dict(lab={R(x['lab'])}, ref={R(x['ref'])}, text={R(x['text'])}),\n" for x in D['whole']) + ']\n'
    open(p, 'w').write(s)
    exec(compile(s, p, 'exec'), {})
print('ok')
