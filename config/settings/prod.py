import os

from .base import *


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = False

# ALLOWED_HOSTS = [
#     os.getenv("NCP_LB_DOMAIN"),
# ]

# CSRF_TRUSTED_ORIGINS = [
#     f"http://{os.getenv('NCP_LB_DOMAIN')}",
# ]

INSTALLED_APPS += [
    "storages",
]


# S3
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com"
AWS_DEFAULT_ACL = "public-read"
DEFAULT_FILE_STORAGE = "config.storages.S3DefaultStorage"
STATICFILES_STORAGE = "config.storages.S3StaticStorage"
