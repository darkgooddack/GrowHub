from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Project, ProjectPosition, Stack
from .serializers import ProjectReadSerializer, ProjectWriteSerializer, ProjectPositionSerializer, StackSerializer, \
    ProjectPositionReadSerializer


# Разрешения: только автор может редактировать, остальные - только чтение
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


# ViewSet для проекта
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related('stacks', 'positions', 'author')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['stacks', 'positions__role_id', 'positions__grade_id']
    search_fields = ['name', 'description', 'author__username']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProjectReadSerializer
        return ProjectWriteSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthorOrReadOnly()]
        return [permissions.IsAuthenticatedOrReadOnly()]


# ViewSet для ProjectPosition (если нужен отдельный CRUD)
class ProjectPositionViewSet(viewsets.ModelViewSet):
    queryset = ProjectPosition.objects.all()
    serializer_class = ProjectPositionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProjectPositionReadSerializer
        return ProjectPositionSerializer

    def get_queryset(self):
        """
        Пользователь видит свои позиции или все позиции для чтения
        """
        user = self.request.user
        if user.is_authenticated:
            return ProjectPosition.objects.select_related('project').all()
        return ProjectPosition.objects.select_related('project').all()


class StackViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Только чтение: просмотр доступных стеков
    """
    queryset = Stack.objects.all()
    serializer_class = StackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

