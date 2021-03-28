import datetime
from datetime import timedelta

from django.db import models
from django.db.models import Count

TODAY = datetime.datetime.today()
YESTERDAY = TODAY - timedelta(days=1)


class MenuManager(models.Manager):
    def with_count_meals(self):
        return self.annotate(
            meals_count=Count("meals"),
            meals_name=self.values("name").distinct(),
        ).order_by("name", "meals_count")


class MealManager(models.Manager):
    def latest_created(self):
        return self.filter(created__exact=TODAY)

    def latest_updated(self):
        return self.filter(created__exact=YESTERDAY)

    def for_subscribers(self):
        return {
            "latest_updated": self.latest_updated(),
            "latest_created": self.latest_created(),
        }
