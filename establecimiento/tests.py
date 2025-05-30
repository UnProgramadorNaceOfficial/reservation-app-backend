from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from establecimiento.models import Establecimiento


class EstablecimientoTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com',
            role='ADMINISTRADOR'
        )

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.establecimiento_data = {
            "nombre": "Café del Centro",
            "tipo": "Cafetería",
            "direccion": "Calle 10 #5-20",
            "ciudad": "Medellín",
            "telefono": "3001234567"
        }

    def crear_establecimiento(self):
        return Establecimiento.objects.create(**self.establecimiento_data)

    # CREAR
    def test_crear_establecimiento_autenticado(self):
        response = self.client.post('/establecimiento/api/v1/establecimiento/', self.establecimiento_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_establecimiento_sin_token(self):
        self.client.credentials()
        response = self.client.post('/establecimiento/api/v1/establecimiento/', self.establecimiento_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # LISTAR
    def test_listar_establecimientos_autenticado(self):
        self.crear_establecimiento()
        response = self.client.get('/establecimiento/api/v1/establecimiento/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_listar_establecimientos_sin_token(self):
        self.crear_establecimiento()
        self.client.credentials()
        response = self.client.get('/establecimiento/api/v1/establecimiento/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # OBTENER
    def test_detalle_establecimiento_autenticado(self):
        establecimiento = self.crear_establecimiento()
        response = self.client.get(f'/establecimiento/api/v1/establecimiento/{establecimiento.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], "Café del Centro")

    def test_detalle_establecimiento_sin_token(self):
        establecimiento = self.crear_establecimiento()
        self.client.credentials()
        response = self.client.get(f'/establecimiento/api/v1/establecimiento/{establecimiento.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ACTUALIZAR
    def test_actualizar_establecimiento_autenticado(self):
        establecimiento = self.crear_establecimiento()
        nueva_data = self.establecimiento_data.copy()
        nueva_data['nombre'] = 'Café Moderno'
        response = self.client.put(f'/establecimiento/api/v1/establecimiento/{establecimiento.id}/', nueva_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Café Moderno')

    def test_actualizar_establecimiento_sin_token(self):
        establecimiento = self.crear_establecimiento()
        nueva_data = self.establecimiento_data.copy()
        nueva_data['nombre'] = 'Café Moderno'
        self.client.credentials()
        response = self.client.put(f'/establecimiento/api/v1/establecimiento/{establecimiento.id}/', nueva_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ELIMINAR
    def test_eliminar_establecimiento_autenticado(self):
        establecimiento = self.crear_establecimiento()
        response = self.client.delete(f'/establecimiento/api/v1/establecimiento/{establecimiento.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_eliminar_establecimiento_sin_token(self):
        establecimiento = self.crear_establecimiento()
        self.client.credentials()
        response = self.client.delete(f'/establecimiento/api/v1/establecimiento/{establecimiento.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
