import requests, pandas as pd, os, datetime, logging
from io import StringIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 환경변수 확인
required_envs = ["SPACE_TRACK_USER", "SPACE_TRACK_PASS", "EMAIL_USER", "EMAIL_PASS", "EMAIL_TO"]
missing_envs = [env for env in required_envs if not os.getenv(env)]
if missing_envs:
    raise EnvironmentError(f"누락된 환경변수: {', '.join(missing_envs)}")

# 환경변수 로드
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

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_TO.split(","), msg.as_string())
        logging.info("📧 이메일 전송 완료")
    except Exception as e:
        logging.error(f"이메일 전송 실패: {e}")

def fetch_tip():
    logging.info("🚀 Space-Track 로그인 시도 중...")
    session = requests.Session()
    login_resp = session.post(LOGIN_URL, data={"identity": SPACE_TRACK_USER, "password": SPACE_TRACK_PASS})
    if login_resp.status_code != 200:
        raise ConnectionError("Space-Track 로그인 실패")

    logging.info("📥 TIP 데이터 요청 중...")
    resp = session.get(TIP_URL)
    if resp.status_code != 200:
        raise ConnectionError("TIP 데이터 요청 실패")

    try:
        df = pd.read_csv(StringIO(resp.text))
        logging.info(f"✅ TIP 메시지 {len(df)}건 수신 완료")
    except Exception as e:
        raise ValueError(f"CSV 파싱 실패: {e}")

    os.makedirs("data", exist_ok=True)
    today = datetime.datetime.utcnow().strftime("%Y%m%d")
    df.to_csv(f"data/tip_{today}.csv", index=False)
    df.to_string("data/tip_latest.txt")

    old_path = "data/tip_latest.csv"
    old_df = pd.read_csv(old_path) if os.path.exists(old_path) else None

    if old_df is not None:
        new_df = pd.concat([df, old_df]).drop_duplicates(keep=False)
        if not new_df.empty:
            new_df.to_csv("data/tip_new.csv", index=False)
            # TXT 저장 추가
            with open("data/tip_new.txt", "w", encoding="utf-8") as f:
                f.write(new_df.to_string(index=False))
            send_email(new_df)
        else:
            logging.info("📭 신규 TIP 메시지 없음")
    else:
        logging.info("📂 이전 TIP 데이터 없음, 최초 실행으로 간주")

    df.to_csv(old_path, index=False)

if __name__ == "__main__":
    try:
        fetch_tip()
    except Exception as e:
        logging.error(f"스크립트 실패: {e}")
        exit(1)
