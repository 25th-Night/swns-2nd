from random import *

from django.core.management.base import BaseCommand

from faker import Faker

from users.models import User


# TODO: 커맨드 활용
# https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/#testing
class Command(BaseCommand):
    help = "PUSH FOLLOW DB"

    def handle(self, *args, **options):
        fake = Faker(locale="ko_KR")

        users = User.objects.all()
        count = 0

        for user in users:
            other_user = User.objects.exclude(id=user.id)
            other_user_count = other_user.count()
            random_count = choice(range(1, other_user_count + 1))
            following_users = choices(list(other_user), k=random_count)

            user.following.add(*following_users)

            count += len(following_users)

            print(f"{user.id}번 유저가 {following_users} 해당 유저들을 follow 하였습니다.")

        print(f"총 {count}개의 팔로우 생성을 완료하였습니다.")
