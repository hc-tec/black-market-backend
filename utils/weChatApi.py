import requests
import json


def get_openid(js_code=None):
    try:
        params = {"appId": "wxc15e6f87b7fabe0b", "secret": "4411d660429b44c879627c49e8a837bf", "js_code": js_code,
                  "grant_type": "authorization_code"}
        r = requests.get("https://api.weixin.qq.com/sns/jscode2session", params=params, timeout=60)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.json()
        # return json.dumps(r.text, ensure_ascii=False)
    except Exception as e:
        raise Exception("微信接口调用失败")


# if __name__ == "__main__":
#     a = get_openid("1234556")
#     print(a, type(a))
