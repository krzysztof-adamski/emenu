# from rest_framework import mixins
# from rest_framework import generics
# from rest_framework import status, viewsets
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
# #from django.contrib.auth.models import User
# from .models import Menu, Meal
# from django.db.models import Count
# from .serializers import MenuSerializer
# from rest_framework import (
#     filters,
#     generics,
#     status,
#     viewsets,
#     mixins
# )
#
#
# class MenuListAPIView(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
#     queryset = Menu.objects.annotate(meals_count=Count('meals')).order_by("name", "meals_count")
#     serializer_class = MenuSerializer
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['name', 'meals']
#     ordering = ['name']
#
#     def get_queryset(self):
#         #import ipdb; ipdb.set_trace()
#         qs = super().get_queryset()
#         if self.request.user.is_authenticated:
#             return qs
#         return qs.filter(meals_count__gt=0)
#
#
# class MenuDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
#     queryset = Menu.objects.all()
#     serializer_class = MenuSerializer
#
#
# # class MenuViewSet(viewsets.ReadOnlyModelViewSet):
# #     """
# #     A simple ViewSet for viewing and editing accounts.
# #     """
# #     queryset = Menu.objects.all()   #prefetch_related('meal_set')  # .annotate(meals_count=Count('meals'))
# #     serializer_class = MenuSerializer
# #     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
# #     #permission_classes = [IsAccountAdminOrReadOnly]
#
# #     def create(self, request, *args, **kwargs):
# #         data = request.data
#
# #         # menu = Menu.objects.create(**data)
# #         # menu.save()
#
# #         # for meal in data["meals"]:
# #         #     module_obj = Meal.objects.get(module_name=module["module_name"])
# #         #     new_student.modules.add(module_obj)
#
# #         # serializer = StudentsSerializer(new_student)
#
# #         # return Response(serializer.data)
#
#
# # class MenuDetail(mixins.RetrieveModelMixin,
# #                     generics.GenericAPIView):
# #     queryset = Menu.objects.all()
# #     serializer_class = MenuSerializer
#
# #     def get(self, request, *args, **kwargs):
# #         return self.retrieve(request, *args, **kwargs)
