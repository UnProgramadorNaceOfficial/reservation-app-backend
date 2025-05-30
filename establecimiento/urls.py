from django.urls import path, include
from rest_framework import routers
from establecimiento import views

routers = routers.DefaultRouter()
routers.register(r'establecimiento', views.EstablecimientoViewSet, 'establecimiento')

urlpatterns = [
    path("api/v1/", include(routers.urls))
]