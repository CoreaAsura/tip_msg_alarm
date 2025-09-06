import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TIP MSG Viewer", layout="wide")
st.title("위성추락경보 for MSSB")

latest_path = "data/tip_latest.csv"
new_csv_path = "data/tip_new.csv"
new_txt_path = "data/tip_new.txt"

# 분석 앱에서 요구하는 전체 TIP 필드
TIP_COLUMNS = [
    "NORAD_CAT_ID", "MSG_EPOCH", "INSERT_EPOCH", "DECAY_EPOCH", "WINDOW", "REV",
    "DIRECTION", "LAT", "LON", "INCL", "NEXT_REPORT", "ID", "HIGH_INTEREST", "OBJECT_NUMBER"
]

# 📌 최신 TIP MSG
if os.path.exists(latest_path):
    df = pd.read_csv(latest_path)
    st.subheader("📌 최신 TIP MSG")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("아직 TIP MSG 데이터가 없습니다.")

# 🚨 신규 TIP MSG
if os.path.exists(new_csv_path):
    new_df = pd.read_csv(new_csv_path)

    # TIP_COLUMNS 기준으로 정렬 및 누락 컬럼 채우기
    for col in TIP_COLUMNS:
        if col not in new_df.columns:
            new_df[col] = None
    new_df = new_df[TIP_COLUMNS]

    if not new_df.empty:
        st.subheader("🚨 신규 TIP MSG 감지됨!")
        st.dataframe(new_df, use_container_width=True)

        # 📥 CSV 다운로드
        st.download_button(
            label="📥 신규 TIP MSG CSV 다운로드",
            data=new_df.to_csv(index=False).encode("utf-8"),
            file_name="new_tip_msg.csv",
            mime="text/csv"
        )

        # 📥 TXT 다운로드 (Markdown 스타일로 보기 좋게)
        txt_content = new_df.to_markdown(index=False)
        st.download_button(
            label="📥 신규 TIP MSG TXT 다운로드",
            data=txt_content,
            file_name="new_tip_msg.txt",
            mime="text/plain"
        )
    else:
        st.info("✅ 현재 신규 TIP MSG는 없습니다.")
else:
    st.info("아직 신규 TIP MSG 데이터가 없습니다.")
