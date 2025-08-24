import requests, pandas as pd, os, datetime
from io import StringIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 환경변수에서 계정 정보 불러오기
SPACE_TRACK_USER = os.getenv("SPACE_TRACK_USER")
SPACE_TRACK_PASS = os.getenv("SPACE_TRACK_PASS")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")

LOGIN_URL = "https://www.space-track.org/ajaxauth/login"
TIP_URL   = "https://www.space-track.org/basicspacedata/query/class/tip/format/csv"

def send_email(new_df):
    subject = "[TIP MSG] 새로운 위성 추락 경보 발생"
    body = "새롭게 등록된 TIP 메시지:\n\n" + new_df.to_string(index=False)
    msg = MIMEMultipart()
    msg["From"], msg["To"], msg["Subject"] = EMAIL_USER, EMAIL_TO, subject
    msg.attach(MIMEText(body, "plain"))
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_TO.split(","), msg.as_string())

def fetch_tip():
    session = requests.Session()
    session.post(LOGIN_URL, data={"identity": SPACE_TRACK_USER, "password": SPACE_TRACK_PASS})
    resp = session.get(TIP_URL)
    df = pd.read_csv(StringIO(resp.text))
    os.makedirs("data", exist_ok=True)
    today = datetime.datetime.utcnow().strftime("%Y%m%d")
    df.to_csv(f"data/tip_{today}.csv", index=False)
    df.to_csv("data/tip_latest.csv", index=False)
    df.to_string("data/tip_latest.txt")

    # 새로운 메시지 비교
    if os.path.exists("data/tip_latest.csv"):
        old_df = pd.read_csv("data/tip_latest.csv")
        new_df = df.merge(old_df, how="outer", indicator=True)
        new_df = new_df[new_df["_merge"] == "left_only"].drop(columns=["_merge"])
        if not new_df.empty:
            new_df.to_csv("data/tip_new.csv", index=False)
            send_email(new_df)

if __name__ == "__main__":
    fetch_tip()
