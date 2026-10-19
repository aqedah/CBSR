# CBSR 원본 보관 (source 가지)

이 가지는 배포용이 아닙니다. GitHub Pages는 main 가지만 띄웁니다.
main 가지에는 완성된 앱(index.html 등)만 있고, 여기에는 그것을 만드는 원본을 둡니다.

- `app/` : 앱 원본. `template3.html`(화면), `build_site.py`(빌드), 통독·QT 자료(srj, s365b, tools, flow …), 성경연구 코드(study_*.js), 점검 스크립트(ux/)
  - 빌드: `python3 build_site.py` → `site/` → main 가지에 복사
  - 빠진 것: `study/` 자료는 main 가지의 `study/`, 번역 원문 작업 파일(tr/), 지도 타일(tiles/), 화면 캡처(png)는 보관하지 않음
- `lex/` : 성경연구 자료 만드는 스크립트(BHSA → meta/words.json), 짧은 우리말 뜻(gl/), 스트롱 사전 우리말 번역(st/), LOG 한국어 사전(dl/)
  - 필요한 외부 자료: BHSA Text-Fabric 2021, OSHB morphhb(git clone), Open Scriptures HebrewLexicon
- `docs/` : GPT 보고서, 내러티브 원칙, MILALWV 시작 문서
