# -*- coding: UTF-8 -*-
 
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import configparser
cf = configparser.ConfigParser()
cf.read("conf.ini")
conf = dict(cf.items('mail'))
 
my_sender=conf['sender']    # 发件人邮箱账号
my_pass =conf['pass']              # 发件人邮箱密码
my_user=conf['receiver']      # 收件人邮箱账号，我这边发送给自己
def mail(content):
    ret=True
    try:
        msg=MIMEText(content,'plain','utf-8')
        msg['From']=formataddr(["HotWordSpider",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["张天宇",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="Error Report"                # 邮件的主题，也可以说是标题
 
        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret
 
