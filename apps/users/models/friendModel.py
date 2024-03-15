
from django.db import models

from .userinfoModel import UserInfo

class FRIEND_STATUS:
    APPLYING = 1
    APPLY_PASS = 2
    APPLY_DENY = 3

class Friend(models.Model):

    FRIEND_STATUS = (
        (FRIEND_STATUS.APPLYING, "好友申请中"),
        (FRIEND_STATUS.APPLY_PASS, "正式好友"),
        (FRIEND_STATUS.APPLY_DENY, "申请被拒绝")
    )
    own_id = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE, related_name="own", verbose_name="此好友的拥有人")
    friend_id = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE, related_name="friend", verbose_name="其好友 ID")
    friend_status = models.SmallIntegerField(choices=FRIEND_STATUS, default=1, verbose_name="好友状态")

    class Meta:
        # 联合主键
        verbose_name = "好友"
        verbose_name_plural = verbose_name
        unique_together = (("own_id", "friend_id"),)

    def __str__(self):
        return "<{}.{}-{}>".format(self.__class__.__name__, self.own_id, self.friend_id)
