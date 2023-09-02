from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'nickname', 'username', 'password', 'email', ]

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
    nickname = serializers.CharField(source='user.nickname')

    class Meta:
        model = Profile
        fields = ['user', 'nickname', 'profile_img', 'about_me', 'updated_at']


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
        token['username'] = user.username,
        token['email'] = user.email,
        token['nickname'] = user.nickname
        return token
