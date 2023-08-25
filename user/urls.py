from django.urls import path, include
from user import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user import views

urlpatterns = [
    path('register/', views.UserRegisterAPIView.as_view()),
    path('auth/', views.AuthAPIView.as_view()),
    path('profile/<int:user_id>/', views.ProfileView.as_view()),
    path('profile/<int:user_id>/create', views.ProfileCreateView.as_view()),
    path('password/int:user_id/change/', views.UserPasswordChangeAPIView.as_view(), name='user_password_change'),
    path('/int:user_id/delete/', views.UserDeleteAPIView.as_view(), name='user_delete'),

    # simplejwt 에서 제공하는 기본 JWT 인증
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
