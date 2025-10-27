from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# ⚠️ 換成你的 LINE Channel 資料
LINE_CHANNEL_ACCESS_TOKEN = 'vlm/75CNEZV5icmrxFKKHgkc49eaxFkOXdV0SIIII2kjo8g6RyE4JwBZdOG+oYltrv0yASUAJAXs/INGTtjuSJulsX0GggA6nZZrG9LhyvWzEvcXjLbmgrbtEaJtGEpoPfPFw63sffUVj0qh2waeTAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '3dd899ef453849d79d9e92cd03a7e9af'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 測試頁面
@app.route("/")
def home():
    return "Flask LINE Bot is running!"

# LINE Webhook endpoint
@app.route("/callback", methods=['POST', 'GET', 'OPTIONS'])
def callback():
    # 如果是非 POST，直接回 200，避免 405 Method Not Allowed
    if request.method != 'POST':
        return 'OK', 200

    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK', 200

# 回覆文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    reply = f"你說了：{user_text}"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    # 允許外部訪問，Cloudflare Tunnel 需要
    app.run(host="0.0.0.0", port=5000)
