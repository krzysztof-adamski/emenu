from django.db import models


class Menu(models.Model):   # autor
    name = models.CharField(max_length=50, blank=False, null=False, unique=True, verbose_name="Nazwa")
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #meals = models.ManyToManyField(Meal, blank=True)
    #thumbnail = models.ImageField(upload_to="recipe_thumbnails", default="recipe_thumbnails/default.png")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Meal(models.Model):  # book
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=3)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_vege = models.BooleanField(default=False)
    prepartion_time = models.IntegerField()
    menu = models.ForeignKey(Menu, related_name="meals", blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

