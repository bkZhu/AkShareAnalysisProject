def send_qq_email(
        sender_email,
        sender_token,
        receiver_email,
        title_str,
        content_str):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    # 创建SMTP对象
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_port = 465  # 设置服务器端口
    server = smtplib.SMTP_SSL(mail_host, mail_port)

    # 登录邮箱
    server.login(sender_email, sender_token)

    # 创建一个MIMEText邮件对象，HTML邮件正文
    message = MIMEText(content_str, 'plain', 'utf-8')
    message['From'] = sender_email  # 邮件的发送者
    message['To'] = receiver_email  # 邮件的接收者
    message['Subject'] = Header(title_str, 'utf-8')

    # 发送邮件
    server.sendmail(sender_email, [receiver_email], message.as_string())

    # 断开服务器连接
    server.quit()