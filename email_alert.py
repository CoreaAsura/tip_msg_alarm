import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(to_email, new_count, csv_url):
    msg = MIMEMultipart()
    msg["Subject"] = f"[TIP 알림] 최근 2시간 이내 신규 메시지 {new_count}건"
    msg["From"] = "your_email@example.com"
    msg["To"] = to_email

    body = f"""
    최근 2시간 이내 TIP 메시지가 {new_count}건 발견되었습니다.
    아래 링크에서 CSV 파일을 다운로드하세요:

    {csv_url}
    """
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("your_email@example.com", "your_password")
        server.send_message(msg)
