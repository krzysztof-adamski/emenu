from django.db import models


class Meal(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField()
    price = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=3)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_vege = models.BooleanField(default=False)
    prepartion_time = models.IntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



class Menu(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    meals = models.ManyToManyField(Meal, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
