from django.urls import path
from . import views

urlpatterns = [
    path('menus/', views.MenusList.as_view(), name='menus-list'),
    path('menus/<int:pk>/', views.MenusDetail.as_view(), name='menus-detail'),
    path('menus/<int:pk>/meals/', views.MealsList.as_view(), name='menus-meals-list'),
    path('menus/<int:pk>/meals/<int:meal_id>/', views.MealsDetail.as_view(), name='menus-meals-detail'),
]
