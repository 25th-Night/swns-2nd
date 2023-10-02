from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

from django_prometheus.models import ExportModelOperationsMixin

from common.models import CommonModel


class UserManager(BaseUserManager):
    def create_user(self, email, fullname, phone, password):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, phone=phone)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, phone, password):
        user = self.create_user(
            email=email,
            password=password,
            phone=phone,
            fullname=fullname,
        )

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(
    ExportModelOperationsMixin("user"), CommonModel, AbstractBaseUser, PermissionsMixin
):
    email = models.EmailField(verbose_name="이메일", max_length=100, unique=True)
    fullname = models.TextField(verbose_name="이름", max_length=30)
    phone = models.TextField(verbose_name="휴대폰번호", max_length=30, unique=True)
    password = models.CharField(verbose_name="비밀번호", max_length=100)
    is_admin = models.BooleanField(verbose_name="관리자여부", default=False)
    following = models.ManyToManyField(
        "self",
        verbose_name="팔로우",
        through="users.Follow",
        related_name="follower",
        symmetrical=False,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname", "phone", "password"]

    objects = UserManager()

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class Profile(ExportModelOperationsMixin("profile"), CommonModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="유저", related_name="profile"
    )
    nickname = models.TextField(verbose_name="닉네임", max_length=30, unique=True)
    birthday = models.DateField(verbose_name="생년월일")
    image_url = models.URLField(verbose_name="프로필사진", null=True, blank=True)
    is_public = models.BooleanField(verbose_name="공개여부", default=True)

    class Meta:
        verbose_name = "프로필"
        verbose_name_plural = "프로필 목록"
        indexes = [
            models.Index(fields=["-updated_at"]),
        ]
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.user}의 프로필"


class Follow(ExportModelOperationsMixin("follow"), models.Model):
    user_from = models.ForeignKey(
        "users.User",
        verbose_name="팔로우 한 유저",
        related_name="from_user",
        on_delete=models.CASCADE,
    )
    user_to = models.ForeignKey(
        "users.User",
        verbose_name="팔로우 받은 유저",
        related_name="to_user",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(verbose_name="생성일시", auto_now_add=True)

    class Meta:
        verbose_name = "팔로우 관계"
        verbose_name_plural = "팔로우 관계 목록"
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_from} follow {self.user_to}"
