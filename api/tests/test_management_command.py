from django.conf import settings
import datetime
from datetime import timedelta
from django.core.management import call_command
from django.test import TestCase

from api.factories import (
    MealFactory,
    MenuFactory,
    UserFactory,
)
from api.models import Menu, Meal
from django.contrib.auth.models import User

NOW = datetime.datetime.now()
YESTERDAY = NOW - timedelta(days=1)
TWODAYSAGO = NOW - timedelta(days=2)


class EmailForSubscribersTests(TestCase):
    def setUp(self):
        User.objects.all().delete()
        Menu.objects.all().delete()
        Meal.objects.all().delete()
        self.args = []
        self.opts = {}

    def test_shouldnt_send_email_to_subscribers(self):
        user = UserFactory.create()
        user.email = "krzysadam@gmail.com"
        user.save()
        user.refresh_from_db()
        self.menu = MenuFactory.create()
        meal = MealFactory.create(menu=self.menu)
        meal.created = TWODAYSAGO
        meal.updated = YESTERDAY
        meal.save()
        meal.refresh_from_db()

        meal = MealFactory.create(menu=self.menu)
        meal.save()
        meal.refresh_from_db()

        call_command("email_for_subscribers", *self.args, **self.opts)
