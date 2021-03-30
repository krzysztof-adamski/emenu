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
        ).order_by("name", "meals_count")


class MealManager(models.Manager):
    def latest_created(self):
        return self.get_queryset().filter(
            created__year=TODAY.strftime("%Y"),
            created__month=TODAY.strftime("%m"),
            created__day=TODAY.strftime("%d"),
        )

    def latest_updated(self):
        return self.get_queryset().filter(
            updated__year=TODAY.strftime("%Y"),
            updated__month=TODAY.strftime("%m"),
            updated__day=TODAY.strftime("%d"),
        )

    def for_subscribers(self):
        return {
            "latest_updated": self.latest_updated(),
            "latest_created": self.latest_created(),
        }
