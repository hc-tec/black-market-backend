
from typing import Callable, List
from datetime import datetime, timedelta

from apps.users.models import (Thread, Topic,
                               AUDIT_STATUS_ENUM)
from django.db.models.query import QuerySet

from .singleton import Singleton

class BaseHotSingleton(Singleton):

    def __init__(self, *args, **kwargs):
        self._hot_obj = None
        self.args = args
        self.kwargs = kwargs

    def get_all(self, *args, **kwargs) -> QuerySet:
        if self._hot_obj is None:
            self.update()
        #print('BaseHotSingleton', self._hot_obj)
        return self._hot_obj

    def update(self):
        self._hot_obj = self._get_all()

    def get_first(self, *args, **kwargs) -> any:
        res = self.get_all(*args, **kwargs)
        return res.first() if res else None


    def _get_all(self) -> QuerySet:
        filter_obj = self._get_filter_obj()
        return self._order(filter_obj)

    def _get_filter_obj(self) -> QuerySet: ...

    def _order(self, *args, **kwargs) -> QuerySet: ...

class HotThreadSingleton(BaseHotSingleton):

    def __init__(self):
        super().__init__(self)
        self._hot_obj = {}


    def get_all(self, school_zone) -> QuerySet:
        self.school_zone = school_zone
        if self._hot_obj.get(self.school_zone) is None:
            self.update()
        #print('HotThreadSingleton', self._hot_obj)
        return self._hot_obj[self.school_zone]

    def update(self):
        self._hot_obj[self.school_zone] = self._get_all()


    def _get_filter_obj(self) -> QuerySet:
        # 获取最近一星期以内的帖子
        return Thread.objects.filter(
            flag=AUDIT_STATUS_ENUM.AUDIT_PASS,
            author_info__school_zone=self.school_zone,
            thread_time__gt=datetime.now() - timedelta(days=7)
        )

    def _order(self, threads):
        threads = sorted(threads, key=thread_order_func)
        return Thread.objects.filter(pk__in=[x.pk for x in threads])

class HotTopicThreadSingleton(BaseHotSingleton):

    def __init__(self):
        super().__init__(self)
        self._hot_obj = {}


    def get_all(self, topic, school_zone) -> QuerySet:
        self.topic = topic
        self.school_zone = school_zone
        topic_content = self.topic.topic_content
        if self._hot_obj.get(self.school_zone) is None:
            self._hot_obj[self.school_zone] = {}
        school_zone_filter = self._hot_obj[self.school_zone]
        if school_zone_filter.get(topic_content) is None:
            self.update()
        #print('HotTopicThreadSingleton', self._hot_obj)
        return self._hot_obj[self.school_zone][topic_content]

    def update(self):
        self._hot_obj[self.school_zone][self.topic.topic_content] = self._get_all()

    def _get_filter_obj(self):
        return self.topic.thread_topic_set.filter(
            flag=AUDIT_STATUS_ENUM.AUDIT_PASS,
            author_info__school_zone=self.school_zone,
            thread_time__gt=datetime.now() - timedelta(days=7)
        )

    def _order(self, threads):
        threads = sorted(threads, key=thread_order_func)
        return Thread.objects.filter(pk__in=[x.pk for x in threads])

class HotTopicSingleton(HotThreadSingleton):

    def _get_filter_obj(self) -> QuerySet:
        return Topic.objects.all()

    def _order(self, topics) -> QuerySet:
        topic_filter = []
        for topic in topics:
            threads = topic.thread_topic_set.filter(
                        flag=AUDIT_STATUS_ENUM.AUDIT_PASS,
                        author_info__school_zone=self.school_zone,
                    )
            topic_filter.append(
                (topic, threads)
            )
        topics = sorted(topic_filter, key=topic_order_func)
        return Topic.objects.filter(pk__in=[x[0].pk for x in topics])

def thread_order_func(thread):
    like_num = thread.thread_appreciate
    comment_num = thread.thread_info_set.all().count()
    time = (datetime.today() - thread.thread_time.replace(tzinfo=None)).days
    score = thread_calc_score(like_num, comment_num, time)
    return score

def thread_calc_score(like_num: int, comment_num: int, time: int):
    '''

    :param like_num: 点赞数量
    :param comment_num: 评论数量
    :param time: 发布时间距现在的天数
    算法 =
        4 + like*2 + comment*5
        ----------------------
               time + 4
    :return:
    '''
    return (8 + like_num*2 + comment_num*5) / (time + 4)


def topic_order_func(topic_filter):
    # 话题分数为其下所有帖子与关注量的加权和
    threads_score = 0
    threads = topic_filter[1]
    for thread in threads:
        like_num = thread.thread_appreciate
        comment_num = thread.thread_info_set.all().count()
        time = (datetime.today() - thread.thread_time.replace(tzinfo=None)).days
        threads_score += thread_calc_score(like_num, comment_num, time)
    threads_score /= threads.count() or 1
    focus_num = topic_filter[0].topic_focus.all().count()
    score = topic_calc_score(threads_score, focus_num)
    return score

def topic_calc_score(threads_score, focus_num):
    '''
    话题分数
    :param threads_score: 帖子加权和
    :param focus_num: 关注量
    :return:
    算法：
        threads_score*0.6 + focus_num*0.4 + 1
    '''
    return threads_score*0.6 + focus_num*0.4 + 1
