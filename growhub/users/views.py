from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets, status, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import User, Skill, Experience
from .serializers import (
    RegisterSerializer, UserReadSerializer,
    UserWriteSerializer, SkillSerializer, ExperienceSerializer)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import filters


class IsSelfOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменение/удаление только самому пользователю,
    но просмотр доступен всем аутентифицированным.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


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
    permission_classes = [permissions.IsAuthenticated, IsSelfOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    # Для точных фильтров
    filterset_fields = ['role_id', 'grade_id']

    # Для поиска по тексту
    search_fields = ['username', 'email', 'telegram', 'github', 'linkedin']

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserWriteSerializer
        return UserReadSerializer

    def get_queryset(self):
        return User.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        read_serializer = UserReadSerializer(instance, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_200_OK)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminUser]


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get("user_pk")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("Пользователь не найден")
        return Experience.objects.filter(user=user)

    def perform_create(self, serializer):
        user_id = self.kwargs.get("user_pk")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("Пользователь не найден")
        serializer.save(user=user)
