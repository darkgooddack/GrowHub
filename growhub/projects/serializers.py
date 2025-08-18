from rest_framework import serializers
from .models import Project, ProjectPosition, Stack
from users.serializers import UserReadSerializer


class ProjectPositionSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_id_display', read_only=True)
    grade_display = serializers.CharField(source='get_grade_id_display', read_only=True)

    class Meta:
        model = ProjectPosition
        fields = ['id', 'role_id', 'role_display', 'grade_id', 'grade_display', 'count_needed']


class ProjectPositionReadSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_id_display', read_only=True)
    grade_display = serializers.CharField(source='get_grade_id_display', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    author = UserReadSerializer(source='project.author', read_only=True)

    class Meta:
        model = ProjectPosition
        fields = [
            'id', 'role_display',
            'grade_display',
            'count_needed',
            'project_name', 'author'
        ]


class StackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = ['id', 'name']


class ProjectReadSerializer(serializers.ModelSerializer):
    author = UserReadSerializer(read_only=True)
    positions = ProjectPositionSerializer(many=True, read_only=True)
    stacks = StackSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'github', 'description', 'author', 'created_at', 'positions', 'stacks']


class ProjectWriteSerializer(serializers.ModelSerializer):
    positions_data = ProjectPositionSerializer(many=True, write_only=True, required=False)
    stacks_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'github', 'description', 'positions_data', 'stacks_ids']

    def create(self, validated_data):
        positions_data = validated_data.pop('positions_data', [])
        stacks_ids = validated_data.pop('stacks_ids', [])
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
