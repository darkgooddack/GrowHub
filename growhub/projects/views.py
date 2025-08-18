from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Technology
from .serializers import ProjectSerializer, TechnologySerializer


class TechnologyViewSet(viewsets.ModelViewSet):
    """
    CRUD для справочника технологий.
    Можно искать по названию (например ?search=Python).
    """
    queryset = Technology.objects.all().order_by("name")
    serializer_class = TechnologySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class ProjectViewSet(viewsets.ModelViewSet):
    """
    CRUD для проектов.
    - Создаёт проект от имени текущего пользователя (creator).
    - Фильтрация по типу, технологиям и создателю.
    - Поиск по title, description, goal.
    """
    queryset = Project.objects.all().prefetch_related("technologies", "team", "creator")
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["type", "technologies", "creator"]
    search_fields = ["title", "description", "goal"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        # creator = текущий авторизованный пользователь
        serializer.save(creator=self.request.user)
