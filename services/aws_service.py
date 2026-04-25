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


def list_objects() -> list[dict[str, str]]:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError

    settings = get_settings()
    s3 = boto3.client("s3", region_name=settings.aws_region)
    prefix = settings.object_prefix

    try:
        response = s3.list_objects_v2(Bucket=settings.bucket_name, Prefix=prefix)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError("Failed to list S3 objects") from exc

    items: list[dict[str, str]] = []
    for obj in response.get("Contents", []):
        key = obj.get("Key")
        if not key or key.endswith("/"):
            continue
        items.append(
            {
                "key": key,
                "name": key.split("/")[-1],
                "size": str(obj.get("Size", 0)),
            }
        )
    return items


def generate_download_url(object_key: str) -> str:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError

    settings = get_settings()
    s3 = boto3.client("s3", region_name=settings.aws_region)

    try:
        return s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.bucket_name, "Key": object_key},
            ExpiresIn=settings.download_expiry_seconds,
        )
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError("Failed to generate download URL") from exc


def delete_object(object_key: str) -> None:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError

    settings = get_settings()
    s3 = boto3.client("s3", region_name=settings.aws_region)

    try:
        s3.delete_object(Bucket=settings.bucket_name, Key=object_key)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError("Failed to delete S3 object") from exc