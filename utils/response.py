import json

from django.http import JsonResponse

class Response:
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg


class Error(Response):

    def __init__(self, code: int, msg: str):
        super().__init__(code, msg)


class Success(Response):

    def __init__(self, code: int, msg: str):
        super().__init__(code, msg)

class Status:
    Error: Error = None
    Success: Success = None

def validData(Status):
    def inner(func):
        def isValid(cls, *args, **kwargs):
            import copy
            # 深拷贝，防止损坏原字典
            ret = copy.deepcopy(Status.Success.__dict__)
            try:
                # 断言，判断是否存在字段为空情况
                # 要求返回 data 域数据，而非 Response
                data = func(cls, *args, **kwargs)
                if data:
                    ret.update(data)
            except Exception as e:
                ret.update(Status.Error.__dict__)
                ret['error'] = str(e)
                print('[error]: ', str(e))
            # return json.dumps(ret, ensure_ascii=False)
            return JsonResponse(ret, json_dumps_params={"ensure_ascii": False})

        return isValid

    return inner
