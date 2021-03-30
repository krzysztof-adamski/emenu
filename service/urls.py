from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_extensions.routers import ExtendedDefaultRouter

from api.views import MealsListViewSet, MenusListViewSet

router = ExtendedDefaultRouter()
(
    router.register(r"menus", MenusListViewSet, basename="menu").register(
        r"meals",
        MealsListViewSet,
        basename="menus-meal",
        parents_query_lookups=["menu"],
    )
)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
