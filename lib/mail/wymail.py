import smtplib
from email.mime.text import MIMEText

from lib.log import logger_error, logger_debug

# 懒得写了, 这里先就这样吧
mail_host = "smtp.163.com"
mail_user = "notify_robot"
mail_pass = "notify578"
mail_postfix = "163.com"


def send_mail(to_list, sub, content):
    me = "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        # 连接服务器
        server.connect(mail_host)
        # 登录操作
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        logger_debug.debug('send mail success')
        server.close()
        return True
    except Exception as e:
        logger_error.error('send mail error: %s' % e)
        return False
