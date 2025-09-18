import requests
import os

def fetch_tip_messages(email, password, save_path):
    login_url = "https://www.space-track.org/ajaxauth/login"
    query_url = "https://www.space-track.org/basicspacedata/query/class/tip/orderby/MSG_EPOCH desc/format/csv"
    credentials = {"identity": email, "password": password}

    # ✅ 폴더가 없으면 생성
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with requests.Session() as session:
        session.post(login_url, data=credentials)
        response = session.get(query_url)
        if response.status_code == 200:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(response.text)
        else:
            raise Exception("TIP 메시지 다운로드 실패")
