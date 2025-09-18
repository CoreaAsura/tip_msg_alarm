# TIPmsg
# 📡 TIP Message Alarm System

실시간 위성 추락 경보 시스템입니다.  
SPACE-TRACK API를 통해 TIP 메시지를 수집하고, Streamlit 앱으로 시각화하며, GitHub Actions를 통해 2시간마다 자동으로 신규 메시지를 감지하고 이메일로 알림을 전송합니다.

---

## 🚀 주요 기능

- **Streamlit 앱**
  - 최근 7일 / 30일 이내 TIP 메시지 확인
  - CSV 다운로드 버튼 제공

- **자동 알림 시스템 (GitHub Actions)**
  - 2시간마다 SPACE-TRACK에서 TIP 메시지 수집
  - 최근 2시간 이내 신규 메시지 존재 시 이메일 알림 발송
  - CSV 파일 자동 갱신

---

## 📁 프로젝트 구조
tip_msg_alarm/ ├── .github/workflows/ │   └── tip_alert.yml           # GitHub Actions 워크플로우 ├── data/ │   └── tip_new.csv             # TIP 메시지 저장 파일 ├── email_alert.py             # 이메일 발송 로직 ├── fetch_tip.py               # SPACE-TRACK API 연동 ├── run_scheduler.py           # 워크플로우 실행 스크립트 ├── streamlit_app.py           # Streamlit 앱 ├── requirements.txt           # 의존성 목록 ├── README.md                  # 프로젝트 설명

---

## 🔐 인증 정보 설정

### ✅ Streamlit Cloud

`App Settings → Secrets`에서 아래와 같이 TOML 형식으로 입력:

```toml
SPACETRACK_EMAIL = "your_spacetrack_email"
SPACETRACK_PASSWORD = "your_spacetrack_password"
SMTP_USERNAME = "your_gmail_address"
SMTP_PASSWORD = "your_gmail_app_password"
ALERT_RECIPIENT = "receiver_email@example.com"



