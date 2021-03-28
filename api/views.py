from django.db.models import Count

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.generics import get_object_or_404

from api.filters import MenuFilter
from api.models import Meal, Menu
from api.serializers import MealSerializer, MenuSerializer


class MenusBaseView(generics.GenericAPIView):
    queryset = Menu.objects.annotate(
        meals_count=Count("meals"),
        meals_name=Meal.objects.values("name").distinct(),
    ).order_by("name", "meals_count")
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


class MenusList(MenusBaseView, generics.ListCreateAPIView):
    pass


class MenusDetail(MenusBaseView, generics.RetrieveUpdateDestroyAPIView):
    pass


class MealBaseView(generics.GenericAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        get_object_or_404(Menu, pk=pk)
        qs = super().get_queryset()
        return qs.filter(menu_id=pk)


class MealsList(MealBaseView, generics.ListCreateAPIView):
    pass


class MealsDetail(MealBaseView, generics.RetrieveUpdateDestroyAPIView):
    pass
