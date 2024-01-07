import os
import json
import datetime
import pyperclip
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# 設定ファイルを読み込む
with open("config.json") as json_file:
    config = json.load(json_file)

# スコープを変更する場合は、token.jsonファイルを削除する必要があります。
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

creds = None
"""
NOTE: token.jsonファイルは、ユーザーのアクセストークンとリフレッシュトークンを保存し、
最初の認証フローが完了したときに自動的に作成されます。
"""
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json")
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_config({"installed": config["installed"]}, SCOPES)
        creds = flow.run_local_server(port=0)
    # 次回の実行のために認証情報を保存
    with open("token.json", "w") as token:
        token.write(creds.to_json())

# Calendar APIを呼び出す
calendar = build("calendar", "v3", credentials=creds)

start_of_day = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
end_of_day = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + "Z"

# 今日のイベントを取得
print("今日のイベントを取得します")
events_result = (
    calendar.events()
    .list(
        calendarId=config["calendar_id"],
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy="startTime",
    )
    .execute()
)
events = events_result.get("items", [])

if not events:
    print("予定されているイベントはありません。")

# テンプレートファイルを読み込む
with open("template.txt", "r") as file:
    template = file.read().strip()

# イベントの情報をテンプレートに適用
event_summaries = ["- " + event["summary"] for event in events]
events_str = "\n".join(event_summaries)

# テンプレートにイベントの情報を適用
output = template.format(events=events_str)

# クリップボードにコピー
pyperclip.copy(output)

print(output)
