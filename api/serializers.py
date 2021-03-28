from django.core.validators import MaxLengthValidator
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from api.models import Menu, Meal


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = "__all__"

    def create(self, validated_data):
        pk = self.context['view'].kwargs.get("pk")
        menu = get_object_or_404(Menu, pk=pk)
        meal = Meal.objects.create(menu=menu, **validated_data)
        return meal


class MenuSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, read_only=True)
    name = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Menu.objects.all(),
                message=_("Istnieje już menu z tą nazwą!")
            ),
            MaxLengthValidator(
                50, message=_("Maksymalna ilość znaków: 50.")
            )

        ]
    )

    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'created', 'updated', 'meals']
