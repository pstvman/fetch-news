import os
import requests


def get_costomer_list(access_token, userid):
    """获取客户(外部联系人)列表"""

    url = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/list?access_token={access_token}&userid={userid}"
    
    response = requests.get(url)
    print(response.json())
    ret = response.json().get("external_userid")
    if ret == []:
        print("获取客户列表为空")
    else:
        return ret


def get_costomer_details(access_token, external_userid):
    """获取客户（外部联系人）的详细信息"""

    url = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get?access_token={access_token}&external_userid={external_userid}"

    response = requests.get(url)
    # print(response.json())
    # print(response.json().get("external_contact"))

    return response.json().get("external_contact")

