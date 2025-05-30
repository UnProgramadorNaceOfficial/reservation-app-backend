from django.urls import path, include
from rest_framework import routers
from reserva import views

routers = routers.DefaultRouter()
routers.register(r'reserva', views.ReservaViewSet, 'reserva')

urlpatterns = [
    path("api/v1/", include(routers.urls))
]