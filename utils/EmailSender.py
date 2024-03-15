import smtplib
from email.mime.text import MIMEText
from email.header import Header


def getMessage(cls, email_text, receiver_name, encode="utf-8", format_="html"):
    # 封装 message
    message = MIMEText(email_text, format_, encode)
    # 发送者
    # message['from'] = Header(cls.sender_name, encode)
    # 接受者
    # message['to'] = Header(receiver_name, encode)
    # 此邮件名称
    message['Subject'] = Header(cls.email_name, encode)
    # 返回封装后的 message
    return message


class SendEmail:
    def __init__(self, email_name,
                 email_sender="m202373977@hust.edu.cn",
                 email_pawd="52f5ih25CHLDQ3RB",
                 substitute_sender="m202373977@hust.edu.cn",
                 sender_name="华科二手市场"):
        self.substitute_sender = substitute_sender
        self.sender_name = sender_name
        self.email_name = email_name
        # 腾讯企业邮箱 提供第三方 SMTP 服务
        self.email_host = 'mail.hust.edu.cn'
        # 发送者的腾讯企业邮箱用户名
        self.email_sender = email_sender
        # 发送者的 腾讯企业邮箱授权码
        self.email_pawd = email_pawd
        # 链接 腾讯企业邮箱 SMTP 服务
        self.smtpObj = smtplib.SMTP_SSL(self.email_host, 465)
        # 登录
        self.smtpObj.login(self.email_sender, self.email_pawd)
        # 发送邮件

    def send(self, email_text, receiver_name, receiver_list):
        # 代发者
        substitute_sender = self.substitute_sender
        # 收信人列表
        self.receiver_list = receiver_list
        # 封装邮件信息
        message = getMessage(self, email_text, receiver_name)
        try:
            self.smtpObj.sendmail(substitute_sender, receiver_list, message.as_string())
        except smtplib.SMTPException as e:
            print(e)

    def quit(self):
        self.smtpObj.quit()
