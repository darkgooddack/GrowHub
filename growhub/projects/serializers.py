from rest_framework import serializers
from .models import Project, ProjectPosition, Stack
from users.serializers import UserReadSerializer

from users.models import User


class ProjectPositionWriteSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='project.author.id', read_only=True)

    class Meta:
        model = ProjectPosition
        fields = ['id', 'project', 'user_id', 'role_id', 'grade_id', 'count_needed']
        read_only_fields = ['id', 'project', 'user_id']



class ProjectPositionReadSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_id_display', read_only=True)
    grade = serializers.CharField(source='get_grade_id_display', read_only=True)
    project_id = serializers.UUIDField(source='project.id', read_only=True)
    user_id = serializers.UUIDField(source='project.author.id', read_only=True)

    class Meta:
        model = ProjectPosition
        fields = [
            'id',
            'role',
            'grade',
            'count_needed',
            'project_id',
            'user_id'
        ]


class StackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = ['id', 'name']


class ProjectAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class ProjectReadSerializer(serializers.ModelSerializer):
    author_id = serializers.UUIDField(source="author.id")
    positions = ProjectPositionReadSerializer(many=True)
    stacks = StackSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'github',
            'description',
            'author_id',
            'created_at',
            'stacks',
            'positions',
        ]
        read_only_fields = fields


class ProjectWriteSerializer(serializers.ModelSerializer):
    positions_data = ProjectPositionWriteSerializer(
        many=True, required=False
    )
    stacks = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'github', 'description', 'positions_data', 'stacks']

    def create(self, validated_data):
        positions_data = validated_data.pop('positions_data', [])
        stacks_ids = validated_data.pop('stacks', [])
        user = self.context['request'].user

        project = Project.objects.create(author=user, **validated_data)

        # Создаем позиции
        for pos in positions_data:
            ProjectPosition.objects.create(project=project, **pos)

        # Привязываем стеки через M2M
        if stacks_ids:
            project.stacks.set(stacks_ids)

        return project

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions_data', None)
        stacks_ids = validated_data.pop('stacks_ids', None)

        instance = super().update(instance, validated_data)

        # Обновляем позиции
        if positions_data is not None:
            instance.positions.all().delete()
            for pos in positions_data:
                ProjectPosition.objects.create(project=instance, **pos)

        # Обновляем стеки
        if stacks_ids is not None:
            instance.stacks.set(stacks_ids)

        return instance
