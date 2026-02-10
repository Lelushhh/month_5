from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, ConfirmCode


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_active=False
        )
        ConfirmCode.objects.create(user=user)
        return user
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('User is not active')
        data['user'] = user
        return data


class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            confirm = user.confirm_code
        except:
            raise serializers.ValidationError('Invalid user')

        if confirm.code != data['code']:
            raise serializers.ValidationError('Invalid code')

        data['user'] = user
        return data
