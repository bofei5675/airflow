from past.builtins import basestring

import importlib
import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate

from airflow import configuration
from airflow.exceptions import AirflowConfigException
from airflow.utils.log.logging_mixin import LoggingMixin
import requests


APP_ID = 'cli_9dd0c7826ea0d101'
APP_SCECRET = 'DD1ils7jCDaUwUbRBNNRybuuQVdJ87v2'
BOT_AUTH_API = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
SENDER_API = 'https://open.feishu.cn/open-apis/message/v3/send/'
def get_token(bot_auth_api,app_id,app_secret):
    params={'app_id':app_id,'app_secret':app_secret}
    user_token_reponse = requests.get(bot_auth_api,params=params)
    user_token_reponse = user_token_reponse.json()
    tenant_access_token = user_token_reponse['tenant_access_token']
    return tenant_access_token
def larkbot_msg_sender(msg):
    app_id = configuration.conf.get('lark','APP_ID')
    app_secret = configuration.conf.get('lark','APP_SECRET')
    bot_auth_api = configuration.conf.get('lark','BOT_AUTH_API')
    sender_api = configuration.conf.get('lark','SENDER_API')

    tenant_access_token = get_token(bot_auth_api,app_id,app_secret)
    header = {"Authorization": "Bearer " + str(tenant_access_token), "Content-Type": "application/json"}
    data = {
        "open_chat_id": "6727899551597854984",
        "msg_type": "text",
        "content": {
            "text": msg
        }
    }
    code = requests.post(sender_api, json = data, headers = header)

def larkbot_backend(msg):
    path, attr = configuration.conf.get('lark', 'LARKBOT_BACKEND')
    # 在上下文中注册这个机器人 函数
    module = importlib.import_module(path)
    # backend is the function of larkbot_msg_sender
    backend = getattr(module, attr)
    return backend(msg)


