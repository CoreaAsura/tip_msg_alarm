import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
import os

st.set_page_config(page_title="TIP MSG Viewer", layout="wide")
st.title("위성추락경보 for MSSB")

CSV_PATH = "data/tip_new.csv"

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
