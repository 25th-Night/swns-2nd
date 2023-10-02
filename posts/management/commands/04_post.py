from random import *

from django.core.management.base import BaseCommand

from faker import Faker

from posts.models import Post
from users.models import User


# TODO: 커맨드 활용
# https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/#testing
class Command(BaseCommand):
    help = "PUSH POST DB"

    def handle(self, *args, **options):
        fake = Faker(locale="ko_KR")

        # 생성할 post 수
        number = int(input("생성할 게시글 수를 입력하세요 :  "))
        created = 0

        title_list = [fake.sentence(nb_words=10) for _ in range(30)]
        author_list = list(User.objects.all())
        body_list = [fake.paragraph(nb_sentences=10) for _ in range(50)]
        tag_list = [str(i) + "월" for i in range(1, 13)]

        while created != number:
            title = choice(title_list)
            author = choice(author_list)
            body = choice(body_list)
            status = choices([0, 1], weights=[1, 7], k=1)[0]
            tags = choices(tag_list, k=choice(range(0, 6)))

            if Post.objects.filter(title=title, author=author, body=body).exists():
                continue

            post = Post.objects.create(
                title=title, author=author, body=body, status=status
            )
            post.tags.add(*tags)

            created += 1

            print(f"{created}개의 게시글이 생성되었습니다.")

        print(f"총 {number}개 게시글의 생성을 완료하였습니다.")
