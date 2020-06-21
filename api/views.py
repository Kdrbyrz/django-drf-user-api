from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg import openapi

from api.models.user import User
from api.serializers.user_serializer import UserSerializer


class UserSignUpViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post"]

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        authentication_classes=[BasicAuthentication],
    )
    def me(self, request):
        recent_user = self.queryset.filter(pk=request.user.pk)

        serializer = self.serializer_class(recent_user, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="string"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="string"
                ),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="string"),
                "first_name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="string"
                ),
                "last_name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="string"
                ),
                "bio": openapi.Schema(type=openapi.TYPE_STRING, description="string"),
            },
            required=["username", "password", "bio"],
        ),
    )
    @action(detail=False, methods=["post"], url_path="sign-up")
    def sign_up(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                username=serializer.data.get("username"),
                email=serializer.data.get("email", ""),
                first_name=serializer.data.get("first_name", ""),
                last_name=serializer.data.get("last_name", ""),
                bio=serializer.data.get("bio"),
            )

            user.set_password(serializer.data["password"])
            user.save()
            return Response({"status": "User created."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
