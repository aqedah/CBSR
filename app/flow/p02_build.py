import json,importlib.util,sys
D={}
for m in ['p02_lev','p02_num','p02_deu']:
    try:
        spec=importlib.util.spec_from_file_location(m,f'/home/claude/rj/flow/{m}.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); D.update(mod.D)
    except FileNotFoundError: pass
json.dump(D,open('/home/claude/rj/flow/part02.json','w'),ensure_ascii=False,indent=0)
