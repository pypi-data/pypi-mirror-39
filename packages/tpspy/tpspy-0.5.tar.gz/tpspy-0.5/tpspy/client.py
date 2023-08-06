# -*- coding: utf-8 -*-

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
import requests
import json
from tpspy.auth.authutil import AuthUtil


class Client(object):
    user_api = "API"

    class MessageChannel(object):
        # 企业微信-群聊-文本
        WECHAT_WORK_GROUP_CHAT_TEXT = "WECHAT_WORK_GROUP_CHAT_TEXT"
        # 企业微信-群聊-图文
        WECHAT_WORK_GROUP_CHAT_NEWS = "WECHAT_WORK_GROUP_CHAT_NEWS"
        # 企业微信-群聊-卡片
        WECHAT_WORK_GROUP_CHAT_CARD = "WECHAT_WORK_GROUP_CHAT_CARD"
        # 企业微信-应用推送-文本
        WECHAT_WORK_APP_PUSH_TEXT = "WECHAT_WORK_APP_PUSH_TEXT"
        # 企业微信-应用推送-图文
        WECHAT_WORK_APP_PUSH_NEWS = "WECHAT_WORK_APP_PUSH_NEWS"
        # 企业微信-应用推送-卡片
        WECHAT_WORK_APP_PUSH_CARD = "WECHAT_WORK_APP_PUSH_CARD"
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
        self.tps_base_url = tps_base_url or "https://tencent.qq.com/"
        self.sys_id = sys_id
        self.sys_secret = sys_secret
        self.auth = AuthUtil()
        self.auth.set_secret(self.sys_secret)

    def set_tps_base_url(self, tps_base_url):
        self.tps_base_url = tps_base_url

    @property
    def token(self):
        return self.auth.gen_token(user_id="API")

    @property
    def auth_headers(self):
        return {
            "SYS-ID": self.sys_id,
            "TOKEN": self.token,
        }

    @property
    def post_headers(self):
        headers = {
            "Content-Type": "application/json"
        }
        headers.update(self.auth_headers)
        return headers

    @property
    def get_headers(self):
        headers = {
            "Content-Type": "application/json"
        }
        headers.update(self.auth_headers)
        return headers

    @staticmethod
    def resp_get_json(resp):
        try:
            return resp.json()
        except:
            raise Exception("resp is not json: ", resp.status_code, resp.text)

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
        import json
        print(json.dumps(dict(
            type=msg_type,
            to=to,
            content=content,
        )))
        resp = requests.get(url, json=dict(
            type=msg_type,
            to=to,
            content=content,
        ), headers=self.auth_headers)
        return resp.json()

    def message_chat_create(self, name, owner, user_list):
        url = urljoin(self.tps_base_url, "api/v1/message/chat")
        print(json.dumps(dict(
            name=name,
            owner=owner,
            user_list=user_list,
        )))
        resp = requests.post(url, json=dict(
            name=name,
            owner=owner,
            user_list=user_list,
        ), headers=self.auth_headers)
        return resp.json()

    def message_chat_info(self, chat_id=''):
        url = urljoin(self.tps_base_url, "api/v1/message/chat")
        print(json.dumps(dict(
            chat_id=chat_id
        )))
        resp = requests.get(url, json=dict(
            chat_id=chat_id
        ), headers=self.auth_headers)
        return resp.json()

    def metrics_resource_flow_upload(self, data):
        url = urljoin(self.tps_base_url, "api/v1/metrics/resource_flow/upload")

        resp = requests.post(url, data=json.dumps(dict(
            data=data
        )), headers=self.post_headers)
        return self.resp_get_json(resp)

    def metrics_resource_flow_get(self, params):
        url = urljoin(self.tps_base_url, "api/v1/metrics/resource_flow/get")

        resp = requests.get(url, data=json.dumps(params), headers=self.get_headers)
        return self.resp_get_json(resp)


if __name__ == "__main__":
    pass
