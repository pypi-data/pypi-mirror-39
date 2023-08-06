# coding: utf-8
# -*- coding: utf-8 -*-

__author__ = "Jalpesh Borad"
__copyright__ = "Copyright 2018"

__version__ = "0.0.1"
__maintainer__ = "Jalpesh Borad"
__email__ = "jalpeshborad@gmail.com"
__status__ = "Development"


import smtplib
from traceback import format_exc

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from error.exceptions import CommunicationError


def send_email(**kwargs):
    """
    Sends e-mail to provided mail-address by source email
    :param kwargs:
    :return:
    """
    try:
        from_addr = kwargs.pop("from")
        passwd = kwargs.pop("passwd")
        host = kwargs.pop("host")
        port = kwargs.pop("port")
        subject = kwargs.pop("subject")
        message = kwargs.pop("message")
        to_add = kwargs.pop("to_add")

        s = smtplib.SMTP(host=host, port=port)
        s.starttls()
        s.login(from_addr, passwd)

        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_add
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))
        s.sendmail(from_addr, to_add, msg.as_string())
        s.quit()
    except Exception:
        raise CommunicationError(format_exc())

