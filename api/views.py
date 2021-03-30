from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from api.filters import MenuFilter
from api.models import Meal, Menu
from api.serializers import MealSerializer, MenuSerializer


class MenusListViewSet(NestedViewSetMixin, ModelViewSet):
    model = Menu
    queryset = Menu.objects.with_count_meals()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MenuFilter
    ordering_fields = ["meals_name", "meals_count"]
    ordering = ["name"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            return qs
        return qs.filter(meals_count__gt=0)


class MealsListViewSet(NestedViewSetMixin, ModelViewSet):
    model = Meal
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
