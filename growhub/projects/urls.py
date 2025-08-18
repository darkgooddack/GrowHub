from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectPositionViewSet, StackViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'positions', ProjectPositionViewSet, basename='position')
router.register(r'stacks', StackViewSet, basename='stack')  # новый эндпоинт

urlpatterns = [
    path('', include(router.urls)),
]
