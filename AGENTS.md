# CBSR 저장소에서 작업할 때 (Claude·Codex 공통)

이 저장소의 **main 가지는 빌드 결과물**입니다. `index.html`, `try.html`, `sw.js` 등은 `source` 가지의 원본으로 만들어집니다.

## 지킬 것
1. **main의 index.html·try.html·sw.js를 직접 고치지 않습니다.** 다음 빌드 때 덮여 사라지고, 다른 대화가 올린 것과 엇갈려 올리기가 거절됩니다.
2. 고칠 것이 있으면 `source` 가지의 원본을 고칩니다.
   - 화면: `app/template3.html`
   - 지도 지명: `app/gaz.json` (`{"places":[[이름, 위도, 경도, 종류(, 추정 0/1, 확실성 0–1000)]], "people":[…]}`)
   - 빌드: `app/build_site.py` → `site/` 를 main에 복사
3. `source` 가지의 `app/`에 커밋하면 GitHub Actions(`.github/workflows/build.yml`)가 2–3분 안에 빌드해서 main에 올립니다. 직접 빌드하지 않아도 됩니다.
   - 목사님이 앱 관리자 화면에서 고친 내용은 `app/edits/inbox/`로 들어오고, 이 빌드가 원본 파일에 반영한 뒤 inbox를 비웁니다.
4. 커밋 작성자는 aqedah입니다. 공개 파일 안에 이메일을 쓰지 않습니다.

## MILALWV와의 관계
- 성경연구(히브리어 원문) 기능은 2026-10-23부터 MILALWV(aqedah/MILALWV)로 옮겼습니다. CBSR에는 메뉴의 MILALWV 배너만 있습니다.
- MILALWV에서 정한 지명을 CBSR 지도에 넣을 때는 `pipeline/cbsr_sync_places.py <CBSR source 가지 폴더>`로 `app/gaz.json`을 고쳐 source 가지에 커밋합니다.
