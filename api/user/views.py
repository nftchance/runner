from django.contrib.auth import get_user_model

from rest_framework import generics, mixins, permissions, status, views, viewsets
from rest_framework.decorators import action
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


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "user_id"

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageUser]

    def get_serializer_class(self):
        print('action', self.action)

        if self.action in ['update', 'partial_update'] or self.request.method == 'PATCH':
            self.serializer_class = UpdateUserSerializer

        if self.action in ['log_out']:
            self.serializer_class = LogOutSerializer

        if self.action in ['update_password']:
            self.serializer_class = ChangePasswordSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        if self.request.user.has_perm('user.manage_user'):
            return self.get_queryset.all()

        return self.queryset.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action in ['sign_up']:
            self.permission_classes = []
        if self.action in ['log_out', 'log_out_all']:
            self.permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=['post'], url_path='sign-up')
    def sign_up(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        serializer = self.get_serializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'], url_path='password')
    def update_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.set_password(serializer.validated_data['password1'])
        user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='log-out')
    def log_out(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='log-out-all')
    def log_out_all(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer