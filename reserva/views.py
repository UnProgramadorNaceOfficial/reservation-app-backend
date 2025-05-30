from global_project.permissions import IsAuthenticate
from rest_framework import viewsets

from reserva.models import Reserva
from reserva.serializer import ReservaSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import json

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticate]

    @action(detail=False, methods=['get'], url_path='exportar-pdf')
    def exportar_pdf(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_reservas.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter
        y = height - 40

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y, "Reporte de Reservas")
        y -= 30

        p.setFont("Helvetica", 10)

        reservas = Reserva.objects.select_related('cliente', 'establecimiento').all()
        for reserva in reservas:
            if y < 80:
                p.showPage()
                y = height - 40
                p.setFont("Helvetica", 10)

            # Línea 1: Fecha y Cliente
            p.drawString(50, y, f"Fecha: {reserva.fecha.strftime('%Y-%m-%d %H:%M')}")
            p.drawString(300, y, f"Cliente: {reserva.cliente.nombre} {reserva.cliente.apellido}")
            y -= 15

            # Línea 2: Documento
            p.drawString(50, y, f"Documento del cliente: {reserva.cliente.documento}")
            y -= 15

            # Línea 3: Establecimiento
            p.drawString(50, y, f"Establecimiento: {reserva.establecimiento.nombre} - {reserva.establecimiento.ciudad}")
            y -= 15

            # Línea 4: Valor
            p.drawString(50, y, f"Valor: ${reserva.valor}")
            y -= 25  # Espacio extra entre reservas

        p.showPage()
        p.save()
        return response
    
    @action(detail=False, methods=['get'], url_path='exportar-json')
    def exportar_json(self, request):
        reservas = Reserva.objects.select_related('cliente', 'establecimiento').all()
        data = []

        for reserva in reservas:
            data.append({
                "fecha": reserva.fecha.strftime('%Y-%m-%d %H:%M'),
                "cliente": {
                    "nombre": reserva.cliente.nombre,
                    "apellido": reserva.cliente.apellido,
                    "documento": reserva.cliente.documento
                },
                "establecimiento": {
                    "nombre": reserva.establecimiento.nombre,
                    "ciudad": reserva.establecimiento.ciudad
                },
                "valor": float(reserva.valor)
            })

        json_data = json.dumps(data, indent=4)

        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="reporte_reservas.json"'
        return response

