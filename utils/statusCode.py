"""
    状态码配置文件

    错误码：1000 ~ 1999
    成功码：2000 ~ 2999
"""

from .response import Error, Success, Status

'''
class GenericsStatus:
    """
    通用简易型状态码类

    使用时只需传入状态码，而无需配置错误 | 成功信息
    自动以类名作为补充信息
    """
    def __init__(self, err_code: int, suc_code: int):
        cls_name = self.__class__.__name__
        self.Error: Error = Error(err_code, "{} Error".format(cls_name))
        self.Success: Success = Success(suc_code, "{} Success".format(cls_name))

class Status:
    """
    状态码类

    使用时需传入详细的配置信息
    """
    def __init__(self, err: Error, suc: Success):
        self.Error: Error = err
        self.Success: Success = suc

'''


class Register:
    Error = Error(1000, "Register Error")
    Success = Success(2000, "Register Success")


class WeChatRegister:
    Error = Error(1001, "WeChatRegister Error")
    Success = Success(2001, "WeChatRegister Success")


class Login:
    Error = Error(1002, "Login Error")
    Success = Success(2002, "Login Success")


class WeChatLogin:
    Error = Error(1003, "WeChat Login Error")
    Success = Success(2003, "WeChat Login Success")


class AvatarModify:
    Error = Error(1004, "Avatar Modify Error")
    Success = Success(2004, "AvatarModify Success")


class UserNameModify:
    Error = Error(1005, "UserName Modify Error")
    Success = Success(2005, "UserName Modify Success")


class GetCode:
    Error = Error(1006, "Get Code Error")
    Success = Success(2006, "Get Code Success")


class PasswordModify:
    Error = Error(1007, "Password Modify Error")
    Success = Success(2007, "Password Modify Success")


class QQModify:
    Error = Error(1008, "QQ Modify Error")
    Success = Success(2008, "QQ Modify Success")


class Logout:
    Error = Error(1009, "Logout Error")
    Success = Success(2009, "Logout Success")


class Exit:
    Error = Error(1010, "Exit Error")
    Success = Success(2010, "Exit Success")


class GoodUpload:
    Error = Error(1011, "Good Upload Error")
    Success = Success(2011, "Good Upload Success")


class WantedUserUpdate:
    Error = Error(1012, "WantedUser Update Error")
    Success = Success(2012, "WantedUser Update Success")


class WantedUserDelete:
    Error = Error(1013, "WantedUser Delete Error")
    Success = Success(2013, "WantedUser Delete Success")


class GoodsModify:
    Error = Error(1014, "Goods Modify Error")
    Success = Success(2014, "Goods Modify Success")


class ThreadUpload:
    Error = Error(1015, "Thread Upload Error")
    Success = Success(2015, "Thread Upload Success")


class AppreciateThread:
    Error = Error(1016, "Thread appreciate Error")
    Success = Success(2016, "Thread appreciate Success")


class GetAppreciateThreadPeople:
    Error = Error(1017, "Get Appreciate Thread People Error")
    Success = Success(2017, "Get Appreciate Thread People Success")


class ThreadDelete:
    Error = Error(1018, "Thread Delete People Error")
    Success = Success(2018, "Thread Delete People Success")

class DeleteAppreciateThread:
    Error = Error(1019, "AppreciateThread Delete People Error")
    Success = Success(2019, "AppreciateThread Delete People Success")

class DeleteThreadComment:
    Error = Error(1020, "ThreadComment Delete People Error")
    Success = Success(2020, "ThreadComment Delete People Success")

class GetTopic:
    Error = Error(1021, "Get Topic People Error")
    Success = Success(2021, "Get Topic Delete People Success")

class StudentIdModify:
    Error = Error(1022, "StudentId Modify Error")
    Success = Success(2022, "StudentId Modify Success")


class SchoolZoneModify:
    Error = Error(1023, "SchoolZone Modify Error")
    Success = Success(2023, "SchoolZone Modify Success")


class ProfileModify:
    Error = Error(1024, "Profile Modify Error")
    Success = Success(2024, "Profile Modify Success")

class DeleteAppreciateThreadComment:
    Error = Error(1024, "Delete Appreciate ThreadComment Error")
    Success = Success(2024, "Delete Appreciate ThreadComment Success")


class MessageDelete:
    Error = Error(1025, "Message Delete Error")
    Success = Success(2025, "Message Delete Success")

class GoodSold:
    Error = Error(1026, "Good Sold Error")
    Success = Success(2026, "Good Sold Success")

class GoodAudit:
    Error = Error(1027, "Good Audit Error")
    Success = Success(2027, "Good Audit Success")

class ThreadAudit:
    Error = Error(1027, "Thread Audit Error")
    Success = Success(2027, "Thread Audit Success")

class GoodReport:
    Error = Error(1028, "Good Report Error")
    Success = Success(2028, "Good Report Success")

class ThreadReport:
    Error = Error(1029, "Thread Report Error")
    Success = Success(2029, "Thread Report Success")

class CommentReport:
    Error = Error(1030, "Comment Report Error")
    Success = Success(2030, "Comment Report Success")

'''
 --- titto start ---
'''

class ThreadCommentUpload:
    Error = Error(1500, "Thread Comment Upload Error")
    Success = Success(2500, "Thread Comment Upload Success")


class AppreciateThreadComment:
    Error = Error(1501, "Appreciate Thread Comment Error")
    Success = Success(2501, "Appreciate Thread Comment Success")

class FriendApply:
    Error = Error(1503, "Friend Apply Error")
    Success = Success(2503, "Friend Apply Success")

class DeleteFriend:
    Error = Error(1504, "Friend Delete Error")
    Success = Success(2504, "Friend Delete Success")

class FriendApplyPass:
    Error = Error(1505, "Friend Apply Pass Error")
    Success = Success(2505, "Friend Apply Pass Success")

class FriendDetails:
    Error = Error(1506, "FriendDetails Get Error")
    Success = Success(2506, "FriendDetails Get Success")

'''
 --- titto end ---
'''
