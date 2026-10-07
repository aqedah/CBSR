# 이야기 통독 노트 (CBSR)

중앙성서교회 성도들을 위한 성경통독 웹앱입니다. 리딩지저스 45주 일정에 맞춰 오늘 본문, 요약, 단어 설명, 지도, 퀴즈, QT를 제공합니다.

- 휴대폰에서 열고 「홈 화면에 추가」하면 앱처럼 쓸 수 있습니다. 한 번 연 뒤에는 인터넷이 없어도 열립니다.
- 기록(진행률·퀴즈·QT)은 각자 휴대폰에 저장됩니다. 이름 + 숫자 4자리로 다른 기기와 이어 보는 기능은 만들어 두었지만 지금은 꺼 두었습니다. `config.js`의 `CBSR_LOGIN`을 `true`로 바꾸면 켜집니다.
- 통독을 마치면 교회 전체 '함께 읽기' 숫자가 올라갑니다(이름 없이 숫자만).

## 처음 설정 (한 번만)

1. Firebase 콘솔(https://console.firebase.google.com)에서 새 프로젝트를 만듭니다. 이름 예: `CBSR`
2. **빌드 → Authentication → 시작하기 → 로그인 방법 → 익명**을 켭니다.
3. **빌드 → Firestore Database → 데이터베이스 만들기** (위치: `asia-northeast3 (서울)`, 프로덕션 모드)
4. Firestore의 **규칙** 탭에 이 저장소의 `firestore.rules` 내용을 붙여 넣고 게시합니다.
5. **프로젝트 설정 → 일반 → 내 앱 → 웹 앱 추가(</>)** 를 누르고 나오는 `firebaseConfig` 값을 `config.js`에 넣습니다.
6. **Authentication → 설정 → 승인된 도메인**에 `aqedah.github.io`를 추가합니다.
7. GitHub 저장소 **Settings → Pages**에서 `main` 브랜치, `/ (root)`를 선택합니다.

주소: https://aqedah.github.io/CBSR/

## 파일

| 파일 | 내용 |
|---|---|
| `og.png` | 카카오톡 등에서 공유할 때 보이는 썸네일 |
| `index.html` | 앱 화면과 내용(요약, 퀴즈, 단서, QT 등) |
| `bible.js` | 개역개정 본문(압축) |
| `terrain/` | 지형도 이미지 |
| `sync.js` | 기록 이어 보기 · 함께 읽기 (Firebase) |
| `config.js` | Firebase 설정값 |
| `sw.js`, `manifest.webmanifest`, `icons/` | 앱처럼 설치하고 오프라인으로 쓰기 위한 파일 |
| `firestore.rules` | Firestore 보안 규칙 |

지형: AWS Terrain Tiles(Mapzen) · 해안선: Natural Earth · 성경 본문: 개역개정4판 · 통독 일정: 리딩지저스 45주 성경통독표(웨스트민스터코리아)

제작: 이삭 목사 (중앙성서교회) https://www.centralbible.net/
