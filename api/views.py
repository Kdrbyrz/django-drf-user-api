from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication


from api.models.user import User
from api.serializers.user_serializer import UserSerializer


class UserSignUpViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post"]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated], authentication_classes=[BasicAuthentication])
    def me(self, request):
        recent_user = self.queryset.filter(pk=request.user.pk)

        serializer = self.serializer_class(recent_user, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="sign-up")
    def sign_up(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                username=serializer.data['username'],
                email=serializer.data['email'],
                first_name=serializer.data['first_name'],
                last_name=serializer.data['last_name'],
                bio=serializer.data['bio'],
            )

            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'User Created.'})
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
