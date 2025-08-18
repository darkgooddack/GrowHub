from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from users.models import User


class UserFilter(FilterSet):
    username = CharFilter(field_name='username', lookup_expr='icontains')
    email = CharFilter(field_name='email', lookup_expr='icontains')
    telegram = CharFilter(field_name='telegram', lookup_expr='icontains')
    github = CharFilter(field_name='github', lookup_expr='icontains')
    linkedin = CharFilter(field_name='linkedin', lookup_expr='icontains')
    role_id = CharFilter(field_name='role_id', lookup_expr='exact')
    grade_id = CharFilter(field_name='grade_id', lookup_expr='exact')

    class Meta:
        model = User
        fields = ['username', 'email', 'telegram',
                  'github', 'linkedin', 'role_id', 'grade_id']
