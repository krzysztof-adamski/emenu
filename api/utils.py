import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


def sendmail(title, text, to_email, email_template=None):
    if email_template:
        context = {"text": text}
        html_text = render_to_string(email_template, context)
    else:
        html_text = None

    try:
        email = EmailMultiAlternatives(
            subject=title,
            body=text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        if html_text:
            email.attach_alternative(html_text, "text/html")
        email.send(fail_silently=False)
    except SMTPException:
        logger.exception("There was an error sending an email")
