# -*- coding: utf-8 -*-


import os
from tpspy.client import Client


TPS_SYS_ID = os.getenv("TPS_SYS_ID", '')
TPS_SYS_SECRET = os.getenv("TPS_SYS_SECRET", '')

client = Client(sys_id=TPS_SYS_ID, sys_secret=TPS_SYS_SECRET, tps_base_url="http://127.0.0.1:30180/")
# client = Client(sys_id=TPS_SYS_ID, sys_secret=TPS_SYS_SECRET, tps_base_url="https://tps-test.sngapm.qq.com/")


def test_api():
    r = client.api_tapd_tencent(method="GET", path="bugs.json", params={
        "workspace_id": 10066461,
        "title": "QAPM"
    })
    print(r)
    assert isinstance(r, dict) and r.get("code") == 10000


def test_message():
    to = "kangtian"
    content = dict(
        title="test",
        body="""你的快递已到，请携带工卡前往邮件中心领取。\n出发前可查看 http://work.weixin.qq.com 邮件中心视频实况，聪明避开排队。"""
    )

    # r = client.message_send(msg_type=client.MessageChannel.WECHAT, to=to, content=content)
    # print("WECHAT, ", r)

    # r = client.message_send(msg_type=client.MessageChannel.MAIL, to=to, content=content)
    # print("MAIL, ", r)

    # r = client.message_send(msg_type=client.MessageChannel.WECHAT_WORK_APP_PUSH_TEXT, to=to, content=content)
    # print("WECHAT_WORK_APP_PUSH_TEXT, ", r)

    msg_types = ",".join([client.MessageChannel.WECHAT, client.MessageChannel.MAIL, client.MessageChannel.WECHAT_WORK_APP_PUSH_TEXT])
    r = client.message_send(msg_type=msg_types, to=to, content=content)
    print("MULTICHANNEL MSG, ", r)


if __name__ == "__main__":
    # test_api()
    test_message()
