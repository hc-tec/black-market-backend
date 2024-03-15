

from typing import Callable, List
from datetime import datetime, timedelta

from django.db.models.signals import pre_delete
from django.dispatch import receiver


# 将文件删除
# @receiver(pre_delete, sender=Image)
# def image_delete(instance, **kwargs):
#     """
#
#     :param sender: 文件字段所在的类
#     :param instance: 模型对象
#     :param kwargs:
#     :return:
#     """
#     instance.images.delete(False)

class Listener:

    __listeners: List[Callable] = []

    @classmethod
    def listen(self, listener: Callable):
        self.__listeners.append(listener)

    @classmethod
    def trigger(self, data):
        for listener in self.__listeners:
            listener(data)

def generate_chat_id(user_id: int, friend_id: int) -> str:
    return "-".join(map(str, sorted([user_id, friend_id])))

def correct_time(time: datetime) -> datetime:
    return time + timedelta(hours=8)

def format_time(time: datetime) ->str:
    return correct_time(time)\
        .strftime("%Y-%m-%d %H:%M:%S")

