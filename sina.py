#coding:utf8
from weibo import APIClient
import webbrowser

APP_KEY="2952971815"
APP_SECRET="bc8608ca6d902e2102f8781ae91d8caf"
CALLBACK_URL="https://api.weibo.com/oauth2/default.html"

api=APIClient(app_key=APP_KEY,app_secret=APP_SECRET,
        redirect_uri=CALLBACK_URL)
authorize_url=api.get_authorize_url(redirect_url=CALLBACK_URL)
print authorize_url
code=raw_input("请输入code:").strip()

r=api.request_access_token(code)
access_token=r.access_token
expires_in=r.expires_in

api.set_access_token(access_token,expires_in)

print api.statuses.public_timeline.get()
