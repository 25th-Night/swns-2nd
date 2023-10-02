from random import *

from django.core.management.base import BaseCommand

from faker import Faker

from posts.models import Comment, Post
from users.models import User


# TODO: 커맨드 활용
# https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/#testing
class Command(BaseCommand):
    help = "PUSH COMMENT DB"

    def handle(self, *args, **options):
        fake = Faker(locale="ko_KR")

        # 생성할 comment 수
        number = int(input("생성할 댓글 수를 입력하세요 :  "))
        created = 0

        post_list = list(Post.objects.all())
        author_list = list(User.objects.all())
        body_list = [fake.paragraph(nb_sentences=4) for _ in range(200)]

        while created != number:
            post = choice(post_list)
            author = choice(author_list)
            body = choice(body_list)

            comment = Comment.objects.create(
                post=post,
                author=author,
                body=body,
            )

            created += 1

            print(f"{created}개의 댓글이 생성되었습니다.")

        print(f"총 {number}개 댓글의 생성을 완료하였습니다.")
