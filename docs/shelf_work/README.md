# 성경 서고 작업 원본

앱에 들어가는 것은 `app/site_src/shelf.js`, `app/site_src/shelf_66.json`, `app/site_src/shelf_edit.html`, `app/site_src/img/shelf/`입니다. 이 폴더에는 그것들을 만드는 원본을 보관합니다. 이 폴더를 고쳐도 빌드는 돌지 않습니다.

- `desk/shelf.src.js` + `desk/shelf_art.json` → `desk/make_shelf.py`가 `app/site_src/shelf.js`와 `shelf_66.json`을 만듭니다.
- `desk/data/*.md` — 66권 개론 원고(합본). `desk/data_v1/`은 첫 초안, `desk/merge.py`는 합본을 만든 규칙입니다.
- `desk/template.html` + `desk/build.py` → 작업대(`shelf_edit.html`).
- `desk/check/` — 화면 시험.
- `desk/sketch/` — 사서 그림과 대화 틀 스케치(2026-11-24). `mk_libr.py`로 그리고 `engr.py`로 판화 결을 입힙니다. 앱에 들어간 그림은 `libr7a`(3차, 인자한 얼굴을 어둡게: `engr.py … facel=0.5 base=0.30 gain=0.9`), 카드를 드는 사서 `libr7c`(`mk_libr_c.py`), 카드를 쥔 손 `hand`입니다. `libr6`은 2차(밝은 것)이고 `libr4`·`mk_libr_1차.py`는 1차 시안입니다. `board.html`이 처음 장면 스케치입니다.
- `desk/check/test_dlg.py`(대화·안내·적어 두기), `test_card.py`(통독표·말씀 카드), `test_app2.py`·`test_app3.py`(실제 빌드)가 지금 쓰는 시험입니다. `test_qa.py`·`test_etc.py`는 옛 화면(다섯 물음, 경고장 단추) 것입니다.
- `art_tools/` — 서고 그림을 그리는 도구(`engrave.py`가 서고 전경과 서가, `mkpress.py`가 서가 일곱 장).
- `sian/` — 처음 시안 네 가지.
