# 장마다 절 수(개역개정, app/bible.b64에서 셈). make_plan_v5.py가 씁니다.
import json, os
VC = {int(k): v for k, v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bible_vc.json'))).items()}
