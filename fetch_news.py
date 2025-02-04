# 示例代码框架（需根据API文档完善）
import requests
import schedule
import time
from datetime import datetime, timedelta
from news_analysis import save_to_es


# 示例：抓取微博热搜并结构化存储
def fetch_weibo_hot_news():
    url = "https://weibo.com/ajax/side/hotSearch"
    response = requests.get(url).json()
    hot_list = []
    for item in response["data"]["realtime"]:
        hot_list.append({
            "keyword": item["word"],
            "rank": item["rank"],
            "category": item.get("category", "社会"),  # 分类（如科技、财经）
            "timestamp": datetime.now().isoformat(),  # 时间戳
            "source": "微博热搜"
        })
    return hot_list

# 1. 定义数据源（以微博热搜和NewsAPI为例）
def fetch_weibo_hot():
    url = "https://weibo.com/ajax/side/hotSearch"
    response = requests.get(url).json()
    return [item["word"] for item in response["data"]["realtime"]]

def fetch_newsapi():
    api_key = "YOUR_API_KEY"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url).json()
    return [article["title"] for article in response["articles"]]

# 2. 数据清洗与去重
def clean_data(data_list):
    # 去除广告、重复词、非24小时内内容（需结合时间戳）
    return list(set(data_list))

# 3. 生成报告
def generate_report(content):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(f"output/news_report_{today}.md", "w", encoding="utf-8") as f:
        f.write(f"## 每日热点报告（{today}）\n\n")
        f.write("### 国内热点\n- " + "\n- ".join(content["domestic"]))
        # f.write("\n\n### 国际热点\n- " + "\n- ".join(content["international"]))

# 4. 主任务
def daily_task():
    domestic_news = fetch_weibo_hot()
    # international_news = fetch_newsapi()
    cleaned_data = {
        "domestic": clean_data(domestic_news),
        # "international": clean_data(international_news)
    }
    generate_report(cleaned_data)
    # 写入es
    save_to_es(cleaned_data)
    # 可选：发送邮件（使用smtplib）

# # 5. 定时任务（每天6点执行）
# schedule.every().day.at("06:00").do(daily_task)

# while True:
#     schedule.run_pending()
#     time.sleep(60)
    
# 单次运行测试
# daily_task()
cleaned_data = {'domestic': ['DeepSeek回答如何过好这一生', '门牙上的豁口真是嗑瓜子嗑出来的吗', '勇士有意集齐詹杜库', '小蛇糕', '库班对东契奇交易感到困惑', '正月初七为啥称为人日', '亚冬会火炬传递圆满结束', '小S曾在姐姐去世前几小时和妈妈跳舞', '吴京 流浪地球3', '射雕疑似被恶意打分', '闭眼除夕睁眼初七', '哪吒2进影史前10', '林志玲发文悼念大S', '泽连斯基称不知道美国给的钱去了哪里', '石矶娘娘心态', '怎么假期就最后一天了', '明天上班', '哪吒3', '直播春运返程高峰', '哪吒之魔童闹海票房破42亿', '吴佩慈受访时泣不成声', '具俊晔崩溃', '饺子导演 你别累着但也别闲着', '小S两个女儿回台', '奥司他韦不能乱吃', '饺子导演手绘无表情哪吒', '多地返程遇雨雪', '徐妈妈希望外界给予徐家人一点时间', '卧室再小也能做个衣帽间', '美国将再次退出联合国人权理事会', '女子4次陪老公跨越260公里悼念亡妻', '藕饼', '美将 停止资助联合国巴勒斯坦救助机构', '小米集团市值突破万亿港元', '射雕口碑', '蛋清羊尾是中国人自己的泡芙', '王楚钦说低潮期一度崩溃', '返程开车牢记这几个细节', '人心中的成见是一座大山 那很漂亮了', '被诬陷偷拍男子结婚了', '学医的老公回村过年邻居8点排队看病', '光线要拍敖丙传', '流浪地球给哪吒做的贺图', 'DeepSeek现象背后', '最后一天假期怎么过', '厄瓜多尔对墨西哥加征27%的关税', '遇见熙媛5363 天', '流感合并肺炎有这些症状', '多平台宣布上线DeepSeek大模型', '大S就医时或已错过治疗黄金期']}
save_to_es(cleaned_data)