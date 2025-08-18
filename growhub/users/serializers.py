from rest_framework import serializers
from .models import User, RoleEnum, GradeEnum, Skill, Experience


class ExperienceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Experience
        fields = ['id', 'company', 'position', 'start_date', 'end_date', 'description']


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
        fields = '__all__'


class UserReadSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'telegram', 'avatar',
            'github', 'linkedin', 'resume', 'info',
            'role_id', 'grade_id', 'skills'
        ]
        read_only_fields = fields


class UserWriteSerializer(serializers.ModelSerializer):
    role_id = serializers.ChoiceField(choices=RoleEnum.choices)
    grade_id = serializers.ChoiceField(choices=GradeEnum.choices)
    skill_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False
    )
    experiences_data = ExperienceSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'telegram', 'avatar',
            'github', 'linkedin', 'resume', 'info',
            'role_id', 'grade_id', 'skill_ids', 'experiences_data'
        ]

    def update(self, instance, validated_data):
        skill_ids = validated_data.pop('skill_ids', None)
        experiences_data = validated_data.pop('experiences_data', None)
        instance = super().update(instance, validated_data)

        if skill_ids is not None:
            instance.skills.set(skill_ids)

        if experiences_data is not None:
            instance.experiences.all().delete()  # удаляем старые места работы
            for exp_data in experiences_data:
                Experience.objects.create(user=instance, **exp_data)

        return instance
