# -*- coding:utf-8 -*-

import click
from .controller.send_mail_controller import SendMailController


@click.option("--sender", help="发件人邮箱地址")
@click.option("--cc", help="抄送人邮箱地址，多个逗号分开")
@click.option("--content", "-c", nargs=1, prompt="请输入邮件正文", help="邮件正文")
@click.option("--sub", "-s", nargs=1, prompt="请输入邮件标题", help="邮件主题")
@click.option("--receivers", "-r", nargs=1, prompt="输入收件人，多个逗号分开", help="收件人邮箱地址,多个逗号分开")
@click.command()
def send_mail(sender, receivers, cc, sub, content):
    """
        发送邮件,不提供参数时自动提示需要输入的参数
    """
    controller = SendMailController()

    if cc is not None:
        cc = cc.split(",")
    receivers = receivers.split(",")

    controller.send_mail(sub, content, sender=sender, receivers=receivers, cc=cc)
