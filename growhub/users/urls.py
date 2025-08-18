from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import RegisterView, UserViewSet, SkillViewSet, ExperienceViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'skills', SkillViewSet)

users_router = routers.NestedDefaultRouter(router, r'users', lookup='user')
users_router.register(r'experiences', ExperienceViewSet, basename='user-experiences')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('', include(users_router.urls)),
]
