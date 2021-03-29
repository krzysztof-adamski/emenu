import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


def sendmail(title, body, to_email, email_template=None):
    context = body
    html_text = render_to_string(email_template, context)
    try:
        email = EmailMultiAlternatives(
            subject=title,
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.attach_alternative(html_text, "text/html")
        #import ipdb;        ipdb.set_trace()
        email.send(fail_silently=False)
    except SMTPException:
        logger.exception("There was an error sending an email")
