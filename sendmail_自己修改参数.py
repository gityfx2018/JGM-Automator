# coding:utf-8

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = 'xxxxx'  # 发件人邮箱账号
my_pass = 'xxxxx'  # 发件人邮箱密码 这个不是邮箱密码 时smtp的授权码
my_user = 'xxx'  # 收件人邮箱账号，我这边发送给自己

# 设置参数避免import时就发送邮件
def mail(ret=False):
    if ret == True:
        msg = MIMEText('填写邮件内容', 'plain', 'utf-8')
        msg['From'] = formataddr(["From_gityufx", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["gityufx", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "报告老大！！！今日火车发货over！"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP("smtp.qq.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    else:
        print("默认不发邮件")
    return ret


ret = mail()
if ret:
    print("邮件发送成功")
else:
    print("邮件发送失败")