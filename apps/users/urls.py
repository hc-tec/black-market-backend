from django.urls import path

from .search import search_view
from .views import *

urlpatterns = [
    path('register/', Register.as_view()),
    path('wechatRegister/', WeChatRegister.as_view()),
    path('login/', Login.as_view()),
    path('wechatLogin/', WeChatLogin.as_view()),
    path('avatarModify/', AvatarModify.as_view()),
    path('userNameModify/', UserNameModify.as_view()),
    path('studentIdModify/', StudentIdModify.as_view()),
    path('schoolZoneModify/', SchoolZoneModify.as_view()),
    path('profileModify/', ProfileModify.as_view()),
    path('passwordModify/', PasswordModify.as_view()),
    path('qqModify/', QQModify.as_view()),
    path('getcode/', GetCode.as_view()),
    path('exit/', Exit.as_view()),
    path('logout/', Logout.as_view()),
    path('getUserinfo/', GetUserInfo.as_view()),
    path('goodsView/', GoodsView.as_view()),
    path('threadView/', ThreadView.as_view()),
    path('getEmailCode/', GetEmailCode.as_view()),
    path('wantedUser/', WantedUser.as_view()),
    path('threadCommitView/', ThreadCommentView.as_view()),
    path('appreciateThread/', AppreciateThread.as_view()),
    path('getAppreciateThreadPeople/', GetAppreciateThreadPeople.as_view()),
    path('appreciateThreadComment/', AppreciateThreadComment.as_view()),
    path('GoodsSearch/', search_view.GoodsSearchView.as_view()),
    path('AutoLogin/', AutoLogin.as_view()),
    path('topicView/', TopicView.as_view()),
    path('AtomicGoodsView/', AtomicGoodsView.as_view()),
    path('AtomicThreadView/', AtomicThreadView.as_view()),
    path('messageView/', MessageView.as_view()),
    path('goodsAuditView/', GoodsAuditView.as_view()),  # 商品审核接口
    path('threadAuditView/', ThreadAuditView.as_view()),  # 帖子审核接口
    path('dealView/', DealView.as_view()),
    path("goodReportView/", GoodReportView.as_view()),  # 商品举报接口

    path('FriendView', FriendView.as_view()),
    path('FriendDetails', FriendDetails.as_view()),
    path('ChatMessage', ChatMessage.as_view()),
    path('ChatUserSearch', search_view.ChatUserSearch.as_view()),
]
