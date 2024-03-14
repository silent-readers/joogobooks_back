from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'nickname', 'username', 'email', ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    def update(self, validated_data):
        user = User.objects.update(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = User
        fields = '__all__'


class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    # response 커스텀
    default_error_messages = {
        'no_active_account':
            {
                'message': 'username or password is incorrect!',
                'success': False,
                'status': 401
            }
    }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 정보 더하기
        token['username'] = user.username
        return token
