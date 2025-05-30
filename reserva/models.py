from django.db import models
from cliente.models import Cliente
from establecimiento.models import Establecimiento

class Reserva(models.Model):
    fecha = models.DateTimeField()
    descripcion = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=100, default="Confirmado")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, related_name='reservas')

    def __str__(self):
        return f"Reserva {self.id} - {self.fecha}"