from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from users.models import User
from users.serializers import UserSerializer

_bearer_security = [{'Bearer': []}]


@method_decorator(name='list', decorator=swagger_auto_schema(security=_bearer_security))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(security=_bearer_security))
@method_decorator(name='update', decorator=swagger_auto_schema(security=_bearer_security))
@method_decorator(name='destroy', decorator=swagger_auto_schema(security=_bearer_security))
class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(security=_bearer_security)
    def create(self, request, *args, **kwargs):
        if 'password' in request.data:
            request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(security=_bearer_security)
    def partial_update(self, request, *args, **kwargs):
        if 'password' in request.data:
            request.data['password'] = make_password(request.data['password'])
        return super().partial_update(request, *args, **kwargs)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(security=_bearer_security)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
