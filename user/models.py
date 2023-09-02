from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):

        if not username:
            raise TypeError('User must have a username.')

        if not email:
            raise ValueError('User must have an email address.')

        if not password:
            raise TypeError('User must have a password.')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # create_user
    def create_user(self, username, email, password, **extra_fields):

        return self._create_user(username, email, password, False, False, True, **extra_fields)

    # create_superuser
    def create_superuser(self, username, email, password, **extra_fields):

        return self._create_user(username, email, password, True, True, True, **extra_fields)


class User(AbstractUser):
    username = models.CharField("아이디", max_length=30, unique=True)
    email = models.EmailField("이메일주소", unique=True, max_length=255)
    is_staff = models.BooleanField("관리자권한", default=False)
    is_superuser = models.BooleanField("관리자", default=False)
    is_active = models.BooleanField("계정활성화", default=True)
    last_login = models.DateTimeField("마지막 로그인 시간", null=True, blank=True)
    date_joined = models.DateTimeField("가입일", auto_now_add=True)
    nickname = models.CharField(
        "닉네임", max_length=20, unique=True, null=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'nickname']

    objects = UserManager()

    def __str__(self):
        return f"{self.username} / {self.email}"


class Profile(models.Model):
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE)
    profile_img = models.ImageField(
        "프로필이미지", upload_to='profile/', null=True, blank=True)
    about_me = models.TextField("자기소개", null=True, blank=True)
    updated_at = models.DateTimeField(
        "최근프로필수정일", auto_now=True)

    def __str__(self):
        return f"{self.user}"
