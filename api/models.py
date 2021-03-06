from django.conf import settings
from django.db import models
from django.urls import reverse

from api.managers import MealManager, MenuManager


class Menu(models.Model):
    name = models.CharField(
        max_length=50, blank=False, null=False, unique=True
    )
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = MenuManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_vege = models.BooleanField(default=False)
    prepartion_time = models.IntegerField()
    menu = models.ForeignKey(
        Menu, related_name="meals", blank=True, on_delete=models.CASCADE
    )

    objects = MealManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        reverse_url = reverse(
            "menus-meal-detail",
            kwargs={"parent_lookup_menu": self.menu_id, "pk": self.pk},
        )
        return f"{settings.BASE_URL}{reverse_url}"
