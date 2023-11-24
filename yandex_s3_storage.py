from storages.backends.s3boto3 import S3Boto3Storage
from sports_events.settings import YANDEX_BUCKET_NAME


class MediaStorage(S3Boto3Storage):
    bucket_name = YANDEX_BUCKET_NAME
    file_overwrite = False
