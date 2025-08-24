import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TIP MSG 모니터링", layout="wide")
st.title("🛰️ 위성 추락 경보 모니터링 (TIP MSG)")

DATA_FILE = "data/tip_latest.csv"
TXT_FILE  = "data/tip_latest.txt"

if st.button("📡 즉시 TIP 확인"):
    os.system("python fetch_tip.py")

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.success(f"최신 TIP 메시지 {len(df)}건을 불러왔습니다.")
    st.dataframe(df)
    st.download_button("📄 CSV 다운로드", df.to_csv(index=False).encode("utf-8"), "tip_latest.csv", "text/csv")
    with open(TXT_FILE, "r", encoding="utf-8") as f:
        txt_data = f.read()
    st.download_button("📄 TXT 다운로드", txt_data.encode("utf-8"), "tip_latest.txt", "text/plain")
else:
    st.warning("아직 TIP MSG 데이터가 없습니다. 자동 수집 대기 중입니다.")
