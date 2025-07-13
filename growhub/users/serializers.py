from rest_framework import serializers
from .models import User

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
    role = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username', 'email', 'telegram', 'avatar',
            'github', 'linkedin', 'resume', 'info',
            'role', 'grade'
        ]
        read_only_fields = fields

    def get_role(self, obj):
        return obj.get_role_id_display()

    def get_grade(self, obj):
        return obj.get_grade_id_display()


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'telegram', 'avatar',
            'github', 'linkedin', 'resume', 'info',
            'role_id', 'grade_id'
        ]
