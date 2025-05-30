from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from cliente.models import Cliente


class ClienteTest(APITestCase):
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

        # Crear mocks de cliente
        self.cliente_data = {
            "nombre": "Laura",
            "apellido": "García",
            "documento": "987654321",
            "telefono": "3001112233",
            "email": "laura@example.com",
            "edad": 25
        }

    def crear_cliente(self):
        return Cliente.objects.create(**self.cliente_data)

    # CREAR
    def test_crear_cliente_autenticado(self):
        response = self.client.post('/cliente/api/v1/cliente/', self.cliente_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_cliente_sin_token(self):
        self.client.credentials()
        response = self.client.post('/cliente/api/v1/cliente/', self.cliente_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # LISTAR
    def test_listar_clientes_autenticado(self):
        self.crear_cliente()
        response = self.client.get('/cliente/api/v1/cliente/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_listar_clientes_sin_token(self):
        self.crear_cliente()
        self.client.credentials()
        response = self.client.get('/cliente/api/v1/cliente/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # OBTENER
    def test_detalle_cliente_autenticado(self):
        cliente = self.crear_cliente()
        response = self.client.get(f'/cliente/api/v1/cliente/{cliente.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['documento'], "987654321")

    def test_detalle_cliente_sin_token(self):
        cliente = self.crear_cliente()
        self.client.credentials()
        response = self.client.get(f'/cliente/api/v1/cliente/{cliente.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ACTUALIZAR
    def test_actualizar_cliente_autenticado(self):
        cliente = self.crear_cliente()
        nueva_data = self.cliente_data.copy()
        nueva_data['nombre'] = 'Luisa'
        response = self.client.put(f'/cliente/api/v1/cliente/{cliente.id}/', nueva_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Luisa')

    def test_actualizar_cliente_sin_token(self):
        cliente = self.crear_cliente()
        nueva_data = self.cliente_data.copy()
        nueva_data['nombre'] = 'Luisa'
        self.client.credentials()
        response = self.client.put(f'/cliente/api/v1/cliente/{cliente.id}/', nueva_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ELIMINAR
    def test_eliminar_cliente_autenticado(self):
        cliente = self.crear_cliente()
        response = self.client.delete(f'/cliente/api/v1/cliente/{cliente.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_eliminar_cliente_sin_token(self):
        cliente = self.crear_cliente()
        self.client.credentials()
        response = self.client.delete(f'/cliente/api/v1/cliente/{cliente.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
