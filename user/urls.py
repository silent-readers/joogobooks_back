from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from user import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 회원가입
    path('register/', views.UserRegisterAPIView.as_view()),

    # 로그인, 로그아웃, 회원정보 조회
    path('auth/', views.AuthAPIView.as_view()),

    # 비밀번호 변경
    path('auth/<int:user_id>/changepassword/',
         views.UserPasswordChangeAPIView.as_view()),

    # 회원탈퇴
    path('auth/<int:user_id>/delete/', views.UserDeleteAPIView.as_view()),

    # 프로필 조회
    path('profile/<int:user_id>/', views.ProfileView.as_view()),

    # 프로필 생성
    path('profile/<int:user_id>/create', views.ProfileCreateView.as_view()),

    # 프로필 업데이트
    path('profile/<int:user_id>/update', views.ProfileUpdateView.as_view()),

    # simplejwt 에서 제공하는 기본 JWT 인증
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
