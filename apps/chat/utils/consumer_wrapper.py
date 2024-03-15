
import json

'''
    心跳检测
'''
def heartbeat():
    def inner(func):
        async def check(cls, *args, **kwargs):
            data = kwargs["text_data"]
            if data == '0':
                return
            await func(cls, *args, **kwargs)
        return check
    return inner

'''
    好友之间的 socket 关联
'''
def chatCreate():
    def inner(func):
        async def isValid(cls, *args, **kwargs):
            '''
                {
                    type: connect,
                    chat_id: 1-2,
                }
            '''
            data = kwargs["text_data"]
            try:
                data = json.loads(data.replace('\n',''))
                _type = data.get("type")
                if _type and _type == "connect":
                    # 获取到用房间号
                    chat_id = data["chat_id"]
                    await cls.channel_layer.group_add(
                        chat_id,
                        cls.channel_name
                    )
                    return
            except json.decoder.JSONDecodeError:
                return
            await func(cls, *args, **kwargs)
        return isValid
    return inner
