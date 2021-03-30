from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from api.models import Meal
from api.utils import sendmail


class Command(BaseCommand):
    def handle(self, *args, **options):
        qs = Meal.objects.for_subscribers()
        for user in User.objects.all():
            sendmail(
                settings.SUBJECT_SUBSCRIBTIONS,
                qs,
                user.email,
                "menu_subscription.html",
            )
