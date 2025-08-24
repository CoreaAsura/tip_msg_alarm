import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TIP MSG Viewer", layout="wide")
st.title("🌍 위성 추락 경보 (TIP MSG) 실시간 뷰어")

latest_path = "data/tip_latest.csv"
new_path = "data/tip_new.csv"

if os.path.exists(latest_path):
    df = pd.read_csv(latest_path)
    st.subheader("📌 최신 TIP MSG")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("아직 TIP MSG 데이터가 없습니다. 먼저 fetch_tip.py를 실행해주세요.")

if os.path.exists(new_path):
    new_df = pd.read_csv(new_path)
    if not new_df.empty:
        st.subheader("🚨 신규 TIP MSG 감지됨!")
        st.dataframe(new_df, use_container_width=True)
    else:
        st.info("신규 TIP MSG는 없습니다.")
else:
    st.info("아직 신규 TIP MSG 데이터가 없습니다.")
