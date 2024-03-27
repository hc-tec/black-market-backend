import re
from rest_framework.views import APIView
from utils.response import validData
from utils import statusCode

import qianfan


def extractTagsFromAIText(text):
    # 定义包含标签的文本
    # 使用正则表达式提取所有标签
    # 这里的模式意味着寻找所有的“数字. 标签名称”格式的文本
    tags = re.findall(r'\d+\.\s*(.+)', text)

    # 输出提取到的标签列表
    print(tags)

    return tags


chat_comp = qianfan.ChatCompletion()


class SuggestTagsView(APIView):
    @validData(statusCode.SuggestTags)
    def get(self, request, *args, **kwargs):

        tag = request.query_params["tag"]

        # 调用默认模型，即 ERNIE-Bot-turbo
        resp = chat_comp.do(model="ERNIE-3.5-4K-0205", messages=[{
            "role": "user",
            "content": f"你是一位电商运营专家，现在请为校园二手商城中的‘{tag}’商品打上合适的标签。标签需要简洁明了，能准确反映商品的主要特征或卖点。请注意，你的回答仅包含给出的标签列表，无需其他任何说明与解释，不需要任何其他废话。"
        }])

        text = resp.body.get("result")
        if text:
            tags = extractTagsFromAIText(text)
            return {"data": tags}

        return resp
