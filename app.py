import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TIP MSG Viewer", layout="wide")
st.title("🌍 위성 추락 경보 (TIP MSG) 실시간 뷰어")

latest_path = "data/tip_latest.csv"
new_csv_path = "data/tip_new.csv"
new_txt_path = "data/tip_new.txt"

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

        # 📥 TXT 다운로드
        if os.path.exists(new_txt_path):
            with open(new_txt_path, "r", encoding="utf-8") as f:
                txt_content = f.read()
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
