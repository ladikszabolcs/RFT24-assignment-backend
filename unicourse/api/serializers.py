from rest_framework import serializers
from .models import User, Lecture

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LectureSerializer(serializers.ModelSerializer):
    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Lecture
        fields = '__all__'