from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.constraints import UniqueConstraint

from taggit.managers import TaggableManager

from django_prometheus.models import ExportModelOperationsMixin

from common.models import CommonModel


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(status=Post.StatusChoices.PUBLISHED, is_active=True)
        )


class Post(ExportModelOperationsMixin("post"), CommonModel):
    class StatusChoices(models.IntegerChoices):
        DRAFT = 0
        PUBLISHED = 1

    title = models.TextField(verbose_name="제목", max_length=250)
    slug = models.SlugField(
        verbose_name="슬러그",
        max_length=250,
        unique=True,
        allow_unicode=True,
        unique_for_date="publish",
    )
    author = models.ForeignKey(
        "users.User",
        verbose_name="작성자",
        on_delete=models.CASCADE,
        related_name="posts",
    )
    body = models.TextField(verbose_name="본문")
    status = models.IntegerField(
        verbose_name="게시상태", default=0, choices=StatusChoices.choices
    )
    publish = models.DateTimeField(default=timezone.now)

    tags = TaggableManager()
    likes = GenericRelation("posts.Like", related_query_name="posts")
    like_count = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
            models.Index(fields=["-like_count"]),
        ]

    def __str__(self):
        return f"{self.title[:10]}.." if len(self.title) > 10 else self.title

    def unique_slug_generator(self, new_slug=None):
        slug = slugify(self.title, allow_unicode=True)
        new_slug = slug
        numb = 1
        while Post.objects.filter(slug=new_slug).exists():
            new_slug = "{slug}-{num}".format(slug=slug, num=numb)
            numb += 1
        return new_slug

    def save(self, *args, **kwargs):
        self.slug = self.unique_slug_generator()
        super().save(*args, **kwargs)


class Comment(ExportModelOperationsMixin("comment"), CommonModel):
    post = models.ForeignKey(
        Post, verbose_name="게시글", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        "users.User",
        verbose_name="작성자",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    body = models.TextField(verbose_name="본문")
    likes = GenericRelation("posts.Like", related_query_name="comments")
    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["-like_count"]),
        ]

    def __str__(self):
        return f"{self.body[:10]}.." if len(self.body) > 10 else self.body


class Image(ExportModelOperationsMixin("image"), models.Model):
    name = models.TextField(verbose_name="제목", max_length=50)
    post = models.ForeignKey(
        Post, verbose_name="게시글", on_delete=models.CASCADE, related_name="images"
    )
    author = models.ForeignKey(
        "users.User",
        verbose_name="작성자",
        on_delete=models.CASCADE,
        related_name="images",
    )
    image_url = models.URLField(verbose_name="이미지", null=True, blank=True)
    is_active = models.BooleanField(verbose_name="활성 여부", default=True)
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)

    class Meta:
        verbose_name = "이미지"
        verbose_name_plural = "이미지 목록"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"{self.post} - {self.name}"


class Like(ExportModelOperationsMixin("like"), models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="content type",
        related_name="%(app_label)s_%(class)s_likes",
    )
    object_id = models.IntegerField(verbose_name="object ID", db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(
        "users.User",
        verbose_name="좋아요 누른 사람",
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)

    class Meta:
        verbose_name = "좋아요"
        verbose_name_plural = "좋아요 목록"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            UniqueConstraint(
                fields=["content_type", "object_id", "user"],
                name="unique_like",
            ),
        ]

    def __str__(self):
        return f"{self.user} like {self.content_type.model}//-{self.object_id}"
