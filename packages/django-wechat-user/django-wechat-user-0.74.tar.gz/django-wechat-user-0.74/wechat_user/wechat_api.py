import base64
import json
import logging

import requests
from Crypto.Cipher import AES
from django.conf import settings
from rest_framework.exceptions import APIException

# logger
logger = logging.getLogger(__name__)


def exchange_access_token(code):
    url = (
        "https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code"
    ).format(settings.WECHAT_APPID, settings.WECHAT_APPSECRET, code)
    
    # send request
    response = requests.get(url)
    response.encoding = "utf-8"
    data = response.json()
    # check error
    if "errcode" in data:
        error_msg = "{}({})".format(data["errmsg"], data["errcode"])
        logger.error(error_msg)
        raise APIException(error_msg)
    return data["openid"], data["access_token"], data["refresh_token"], data["expire_in"]


def fetch_user_info(access_token, openid):
    url = (
        "https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN"
    ).format(access_token, openid)
    response = requests.get(url)
    response.encoding = "utf-8"
    data = response.json()
    # check error
    if "errcode" in data:
        error_msg = "{}({})".format(data["errmsg"], data["errcode"])
        logger.error(error_msg)
        raise APIException(error_msg)
    return data


def exchange_session_key(code):
    url = (
        "https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code"
    ).format(settings.WECHAT_APPID, settings.WECHAT_APPSECRET, code)

    response = requests.get(url)
    response.encoding = "utf-8"
    data = response.json()
    if "errcode" in data and data["errcode"] != 0:
        error_msg = "{}({})".format(data["errmsg"], data["errcode"])
        logger.error(error_msg)
        raise APIException(error_msg)
    return data["openid"], data["session_key"], data.get('unionid', None)


def unpad(s):
    return s[:-ord(s[len(s)-1:])]


def decrypt_user_info(session_key, encryptedData, iv):
    cipher = AES.new(base64.b64decode(session_key), AES.MODE_CBC, base64.b64decode(iv))
    decrypted = json.loads(unpad(cipher.decrypt(base64.b64decode(encryptedData))))
    if decrypted['watermark']['appid'] != settings.WECHAT_APPID:
        raise Exception('Invalid Buffer')
    return decrypted
