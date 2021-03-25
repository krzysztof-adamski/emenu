from django.urls import path
from . import views

urlpatterns = [
    path('menus/', views.MenuListView.as_view()),
    path('menus/<int:id>/', views.MenuDetailView.as_view()),
    # path('restaurants/<str:restaurant_id>/recipes/', views.Recipes.as_view()),
    # path('restaurants/<str:restaurant_id>/recipes/<str:recipe_id>/', views.RecipeDetail.as_view()),
]