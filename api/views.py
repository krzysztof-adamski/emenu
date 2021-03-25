from rest_framework import mixins
from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
#from django.contrib.auth.models import User
from .models import Menu, Meal
from django.db.models import Count
from .serializers import MenuSerializer
from rest_framework import (
    filters,
    generics,
    status,
    viewsets,
    mixins
)

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin


class MenuViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    queryset = Menu.objects.annotate(meals_count=Count('meals')).order_by("name", "meals_count")
    #queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'meals', 'meals_count']
    ordering = ['name']

    def get_queryset(self):
        #import ipdb; ipdb.set_trace()
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            return qs
        return qs.filter(meals_count__gt=0)


# class MenuDetail(APIView):
#
#     def get(self, request, restaurant_id, recipe_id):
#         try:
#             recipe = Recipe.objects.get(restaurant__id=restaurant_id, pk=recipe_id)
#         except Recipe.DoesNotExist:
#             raise Http404
#         serializer = serializers.RecipeSerializer(recipe)
#         return Response(serializer.data)
#
#     def delete(self, request, restaurant_id, recipe_id):
#         try:
#             recipe = Recipe.objects.get(restaurant__id=restaurant_id, pk=recipe_id)
#         except Recipe.DoesNotExist:
#             raise Http404
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# class MenuViewSet(APIView):
#
#     def get(self, request, id):
#         meals = Meal.objects.filter(menu__id=id)
#         serializer = serializers.MenuSerializer(meals, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, id):
#         try:
#             Menu.objects.get(pk=id)
#         except Menu.DoesNotExist:
#             raise Http404
#
#         serializer = serializers.MenuSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(menu_id=id, meals=request.data.get("meals"))
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
