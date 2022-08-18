from django.contrib.auth import get_user_model

from rest_framework import generics, mixins, permissions, status, views, viewsets
from rest_framework.response import Response

from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import CanManageUser
from .serializers import (
    LogInSerializer,
    UpdateUserSerializer,
    ChangePasswordSerializer,
    UserSerializer,
    LogOutSerializer
)

User = get_user_model()

class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = "id"
    lookup_url_kwarg = "user_id"

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageUser]

    def get_queryset(self):
        if self.request.user.has_perm('user.manage_user'):
            return self.get_queryset.all()

        return self.queryset.filter(id=self.request.user.id)

class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer


class UpdateProfileView(generics.UpdateAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "user_id"

    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class ChangePasswordView(generics.UpdateAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "user_id"

    queryset = User.objects.all()

    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = ChangePasswordSerializer


class LogOutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = LogOutSerializer

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
