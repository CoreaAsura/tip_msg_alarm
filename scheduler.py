import pandas as pd
from datetime import datetime, timedelta
from fetch_tip import fetch_tip_messages
from email_alert import send_email_alert

# 인증 정보
EMAIL = "your_spacetrack_email"
PASSWORD = "your_spacetrack_password"
CSV_PATH = "data/tip_new.csv"

# TIP 메시지 수집
fetch_tip_messages(EMAIL, PASSWORD, CSV_PATH)

# 신규 메시지 필터링
df = pd.read_csv(CSV_PATH)
df["MSG_EPOCH"] = pd.to_datetime(df["MSG_EPOCH"], errors="coerce", utc=True)
now = datetime.utcnow()
recent_df = df[df["MSG_EPOCH"] >= now - timedelta(hours=2)]

# 알림 조건
if not recent_df.empty:
    send_email_alert("your_alert_email@example.com", len(recent_df), "https://your-streamlit-app-url/data/tip_new.csv")
