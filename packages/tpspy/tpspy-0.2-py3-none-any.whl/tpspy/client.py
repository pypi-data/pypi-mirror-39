# -*- coding: utf-8 -*-

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
import requests
from tpspy.auth.authutil import AuthUtil


class Client(object):
    user_api = "API"

    class MessageChannel(object):
        # 企业微信-群聊
        WECHAT_WORK_GROUP_CHAT_TEXT = "WECHAT_WORK_GROUP_CHAT_TEXT"
        # 企业微信-群聊
        WECHAT_WORK_GROUP_CHAT_NEWS = "WECHAT_WORK_GROUP_CHAT_NEWS"
        # 企业微信-应用推送
        WECHAT_WORK_APP_PUSH_TEXT = "WECHAT_WORK_APP_PUSH_TEXT"
        # 企业微信-应用推送
        WECHAT_WORK_APP_PUSH_NEWS = "WECHAT_WORK_APP_PUSH_NEWS"
        # 企业微信-群聊机器人
        WECHAT_WORK_GROUP_ROBOT_TEXT = "WECHAT_WORK_GROUP_ROBOT_TEXT"
        # 企业微信-群聊机器人
        WECHAT_WORK_GROUP_ROBOT_MD = "WECHAT_WORK_GROUP_ROBOT_MD"

        # 微信推送
        WECHAT = "WECHAT"

        # 邮件, 自动区分内部和外部邮件
        MAIL = "MAIL"

        # 短信
        SMS = "SMS"

    def __init__(self, sys_id, sys_secret, tps_base_url=None):
        self.tps_base_url = tps_base_url or "https://tps.sngapm.qq.com/"
        self.sys_id = sys_id
        self.sys_secret = sys_secret
        self.auth = AuthUtil()
        self.auth.set_secret(self.sys_secret)

    @property
    def token(self):
        return self.auth.gen_token(user_id="API")

    @property
    def auth_headers(self):
        return {
            "SYS-ID": self.sys_id,
            "TOKEN": self.token,
        }

    def api_tapd_tencent(self, method, path, params, api_user=None, api_pwd=None):
        url = urljoin(self.tps_base_url, "api/v1/apibridge/tapdTencent")
        resp = requests.get(url, json=dict(
            method=method,
            path=path,
            params=params,
            api_user=api_user,
            api_pwd=api_pwd,
        ), headers=self.auth_headers)
        return resp.json()

    def message_send(self, msg_type, to, content):
        url = urljoin(self.tps_base_url, "api/v1/message/send")
        resp = requests.get(url, json=dict(
            type=msg_type,
            to=to,
            content=content,
        ), headers=self.auth_headers)
        return resp.json()


if __name__ == "__main__":
    pass
