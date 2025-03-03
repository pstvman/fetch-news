import requests
import json
import time

# 创建群发消息（需群主确认）
def push_costomer_group_message(access_token, chatid, userid):
    """
    群发消息可以是企业统一创建发送的，也可以是成员自己创建发送的；
    每位客户/每个客户群每月最多可接收条数为当月天数，超过接收上限的客户/客户群将无法再收到群发消息。
    """

    url = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_msg_template?access_token={access_token}"
    data = {
        "chat_type": "group",
        "external_userid": [
            "woAJ2GCAAAXtWyujaWJHDDGi0mACAAAA",
            "wmqfasd1e1927831123109rBAAAA"
        ],
        "chat_id_list": chatid,
        "sender": userid,
        "allow_select": False,
        "text": {
            "content": "这是一条测试消息"
        },
        "attachments": [{
            "msgtype": "link",
            "link": {
                "title": "消息标题",
                "picurl": "https://example.pic.com/path",
                "desc": "消息描述",
                "url": "https://example.link.com/path"
            }
        } ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(response.json())


# 提醒成员群发确认
def remind_owner_push(access_token, no_send_msgid):
    """
    企业和第三方应用可调用此接口，重新触发群发通知，提醒成员完成群发任务，24小时内每个群发最多触发三次提醒。
    """
    url = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/remind_groupmsg_send?access_token={access_token}"

    data = {
        "msgid": no_send_msgid,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(response.json())


def time2timestamp(time_data):
    # 将日期转换为时间戳（秒级）
    return int(time.mktime(time_data))


def get_group_send_record(access_token, userid, start_date, end_date):
    """
    获取所有群发记录
    """

    url = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_groupmsg_list_v2?access_token={access_token}"

    # 定义起始日期和结束日期
    start_date = (2025, 3, 3, 0, 0, 0, 0, 0, 0)
    end_date = (2025, 3, 3, 23, 59, 59, 0, 0, 0)

    data = {
        "chat_type":"group",
        "start_time": time2timestamp(start_date),
        "end_time": time2timestamp(end_date),
        "creator": userid,
        "filter_type":2,
        "limit":50,
        "cursor":""
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(response.json())


def cancal_group_push(access_token, msgid):
    """
    停止无需成员继续发送的企业群发
    """

    url = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/cancel_groupmsg_send?access_token={access_token}"

    data = {
        "msgid": msgid,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(response.json())
