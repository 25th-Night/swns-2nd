from random import *

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from faker import Faker

from users.models import User


# TODO: 커맨드 활용
# https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/#testing
class Command(BaseCommand):
    help = "PUSH USER DB"

    def handle(self, *args, **options):
        # 생성할 user 수
        number = int(input("생성할 유저 수를 입력하세요 :  "))
        created = 0

        # email
        def generate_random_email():
            domain_type = [
                "naver.com",
                "google.com",
                "kakao.com",
                "icloud.com",
                "hanmail.net",
                "daum.net",
                "nate.com",
                "outlook.com",
                "hotmail.com",
                "yahoo.com",
            ]
            email = f"{Faker().user_name()}@{choice(domain_type)}"

            return email

        # fullname
        def generate_random_korean_fullname():
            fullname = Faker(locale="ko_KR").name()

            return fullname

        # phone
        def generate_random_phone():
            start = "010"
            middle = str(randrange(2000, 10000))
            end = str(randrange(0, 10000)).zfill(4)

            phone = f"{start}-{middle}-{end}"

            return phone

        # password
        new_password = make_password("1234")

        # Create User objects
        while created != number:
            email = generate_random_email()
            fullname = generate_random_korean_fullname()
            phone = generate_random_phone()
            password = new_password
            try:
                User.objects.get_or_create(
                    email=email, fullname=fullname, password=password, phone=phone
                )
                created += 1

                print(f"{created}명의 유저 계정이 생성되었습니다.")
            except:
                continue

        print(f"총 {created}명의 유저 계정 생성을 완료하였습니다.")
