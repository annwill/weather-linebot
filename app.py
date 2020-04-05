import requests
import json

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app=Flask(__name__)
line_bot_api=LineBotApi('d8EVm9g06hLy8xfd75K/KW1U1oFbLDRyZLSKgRKljXcpLMTheWRFs+m8hEj7ZvVHHE5jvzADHkZPjw4HB+iayP/OlHG2VpX6JPAx+m5mN3A4KOx3g/AvmOs8rwQob/9hQuuAeSn601XQJOh972r2kwdB04t89/1O/w1cDnyilFU=')
handler=WebhookHandler('9639daf138a2c632bac6d07fedbd522a')

def getWeather(county):
    
    api_link="https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-6B1C5648-8E38-4CB6-A534-0F5149345603&format=JSON"
    r=requests.get(api_link)
    dataload=json.loads(r.text)

    index=-1
    title=['天氣狀況','最高溫','最低溫','舒適度','降雨機率']

    datas=dataload['cwbopendata']['dataset']['location']
    for i in range(len(datas)):
        if datas[i]['locationName']==county.replace('台','臺'):
            index=i
            break
    ans=''

    if index !=-1:
        ans=datas[index]['locationName']
        for j in range(5):
            ans +='\n' +title[j]+':'+datas[index]['weatherElement'][j]['time'][0]['parameter']['parameterName']  
    else:
        ans='沒有相關縣市資料'

    return ans    



#heroku 
# app=Flask(__name__)
# line_bot_api=LineBotApi('5VF1kWPoe9rqLdKipMbrbO5MFoR7HEbmOL4nsVAODMEp/FNG9xxX22BjS9dTOCDRtRH7xtsoaUTwQUA+1RF/yr+X6ST9NDnFVPpUU9pKLeAOolmdCm29knDqPf1t4F5UgLl4Z0CqxThw/0EVbXGBEwdB04t89/1O/w1cDnyilFU=')
# handler=WebhookHandler('feec997a0a3d9cf6d25c838c4fd648b3')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=getWeather(text))
    )

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.run()