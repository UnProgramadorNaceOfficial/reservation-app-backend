from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CustomTokenObtainPairSerializer


class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access = response.data.get('access')
            refresh = response.data.get('refresh')

            response.set_cookie(
                settings.SIMPLE_JWT['AUTH_COOKIE'],
                access,
                max_age=3600,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            response.set_cookie(
                settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                refresh,
                max_age=7 * 24 * 3600,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )


        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response({"detail": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)

        response.delete_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH']
        )

        response.delete_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH']
        )

        return response
