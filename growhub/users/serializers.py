from rest_framework import serializers
from .models import User, RoleEnum, GradeEnum, Skill, Experience


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'code', 'name']


class ExperienceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Experience
        fields = ['id', 'company', 'position', 'start_date', 'end_date', 'description']


class UserReadSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    experiences = ExperienceSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'telegram', 'avatar',
            'github', 'linkedin', 'resume', 'info',
            'role_id', 'grade_id', 'skills', 'experiences'
        ]
        read_only_fields = fields


class UserWriteSerializer(serializers.ModelSerializer):
    role_id = serializers.ChoiceField(choices=RoleEnum.choices)
    grade_id = serializers.ChoiceField(choices=GradeEnum.choices)
    skills = serializers.ListField(
        child=serializers.UUIDField(),
        required=False
    )
    experiences = ExperienceSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'telegram', 'avatar',
            'github', 'linkedin', 'resume', 'info',
            'role_id', 'grade_id', 'skills', 'experiences'
        ]

    def update(self, instance, validated_data):
        skill_ids = validated_data.pop('skills', None)
        experiences = validated_data.pop('experiences', None)

        instance = super().update(instance, validated_data)

        # обработка скиллов
        if skill_ids is not None:
            skills = Skill.objects.filter(id__in=skill_ids)
            instance.skills.set(skills)

        # обработка опыта
        if experiences is not None:
            instance.experiences.all().delete()
            for exp_data in experiences:
                Experience.objects.create(user=instance, **exp_data)

        return instance
