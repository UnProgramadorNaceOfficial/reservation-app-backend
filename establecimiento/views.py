from global_project.permissions import IsAuthenticate
from rest_framework import viewsets

from establecimiento.models import Establecimiento
from establecimiento.serializer import EstablecimientoSerializer

class EstablecimientoViewSet(viewsets.ModelViewSet):
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer
    permission_classes = [IsAuthenticate]