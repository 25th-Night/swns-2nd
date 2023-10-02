from random import *

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from posts.models import Comment, Like, Post
from users.models import User


# TODO: 커맨드 활용
# https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/#testing
class Command(BaseCommand):
    help = "PUSH LIKE DB"

    def handle(self, *args, **options):
        post_like_count = 0
        comment_like_count = 0

        post_content_type = ContentType.objects.get_for_model(Post)
        post_list = list(Post.objects.all())

        comment_content_type = ContentType.objects.get_for_model(Comment)
        comment_list = list(Comment.objects.all())

        user_list = list(User.objects.all())

        for user in user_list:
            like_post_list = choices(
                post_list, k=choice(range(1, min(50, len(post_list))))
            )
            for like_post in like_post_list:
                content_type = post_content_type
                object_id = like_post.id
                user = user

                like, created = Like.objects.get_or_create(
                    content_type=content_type,
                    object_id=object_id,
                    user=user,
                )

                if created:
                    like_post.like_count += 1
                    like_post.save()
                    post_like_count += 1

            print(f"{post_like_count}개의 게시글 좋아요가 생성되었습니다.")

        for user in user_list:
            like_comment_list = choices(
                comment_list, k=choice(range(1, min(50, len(comment_list))))
            )
            for like_comment in like_comment_list:
                content_type = comment_content_type
                object_id = like_comment.id
                user = user

                like, created = Like.objects.get_or_create(
                    content_type=content_type,
                    object_id=object_id,
                    user=user,
                )

                if created:
                    like_comment.like_count += 1
                    like_comment.save()
                    comment_like_count += 1

            print(f"{comment_like_count}개의 댓글 좋아요가 생성되었습니다.")

        print(f"총 {post_like_count}개 게시글 좋아요 생성을 완료하였습니다.")
        print(f"총 {comment_like_count}개 댓글 좋아요 생성을 완료하였습니다.")
