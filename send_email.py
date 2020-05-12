import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendmail(subject, msg, toaddrs, fromaddr, smtpaddr, password):
    """
    @subject:邮件主题
    @msg:邮件内容
    @toaddrs:收信人的邮箱地址
    @fromaddr:发信人的邮箱地址
    @smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com
    @password:发信人的邮箱密码
    """
    mail_msg = MIMEMultipart()
    mail_msg['Subject'] = subject
    mail_msg['From'] = fromaddr
    mail_msg['To'] = ','.join(toaddrs)
    mail_msg.attach(MIMEText(msg, 'html', 'utf-8'))
    try:
        s = smtplib.SMTP_SSL()
        s.connect(smtpaddr, 465)  # 连接smtp服务器
        s.login(fromaddr, password)  # 登录邮箱
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string())  # 发送邮件
        s.quit()
    except Exception as e:
        print("Error: unable to send email")
        print(e)


if __name__ == '__main__':
    fromaddr = "******@qq.com"  # 你的发送邮箱
    smtpaddr = "smtp.qq.com"
    toaddrs = ["*****@qq.com"]  # 你的接收邮箱列表
    subject = "最新消息"
    password = "*******"  # 发信人的邮箱密码
    msg = "测试aly"
    sendmail(subject, msg, toaddrs, fromaddr, smtpaddr, password)
