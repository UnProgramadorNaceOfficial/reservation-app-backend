from django.db import models

class Establecimiento(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    direccion = models.CharField(max_length=300)
    ciudad = models.CharField(max_length=100)
    capacidad = models.CharField(max_length=100, default="25")
    estado = models.CharField(max_length=100, default="Disponible")
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre