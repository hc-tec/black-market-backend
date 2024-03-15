from django.db import models
from .userinfoModel import UserInfo
from .goodsModel import Goods
from .threadModel import Thread
from .threadCommentModel import ThreadComment


class BasicReport(models.Model):
    class Meta:
        abstract = True

    REASON = (
        (1, "违法违规"),
        (2, "色情"),
        (3, "低俗"),
        (4, "赌博诈骗"),
        (5, "人身攻击"),
        (6, "侵犯隐私"),
        (7, "垃圾广告"),
        (8, "青少年不良信息"),
        (9, "标题党/封面党"),
        (10, "其它")
    )
    whistleblower = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="举报人")
    reason = models.IntegerField(choices=REASON, verbose_name="举报原因", default=10)
    other_reason = models.TextField(verbose_name="其它原因", null=True, blank=True)


class GoodReport(BasicReport):
    class Meta:
        app_label = 'users'
        verbose_name = "商品举报信息"
        verbose_name_plural = verbose_name
    related_good = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name="report_good_set",
                                     verbose_name="被举报的商品")

    def __str__(self):
        return self.related_good.goods_title


class ThreadReport(BasicReport):
    class Meta:
        app_label = 'users'
        verbose_name = "帖子举报信息"
        verbose_name_plural = verbose_name
    related_thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="report_thread_set",
                                       verbose_name="被举报的帖子")

    def __str__(self):
        return self.related_thread.thread_info


class CommentReport(BasicReport):
    class Meta:
        app_label = 'users'
        verbose_name = "评论举报信息"
        verbose_name_plural = verbose_name
    related_comment = models.ForeignKey(ThreadComment, on_delete=models.CASCADE, related_name="report_comment_set",
                                        verbose_name="被举报的评论")

    def __str__(self):
        return self.related_comment.comment_content