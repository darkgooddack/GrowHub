from rest_framework import serializers
from .models import User, RoleEnum, GradeEnum


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
            username=validated_data["username"],
            email=validated_data["email"],
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
