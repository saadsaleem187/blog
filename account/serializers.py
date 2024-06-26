from django.contrib.auth.models import User

from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        username = data["username"]
        email = data["email"]

        if username:
            if User.objects.filter(username = username).exists():
                raise serializers.ValidationError("Username already taken.")

        if email:
            if User.objects.filter(email = email).exists():
                raise serializers.ValidationError("Email already exists.")

        return data
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data["username"], email = validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
