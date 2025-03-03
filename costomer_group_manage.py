import os
import requests
import json


def get_costomer_group_list(access_token, userid):
    """获取客户群列表"""

    # 获取客户群列表
    url = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/list?access_token={access_token}"
    data = {
        "status_filter": 0,
        "owner_filter": {
            "userid_list": [userid]
        },
        "cursor" : "",
        "limit" : 10
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(response.json())


def get_costomer_group_details(access_token, chatid):
    """获取客户群详情"""

    url = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/get?access_token={access_token}"
    data = {
        "chat_id": chatid,
        "need_name": 1
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(response.json())

