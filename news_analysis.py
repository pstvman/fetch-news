from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import logging

# 配置日志记录
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('elasticsearch')
logger.setLevel(logging.DEBUG)

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=("elastic", "k8=SQl_q_KJ6Cprto_Mv"),
    # scheme="https",
    # verify_certs=False # 如果是自签名证书，临时禁用验证（生产环境不建议）
    )
if es.ping():
    print("成功连接到 Elasticsearch！")
else:
    print("连接失败，请检查配置。")

def save_to_es(data_list, news_keywords):
    print("\n写入es前打印：", data_list, "\n")
    actions = []
    for data in data_list['weibo']:
        print(data)
        action = {
            "_index": news_keywords,  # 索引名称
            "_source": {
                "word": data["word"],
                "hot_value": data["hot_value"],
                "timestamp": data["timestamp"]
            }
        }
        actions.append(action)
    print("actions:", actions)
    # 批量写入（高性能）
    # try:
    #     bulk(es, actions)
    #     print("数据写入成功！")
    # except Exception as e:
    #     print(f"写入失败：{e}")
    try:
        # 设置 stats_only=False 以返回详细错误信息
        success_count, errors = bulk(es, actions, stats_only=False)
        print(f"成功写入 {success_count} 条数据")
        
        # 输出错误详情
        if errors:
            print("\n写入失败的文档及原因：")
            for error in errors:
                # 错误信息通常位于 ['index']['error']
                err_reason = error["index"]["error"]
                doc_id = error["index"]["_id"]  # 如果未指定 _id，可能为 None
                doc_data = actions[error["index"]["_id"]]["_source"]  # 关联原始数据
                print(f"文档 ID {doc_id} 错误：{err_reason}")
                print(f"失败数据内容：{doc_data}\n")
    except Exception as e:
        print(f"批量写入异常：{e}")


# # 测试数据
# sample_data = [
#     {"title": "新闻1", "keywords": ["科技", "AI"]},
#     {"title": "新闻2", "keywords": ["经济", "金融"]}
# ]

# save_to_es(sample_data)