import uuid
from django.db import models
from django.conf import settings
from users.models import RoleEnum, GradeEnum


class Stack(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    github = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    stacks = models.ManyToManyField('Stack', related_name='projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectPosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='positions'
    )
    role_id = models.CharField(
        max_length=50,
        choices=RoleEnum.choices,
        default=RoleEnum.NOT_SELECTED
    )
    grade_id = models.CharField(
        max_length=50,
        choices=GradeEnum.choices,
        default=GradeEnum.NOT_SELECTED
    )
    count_needed = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.get_role_id_display()} - {self.get_grade_id_display()}"
