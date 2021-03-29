from django.contrib import admin
from django.urls import include, path
from rest_framework_extensions.routers import (
    ExtendedDefaultRouter,
)

from api.views import MenusListViewSet, MealsListViewSet

router = ExtendedDefaultRouter()
(
    router.register(r'menus', MenusListViewSet, basename='menu')
        .register(r'meals', MealsListViewSet, basename='menus-meal', parents_query_lookups=['menu'])
)

urlpatterns = [
    path('api/', include(router.urls)),
    path("admin/", admin.site.urls),
]
