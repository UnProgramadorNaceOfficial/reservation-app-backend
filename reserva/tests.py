from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from reserva.models import Reserva
from cliente.models import Cliente
from establecimiento.models import Establecimiento


class ReservaTest(APITestCase):
    def setUp(self):
        # Crear usuario con rol ADMINISTRADOR
        User = get_user_model()
        self.user = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com',
            role='ADMINISTRADOR'
        )

        # Autenticarnos
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Crear mocks de Cliente y Establecimiento
        self.cliente = Cliente.objects.create(
            nombre="Juan", apellido="Pérez", documento="123456", email="juan@example.com", edad=30
        )
        self.establecimiento = Establecimiento.objects.create(
            nombre="Hotel ABC", tipo="Hotel", direccion="Calle 123", ciudad="Bogotá", telefono="1234567890"
        )

        # Crear mock de reserva
        self.data = {
            "fecha": "2025-06-01T15:00:00Z",
            "descripcion": "Reserva de prueba",
            "valor": "150000.00",
            "cliente": self.cliente.id,
            "establecimiento": self.establecimiento.id
        }

    def crear_reserva(self):
        return Reserva.objects.create(
            fecha=self.data["fecha"],
            descripcion=self.data["descripcion"],
            valor=self.data["valor"],
            cliente=self.cliente,
            establecimiento=self.establecimiento
        )

    # CREAR
    def test_crear_reserva_autenticado(self):
        response = self.client.post('/reserva/api/v1/reserva/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_reserva_sin_token(self):
        self.client.credentials()
        response = self.client.post('/reserva/api/v1/reserva/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # LISTAR
    def test_listar_reservas_autenticado(self):
        self.crear_reserva()
        response = self.client.get('/reserva/api/v1/reserva/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_listar_reservas_sin_token(self):
        self.crear_reserva()
        self.client.credentials()
        response = self.client.get('/reserva/api/v1/reserva/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # OBTENER
    def test_detalle_reserva_autenticado(self):
        reserva = self.crear_reserva()
        response = self.client.get(f'/reserva/api/v1/reserva/{reserva.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['descripcion'], "Reserva de prueba")

    def test_detalle_reserva_sin_token(self):
        reserva = self.crear_reserva()
        self.client.credentials()
        response = self.client.get(f'/reserva/api/v1/reserva/{reserva.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ACTUALIZAR
    def test_actualizar_reserva_autenticado(self):
        reserva = self.crear_reserva()
        nueva_data = self.data.copy()
        nueva_data['descripcion'] = 'Hotel medellin'
        response = self.client.put(f'/reserva/api/v1/reserva/{reserva.id}/', nueva_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['descripcion'], 'Hotel medellin')

    def test_actualizar_reserva_sin_token(self):
        reserva = self.crear_reserva()
        nueva_data = self.data.copy()
        nueva_data['descripcion'] = 'Hotel medellin'
        self.client.credentials()
        response = self.client.put(f'/reserva/api/v1/reserva/{reserva.id}/', nueva_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ELIMINAR
    def test_eliminar_reserva_autenticado(self):
        reserva = self.crear_reserva()
        response = self.client.delete(f'/reserva/api/v1/reserva/{reserva.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_eliminar_reserva_sin_token(self):
        reserva = self.crear_reserva()
        self.client.credentials()
        response = self.client.delete(f'/reserva/api/v1/reserva/{reserva.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
