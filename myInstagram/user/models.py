from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
class User(AbstractBaseUser):
    """
    유저 프로필 사진
    유저 아이디      -> 화면에 표기되는 유저 아이디
    유저 이름       -> 실제 사용자 이름
    유저 이메일      -> 로그인 정보
    유저 비밀번호    -> 로그인 정보, 디폴트 사용
    """

    profile_img = models.TextField()
    nickname = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'nickname'

    class Meta:
        db_table = "User"