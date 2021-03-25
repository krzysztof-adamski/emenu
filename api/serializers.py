from rest_framework import serializers
from .models import Menu, Meal
from rest_framework.validators import UniqueValidator


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        #fields = "__all__"
        fields = ['id', 'name', 'description', 'created', 'updated', 'price', "is_vege", "prepartion_time"]
        #extra_kwargs = {'id': {'read_only': False, 'required': True}}
        #exclude = ["meals"]


class MenuSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True)
    name = serializers.CharField(
        max_length=50,
        validators=[
            UniqueValidator(queryset=Menu.objects.all())
        ]
    )
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'created', 'updated', 'meals']
        #fields = "__all__"
        extra_kwargs = {'id': {'read_only': True, 'required': True}}
        #extra_kwargs = {'meals': {'read_only': True, 'required': False}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['meals'].read_only = True
        #import ipdb; ipdb.set_trace()
        if 'create' in self.context['view'].action:
            self.fields['meals'].write_only = True
            self.fields['meals'].required = False
            #self.fields['meals'].read_only = True
        else:
            self.fields['meals'].read_only = True

    def create(self, validated_data):
        #import ipdb;      ipdb.set_trace()
        meals_data = validated_data.pop("meals", [])
        menu = Menu.objects.create(**validated_data)
        for meal_dict in meals_data:
            Meal.objects.create(menu=menu, **meal_dict)
        return menu

    def update(self, menu, validated_data):
        #import ipdb; ipdb.set_trace()
        meals_data = validated_data.pop("meals", [])
        #import ipdb;        ipdb.set_trace()
        menu.__dict__.update(validated_data)
        menu.save()
        for meal_dict in meals_data:
            #pk = meal_dict.pop("id")
            meal, created = Meal.objects.get_or_create(**meal_dict)
            if created:
                meal.menu = menu
            #meal.__dict__.update(meal_dict)
            meal.save()
        return menu