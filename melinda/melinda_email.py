"""Module to handle sending emails."""

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail

log = logging.getLogger(__name__)


def send_email(recipients: List[str], email_text: str, subject: str):
    """
    Send an email.

    This uses `sendgrid` if 'SENDGRID_API_KEY' is defined in the environment
        For example, this is the setup on heroku.
    Otherwise it will setup and use a local SMTP server.
    :param recipients: List of email addresses the send the email to.
    :param email_text: Body of the email.
    :param subject: Subject of the email.
    :return:
    """
    log.info("Sending email to %s: %s: %s", recipients, subject, email_text)

    if "NO_EMAIL" in os.environ:
        log.info("Skipped sending email because NO_EMAIL was set in environment.")
        return

    if "SENDGRID_API_KEY" in os.environ:
        # For sending emails from heroku, using "sendgrid" plugin
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get("SENDGRID_API_KEY"))
        from_email = Email("melinda@sendgrid.net")
        to_email = Email(recipients[0])
        content = Content("text/plain", email_text)
        _mail = Mail(from_email, subject, to_email, content)
        for recip in recipients[1:]:
            _mail.personalizations[0].add_to(Email(recip))
        response = sg.client.mail.send.post(request_body=_mail.get())
        log.info("Sendgrid response: %s", response)
    else:
        # For sending emails from local machine
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = "melinda@sendgrid.net"
        msg["To"] = ",".join(recipients)
        msg.attach(MIMEText(email_text))
        s = smtplib.SMTP("int-smtp")
        s.sendmail("melinda@sendgrid.net", recipients, msg.as_string())
        s.quit()


def send_match_email(recipients: List[str], email_text: str):
    """
    Send an email to the given recipients to inform them of being matched.

    See `send_email` for parameter details.
    """
    send_email(recipients, email_text, "You're a match")


def send_report_email(email_text):
    """
    Send an email to the abuse report address.

    :param email_text: The report text to include in the report email.
    """
    send_email(["howarth.martin@gmail.com"], email_text, "Melinda User Report")
