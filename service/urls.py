from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
#from users.views import UserViewSet
#from menus.views import MenuListAPIView, MenuDetailAPIView
#from django.conf.urls import url
#from rest_framework import permissions
from api import views

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r"menus", views.MenuViewSet, basename="menus")


urlpatterns = [
    path('api/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    #path('menu', MenuListAPIView.as_view(), name='menu-list'),
    #path('menu/<int:pk>', MenuDetailAPIView.as_view(), name='menu-detail'),
    #path('admin/', admin.site.urls),
    #path('api/', include('api.urls'))
]
