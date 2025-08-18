import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import URLValidator
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class RoleEnum(models.TextChoices):
    NOT_SELECTED = 'not_selected', 'Не выбрано'
    BACKEND = 'backend', 'Backend Developer'
    FRONTEND = 'frontend', 'Frontend Developer'
    DEVOPS = 'devops', 'DevOps Engineer'
    DESIGNER = 'designer', 'UI/UX Designer'
    QA = 'qa', 'QA'
    PM = 'pm', 'PM'


class GradeEnum(models.TextChoices):
    NOT_SELECTED = 'not_selected', 'Не выбрано'
    INTERN = 'intern', 'Стажёр'
    JUNIOR = 'junior', 'Junior'
    MIDDLE = 'middle', 'Middle'
    SENIOR = 'senior', 'Senior'
    LEAD = 'lead', 'Tech Lead'
    ARCHITECT = 'architect', 'Архитектор'


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    telegram = models.CharField(max_length=50, unique=True, blank=True, null=True)
    avatar = models.URLField(validators=[URLValidator()], blank=True, null=True)
    github = models.URLField(validators=[URLValidator()], blank=True, null=True)
    linkedin = models.URLField(validators=[URLValidator()], blank=True, null=True)
    resume = models.URLField(validators=[URLValidator()], blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    role_id = models.CharField(
        max_length=20,
        choices=RoleEnum.choices,
        default=RoleEnum.NOT_SELECTED
    )
    grade_id = models.CharField(
        max_length=20,
        choices=GradeEnum.choices,
        default=GradeEnum.NOT_SELECTED
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_staff


class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='skills', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name='users', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"
