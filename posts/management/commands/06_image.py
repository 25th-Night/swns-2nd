from random import *

from django.core.management.base import BaseCommand

from faker import Faker

from posts.models import Image, Post
from users.models import User


# TODO: 커맨드 활용
# https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/#testing
class Command(BaseCommand):
    help = "PUSH IMAGE DB"

    def handle(self, *args, **options):
        fake = Faker(locale="ko_KR")

        # 생성할 이미지 수
        number = int(input("생성할 이미지 수를 입력하세요 :  "))
        created = 0

        post_list = list(Post.objects.all())
        author_list = list(User.objects.all())

        while created != number:
            name = fake.word()
            post = choice(post_list)
            author = choice(author_list)
            image_url = fake.image_url()

            image = Image.objects.create(
                name=name,
                post=post,
                author=author,
                image_url=image_url,
            )

            created += 1

            print(f"{created}개의 이미지가 생성되었습니다.")

        print(f"총 {number}개 이미지의 생성을 완료하였습니다.")
