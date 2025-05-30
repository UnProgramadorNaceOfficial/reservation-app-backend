from rest_framework import serializers
from .models import Reserva
from cliente.models import Cliente
from establecimiento.models import Establecimiento
from datetime import timedelta
from cliente.serializer import ClienteSerializer
from establecimiento.serializer import EstablecimientoSerializer

class ReservaSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    establecimiento = EstablecimientoSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), write_only=True
    )
    establecimiento_id = serializers.PrimaryKeyRelatedField(
        queryset=Establecimiento.objects.all(), write_only=True
    )

    class Meta:
        model = Reserva
        fields = [
            'id', 'fecha', 'descripcion', 'valor', 'estado',
            'cliente', 'establecimiento', 'cliente_id', 'establecimiento_id'
        ]

    def validate(self, data):
        fecha = data['fecha']
        establecimiento = data['establecimiento_id']
        nueva_inicio = fecha
        nueva_fin = fecha + timedelta(hours=3)

        conflicto = Reserva.objects.filter(
            establecimiento=establecimiento,
            fecha__lt=nueva_fin,
            fecha__gt=nueva_inicio - timedelta(hours=3)
        ).exclude(id=self.instance.id if self.instance else None).order_by('fecha').first()

        if conflicto:
            fin_conflicto = conflicto.fecha + timedelta(hours=3)
            tiempo_restante = fin_conflicto - nueva_inicio
            if tiempo_restante.total_seconds() > 0:
                horas = tiempo_restante.seconds // 3600
                minutos = (tiempo_restante.seconds % 3600) // 60
                raise serializers.ValidationError({
                    "Response": f"El establecimiento no está disponible. Intenta reservar en {horas}h {minutos}min (libre a partir de {fin_conflicto.strftime('%Y-%m-%d %H:%M')})."
                })

        return data

    def create(self, validated_data):
        validated_data['cliente'] = validated_data.pop('cliente_id')
        validated_data['establecimiento'] = validated_data.pop('establecimiento_id')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'cliente_id' in validated_data:
            validated_data['cliente'] = validated_data.pop('cliente_id')
        if 'establecimiento_id' in validated_data:
            validated_data['establecimiento'] = validated_data.pop('establecimiento_id')
        return super().update(instance, validated_data)
