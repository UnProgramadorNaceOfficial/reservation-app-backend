from django.urls import path, include
from rest_framework import routers
from cliente import views

routers = routers.DefaultRouter()
routers.register(r'cliente', views.ClienteViewSet, 'cliente')

urlpatterns = [
    path("api/v1/", include(routers.urls)),
]