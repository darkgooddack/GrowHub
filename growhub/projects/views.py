from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Project, ProjectPosition, Stack
from .serializers import (ProjectReadSerializer,
                          ProjectWriteSerializer, ProjectPositionWriteSerializer,
                          StackSerializer, ProjectPositionReadSerializer)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsProjectAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменять/удалять только автору проекта.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.project.author == request.user


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related('stacks', 'positions', 'author')
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['stacks', 'positions__role_id', 'positions__grade_id']
    search_fields = ['name', 'description', 'author__username']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'my']:
            return ProjectReadSerializer
        return ProjectWriteSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthorOrReadOnly()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        project = Project.objects.get(pk=response.data['id'])
        return Response(ProjectReadSerializer(project, context={'request': request}).data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        project = self.get_object()
        return Response(ProjectReadSerializer(project, context={'request': request}).data)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated]
    )
    def my(self, request):
        projects = self.queryset.filter(author=request.user)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)



class ProjectPositionViewSet(viewsets.ModelViewSet):
    queryset = ProjectPosition.objects.select_related('project').all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role_id', 'grade_id']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'my']:
            return ProjectPositionReadSerializer
        return ProjectPositionWriteSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsProjectAuthorOrReadOnly()]
        return [permissions.IsAuthenticated()]

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated]
    )
    def my(self, request):
        """
        Вернуть только позиции в проектах, созданных текущим пользователем
        """
        positions = self.queryset.filter(project__author=request.user)
        serializer = self.get_serializer(positions, many=True)
        return Response(serializer.data)


class StackViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Только чтение: просмотр доступных стеков
    """
    queryset = Stack.objects.all()
    serializer_class = StackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
