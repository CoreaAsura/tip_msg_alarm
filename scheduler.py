import os
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ✅ 환경 변수에서 인증 정보 불러오기
SPACETRACK_EMAIL = os.environ["SPACETRACK_EMAIL"]
SPACETRACK_PASSWORD = os.environ["SPACETRACK_PASSWORD"]
SMTP_EMAIL = os.environ["SMTP_EMAIL"]
SMTP_PASSWORD = os.environ["SMTP_PASSWORD"]
ALERT_RECIPIENT = os.environ["ALERT_RECIPIENT"]

CSV_PATH = "data/tip_new.csv"

# ✅ TIP 메시지 다운로드 함수
def fetch_tip_messages(email, password, save_path):
    login_url = "https://www.space-track.org/ajaxauth/login"
    query_url = "https://www.space-track.org/basicspacedata/query/class/tip/orderby/MSG_EPOCH desc/format/csv"
    credentials = {"identity": email, "password": password}

    # 폴더가 없으면 생성
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with requests.Session() as session:
        login = session.post(login_url, data=credentials)
        if login.status_code != 200:
            raise Exception("SPACE-TRACK 로그인 실패")

        response = session.get(query_url)
        if response.status_code == 200:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(response.text)
        else:
            raise Exception("TIP 메시지 다운로드 실패")

# ✅ 이메일 알림 함수
def send_email_alert(sender, password, recipient, new_count, csv_url):
    msg = MIMEMultipart()
    msg["Subject"] = f"[TIP 알림] 최근 2시간 이내 신규 메시지 {new_count}건"
    msg["From"] = sender
    msg["To"] = recipient

    body = f"""
    최근 2시간 이내 TIP 메시지가 {new_count}건 발견되었습니다.
    아래 링크에서 CSV 파일을 다운로드하세요:

    {csv_url}
    """
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

# ✅ 실행 로직
def main():
    fetch_tip_messages(SPACETRACK_EMAIL, SPACETRACK_PASSWORD, CSV_PATH)

    df = pd.read_csv(CSV_PATH)
    df["MSG_EPOCH"] = pd.to_datetime(df["MSG_EPOCH"], errors="coerce", utc=True)

    now = datetime.now(timezone.utc)
    recent_df = df[df["MSG_EPOCH"] >= now - timedelta(hours=2)]

    if not recent_df.empty:
        # Streamlit 앱에서 접근 가능한 CSV URL로 교체
        csv_url = "https://your-streamlit-app-url/data/tip_new.csv"
        send_email_alert(SMTP_EMAIL, SMTP_PASSWORD, ALERT_RECIPIENT, len(recent_df), csv_url)

if __name__ == "__main__":
    main()
