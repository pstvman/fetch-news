import os
import requests
import json
import time
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# 企业微信参数
CORPID = os.getenv('CORPID')          # 企业ID
CORPSECRET = os.getenv('CORPSECRET')  # 应用Secret
AGENTID = os.getenv('AGENTID')        # 应用AgentId

class AccessTokenManager:
    def __init__(self):
        # self._access_token = None
        # self._expires_at = 0  # token过期时间戳
        # 在当前目录创建缓存文件
        self.cache_file = Path(".cache")
    
    def get_access_token(self):
        """获取Access Token，如果已缓存且未过期则直接返回"""
        # 尝试从缓存文件读取
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r") as f:
                    cache = json.load(f)
                    expires_at = cache.get("expires_at", 0)
                    token = cache.get("access_token")

                    # 提前5分钟刷新token，避免临界点失效
                    if token and time.time() < (expires_at - 300):
                        print("缓存token: ", token)
                        return token
            except Exception as e:
                print(f"读取缓存文件失败：{e}")
        
        # Token不存在或已过期，重新获取
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORPID}&corpsecret={CORPSECRET}"
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("errcode") == 0:
                token = result.get("access_token")
                expires_at = time.time() + result.get("expires_in", 7200)

                # 保存到缓存文件
                try:
                    cache_data = {
                        "access_token": token,
                        "expires_at": expires_at,
                        "update_time": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    with open(self.cache_file, "w") as f:
                        json.dump(cache_data, f)
                except Exception as e:
                    print("写入缓存文件失败：{e}")
                
                return token
            else:
                raise Exception(f"获取Token失败：{result.get('errmsg')}")
        else:
            raise Exception(f"请求失败，状态码：{response.status_code}")

# 创建全局的token管理器实例
token_manager = AccessTokenManager()

# 修改原有的get_access_token函数
def get_access_token():
    """获取Access Token的包装函数"""
    return token_manager.get_access_token()

def send_news():
    """发送早新闻"""
    try:
        # 1. 获取最新的Access Token
        access_token = get_access_token()
        
        # 2. 调用你的资讯接口获取新闻内容
        news = "今日早新闻：\n1. 新闻内容1\n2. 新闻内容2\n3. 新闻内容3"
        
        # 3. 发送消息（以文本消息为例）
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        # url = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_msg_template?access_token=ACCESS_TOKEN"
        data = {
            "touser": "@all",  # 发送给所有人（或指定UserID）
            "msgtype": "text",
            "agentid": AGENTID,
            "text": {"content": news}
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        
        if response.json().get("errcode") == 0:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} 消息发送成功！")
        else:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} 消息发送失败：{response.json()}")
    
    except Exception as e:
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} 发生错误：{str(e)}")

# 执行发送
if __name__ == "__main__":
    send_news()