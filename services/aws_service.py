from typing import BinaryIO
from urllib.parse import quote

from services.settings import get_settings


def upload_file_to_s3(file_obj: BinaryIO, object_key: str) -> str:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError

    settings = get_settings()
    s3 = boto3.client("s3", region_name=settings.aws_region)

    extra_args = {}
    if settings.make_public:
        extra_args["ACL"] = "public-read"

    try:
        if extra_args:
            s3.upload_fileobj(
                file_obj,
                settings.bucket_name,
                object_key,
                ExtraArgs=extra_args,
            )
        else:
            s3.upload_fileobj(file_obj, settings.bucket_name, object_key)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError("Failed to upload file to S3") from exc

    encoded_key = quote(object_key)
    return f"https://{settings.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{encoded_key}"


def send_sns_notification(filename: str, file_url: str) -> None:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError

    settings = get_settings()
    sns = boto3.client("sns", region_name=settings.aws_region)
    message = f"New file uploaded: {filename}\nURL: {file_url}"

    try:
        sns.publish(
            TopicArn=settings.topic_arn,
            Message=message,
            Subject="File Upload Notification",
        )
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError("Failed to publish SNS notification") from exc