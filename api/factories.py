import datetime

from django.contrib.auth.models import User

import factory
from factory.fuzzy import FuzzyChoice, FuzzyNaiveDateTime, FuzzyText

from api.models import Meal, Menu


class MenuFactory(factory.DjangoModelFactory):
    """Faktoria do obiektu Menu."""

    name = factory.Faker("name")
    description = FuzzyText()
    created = FuzzyNaiveDateTime(datetime.datetime.now())
    updated = FuzzyNaiveDateTime(datetime.datetime.now())

    class Meta:
        model = Menu


class MealFactory(factory.DjangoModelFactory):
    """Faktoria do obiektu Meal."""

    name = factory.Faker("name")
    description = FuzzyText()
    price = factory.Sequence(lambda n: n)
    created = FuzzyNaiveDateTime(datetime.datetime.now())
    updated = FuzzyNaiveDateTime(datetime.datetime.now())
    is_vege = FuzzyChoice([True, False])
    prepartion_time = factory.Sequence(lambda n: n)
    menu = factory.SubFactory(MenuFactory)

    class Meta:
        model = Meal


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
