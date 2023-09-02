import jwt
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from joongobooks.settings import SECRET_KEY

from .models import User, Profile
from .serializers import UserSerializer, ProfileSerializer, myTokenObtainPairSerializer


class UserRegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    # 회원가입

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            res = Response({
                "user": serializer.data,
                "message": "register success",
            },
                status=status.HTTP_200_OK,
            )

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    # 유저 정보 확인하기

    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저식별
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except (jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신하기
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('used_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            return jwt.exceptions.InvalidTokenError

        except (jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    def post(self, request):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password'),
        )

        if user is not None:
            serializer = UserSerializer(user)

            # jwt 토큰 접근
            token = myTokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    'user': serializer.data,
                    'message': 'login success!',
                    'token': {
                        'access': access_token,
                        'refresh': refresh_token,
                    },
                },
                status=status.HTTP_200_OK
            )

            # jwt 토큰 => 쿠키에 저장
            res.set_cookie('access', access_token, httponly=True)
            res.set_cookie('refresh', refresh_token, httponly=True)
            return res
        else:
            return Response({'message': '로그인에 실패했습니다!'}, status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response(
            {
                'message': 'Logout success!'
            },
            status=status.HTTP_202_ACCEPTED
        )
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response


class ProfileView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id):
        profile = get_object_or_404(Profile, user_id=user_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ProfileCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        nickname = request.data.get('nickname')
        profile_img = request.data.get('profile_img')
        about_me = request.data.get('about_me')

        try:
            user_instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        profile = Profile.objects.create(
            user=user_instance,
            profile_img=profile_img,
            about_me=about_me
        )

        # 닉네임 업데이트
        user_instance.nickname = nickname
        user_instance.save()

        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, user_id):
        profile = get_object_or_404(Profile, user_id=user_id)
        serializer = ProfileSerializer(
            profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 비밀번호 변경
class UserPasswordChangeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        password = request.data.get('password')
        new_password = request.data.get('new_password')

        if user.check_password(password):

            user.set_password(new_password)
            user.save()

            return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'}, status=status.HTTP_200_OK)

        return Response({'message': '현재 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)


# 회원 탈퇴
class UserDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        password = request.data.get('password')

        if user.check_password(password):
            user.is_active = False
            user.save()
            return Response({'message': '회원 탈퇴가 성공적으로 이루어졌습니다.'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'message': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
