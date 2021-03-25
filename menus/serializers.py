from rest_framework import serializers
from .models import Menu, Meal
from rest_framework.validators import UniqueValidator


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'name', 'description', 'price', 'created', 'updated', 'is_vege', 'prepartion_time']


class MenuSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, read_only=True)
    name = serializers.CharField(
        max_length=50,
        validators=[
            UniqueValidator(queryset=Menu.objects.all())
        ]
    )
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'created', 'updated', 'meals']
        depth = 1
