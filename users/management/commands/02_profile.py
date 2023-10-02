from random import *

from django.core.management.base import BaseCommand

from faker import Faker

from users.models import Profile, User


# TODO: 커맨드 활용
# https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/#testing
class Command(BaseCommand):
    help = "PUSH PROFILE DB"

    def handle(self, *args, **options):
        fake = Faker(locale="ko_KR")

        users = User.objects.all()

        # Create Profile objects
        for user in users:
            if not Profile.objects.filter(user=user).exists():
                nickname = fake.user_name()
                while nickname in Profile.objects.all().values_list(
                    "nickname", flat=True
                ):
                    nickname = fake.user_name()
                birthday = fake.date_of_birth(minimum_age=15, maximum_age=80)
                image_url = fake.image_url()

                profile, created = Profile.objects.get_or_create(
                    user=user, nickname=nickname, birthday=birthday, image_url=image_url
                )

                if created:
                    print(f"{user.id}번 유저 {nickname}님의 프로필 생성을 완료하였습니다.")

        print(
            f"모든 유저의 프로필 생성 완료 유무 : {User.objects.count() == Profile.objects.count()}"
        )
