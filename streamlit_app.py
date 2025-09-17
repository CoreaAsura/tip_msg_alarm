import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
import os

st.set_page_config(page_title="TIP MSG Viewer", layout="wide")
st.title("위성추락경보 for MSSB")

CSV_PATH = "data/tip_new.csv"

# ✅ 1. Streamlit secrets에서 계정 정보 불러오기
email = st.secrets["SPACETRACK_EMAIL"]
password = st.secrets["SPACETRACK_PASSWORD"]

# ✅ 2. SPACE-TRACK에서 TIP 메시지 다운로드
def fetch_tip_messages(email, password, save_path):
    login_url = "https://www.space-track.org/ajaxauth/login"
    query_url = "https://www.space-track.org/basicspacedata/query/class/tip/orderby/MSG_EPOCH desc/format/csv"
    credentials = {"identity": email, "password": password}

    with requests.Session() as session:
        session.post(login_url, data=credentials)
        response = session.get(query_url)
        if response.status_code == 200:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(response.text)
        else:
            st.error("❌ TIP 메시지 다운로드 실패")

# ✅ 3. 데이터 다운로드 및 로딩
if not os.path.exists(CSV_PATH):
    os.makedirs("data", exist_ok=True)
    fetch_tip_messages(email, password, CSV_PATH)

if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
    df["MSG_EPOCH"] = pd.to_datetime(df["MSG_EPOCH"], errors="coerce", utc=True)
    now = datetime.utcnow().replace(tzinfo=pytz.UTC)

    week_df = df[df["MSG_EPOCH"] >= now - timedelta(days=7)]
    month_df = df[df["MSG_EPOCH"] >= now - timedelta(days=30)]

    st.subheader("📅 최근 1주일 이내 TIP MSG")
    if not week_df.empty:
        st.download_button("📥 1주일 CSV 다운로드", week_df.to_csv(index=False).encode("utf-8"), "week_tip.csv", "text/csv")
    else:
        st.info("✅ 최근 1주일 이내 메시지 없음")

    st.subheader("📆 최근 1개월 이내 TIP MSG")
    if not month_df.empty:
        st.download_button("📥 1개월 CSV 다운로드", month_df.to_csv(index=False).encode("utf-8"), "month_tip.csv", "text/csv")
    else:
        st.info("✅ 최근 1개월 이내 메시지 없음")
else:
    st.warning("TIP 메시지 파일이 없습니다.")
