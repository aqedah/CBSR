/* Firebase 설정값 (웹 앱용 공개 설정 — 보안은 firestore.rules가 지킵니다) */
window.CBSR_FIREBASE_CONFIG = {
  apiKey: "AIzaSyAdq9kfpqC0yaEEGZ7_o4Ox44R-1mxszOg",
  authDomain: "cbsr-21238.firebaseapp.com",
  projectId: "cbsr-21238",
  storageBucket: "cbsr-21238.firebasestorage.app",
  messagingSenderId: "693544806035",
  appId: "1:693544806035:web:aabdc21325be4d79288f66"
};

/* 이름 + 숫자 4자리로 기록 이어 보기: 지금은 끔(false). 필요할 때 true로 바꾸면 '나의 기록'에 등록 칸이 나옵니다. */
window.CBSR_LOGIN = false;

/* 관리자 계정(이메일/비밀번호 로그인). 앱에서는 비밀번호만 입력합니다. Firebase 콘솔 Authentication > 사용자에 이 이메일로 계정을 만들어 두세요. */
window.CBSR_ADMIN_EMAIL = "admin@cbsr-21238.firebaseapp.com";
