from django_filters import rest_framework as filters

from api.models import Menu


class MenuFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="contains")
    created = filters.DateFilter(lookup_expr="contains")
    updated = filters.DateFilter(lookup_expr="contains")

    class Meta:
        model = Menu
        fields = ["created", "updated", "name"]
