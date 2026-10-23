# CBSR 저장소에서 작업할 때 (Claude·Codex 공통)

이 저장소의 **main 가지는 빌드 결과물**입니다. `index.html`, `try.html`, `sw.js` 등은 `source` 가지의 원본으로 만들어집니다.

## 지킬 것
1. **main의 index.html·try.html·sw.js를 직접 고치지 않습니다.** 다음 빌드 때 덮여 사라지고, 다른 대화가 올린 것과 엇갈려 올리기가 거절됩니다.
2. 고칠 것이 있으면 `source` 가지의 원본을 고칩니다.
   - 화면: `app/template3.html`
   - 지도 지명: `app/gaz.json` (`{"places":[[이름, 위도, 경도, 종류(, 추정 0/1, 확실성 0–1000)]], "people":[…]}`)
   - 빌드: `app/build_site.py` → `site/` 를 main에 복사
3. 원본을 바꾼 대화가 직접 빌드할 수 없으면 `source` 가지에만 커밋하고 끝냅니다. CBSR을 맡은 대화가 다음 배포 때 source 가지의 바뀐 파일을 받아 함께 빌드합니다.
4. 커밋 작성자는 aqedah입니다. 공개 파일 안에 이메일을 쓰지 않습니다.

## MILALWV와의 관계
- 성경연구(히브리어 원문) 기능은 2026-10-23부터 MILALWV(aqedah/MILALWV)로 옮겼습니다. CBSR에는 메뉴의 MILALWV 배너만 있습니다.
- MILALWV에서 정한 지명을 CBSR 지도에 넣을 때는 `pipeline/cbsr_sync_places.py <CBSR source 가지 폴더>`로 `app/gaz.json`을 고쳐 source 가지에 커밋합니다.
