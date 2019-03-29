from django.core.mail import send_mail
from bbs import settings

def send_active_mail(username,receiver,token):
    '''
    封装发送激活邮件的函数
    :param username:
    :param recever:
    :param token:
    :return:
    '''
    subject = "博客用户激活"  # 标题
    message = ""  # 邮件正文(纯文本)
    sender = settings.EMAIL_FROM  # 发件人
    receivers = [receiver]  # 接收人, 需要是列表
    # 邮件正文(带html样式)
    html_message = '<h2>尊敬的 %s, 感谢注册我的blog</h2>' \
                   '<p>请点击此链接激活您的帐号: ' \
                   '<a href="http://127.0.0.1:8000/active/%s">' \
                   'http://127.0.0.1:8000/active/%s</a>' \
                   % (username, token, token)
    send_mail(subject, message, sender, receivers, html_message=html_message)