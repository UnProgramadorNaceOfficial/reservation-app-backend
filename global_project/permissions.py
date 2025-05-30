from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticate(BasePermission):
    """
    Permite acceso total a los administradores.
    Permite solo lectura a los clientes.
    Niega acceso a usuarios no autenticados o con otro rol.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.role == 'ADMINISTRADOR':
            return True  # Acceso total

        if user.role == 'CLIENTE':
            return request.method in SAFE_METHODS  # Solo GET, HEAD, OPTIONS

        return False  # Otros roles o no autenticado
