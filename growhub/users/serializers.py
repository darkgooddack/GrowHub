from rest_framework import serializers
from .models import User, RoleEnum, GradeEnum, Skill, UserSkill


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


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


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'telegram', 'avatar',
            'github', 'linkedin', 'resume', 'info',
            'role_id', 'grade_id'
        ]
        read_only_fields = fields


class UserWriteSerializer(serializers.ModelSerializer):
    role_id = serializers.ChoiceField(choices=RoleEnum.choices)
    grade_id = serializers.ChoiceField(choices=GradeEnum.choices)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'telegram', 'avatar',
            'github', 'linkedin', 'resume', 'info',
            'role_id', 'grade_id'
        ]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = UserSkill
        fields = ['id', 'user', 'skill', 'skill_id']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        skill_id = validated_data.pop('skill_id')
        skill = Skill.objects.get(id=skill_id)
        return UserSkill.objects.create(user=user, skill=skill)