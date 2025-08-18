from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import UserFilter
from .models import User, Skill, UserSkill
from .serializers import RegisterSerializer, UserReadSerializer, UserWriteSerializer, SkillSerializer, \
    UserSkillSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        if self.action == 'retrieve':
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserWriteSerializer
        return UserReadSerializer

    def get_object(self):
        if self.request.user.is_superuser and 'pk' in self.kwargs:
            return super().get_object()
        return self.request.user

    def get_queryset(self):
        if self.action == 'list':
            return User.objects.all()  # Все аутентифицированные видят всех
        if self.request.user.is_superuser:
            return User.objects.all()  # Админ видит всех в любом случае
        return User.objects.filter(id=self.request.user.id)  # Обычный юзер видит только себя

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminUser]  # только админ может CRUD навыки


class UserSkillViewSet(viewsets.ModelViewSet):
    serializer_class = UserSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)
