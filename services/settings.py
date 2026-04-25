import os
from dataclasses import dataclass


def _read_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value.strip() == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


@dataclass(frozen=True)
class Settings:
    aws_region: str
    bucket_name: str
    topic_arn: str
    max_upload_mb: int
    allowed_extensions: tuple[str, ...]
    make_public: bool


def get_settings() -> Settings:
    raw_extensions = os.getenv(
        "ALLOWED_EXTENSIONS",
        ".txt,.pdf,.png,.jpg,.jpeg,.gif,.csv,.json",
    )
    extensions = tuple(
        ext.strip().lower() for ext in raw_extensions.split(",") if ext.strip()
    )

    return Settings(
        aws_region=os.getenv("AWS_REGION", "ap-northeast-1"),
        bucket_name=_read_env("S3_BUCKET_NAME"),
        topic_arn=_read_env("SNS_TOPIC_ARN"),
        max_upload_mb=int(os.getenv("MAX_UPLOAD_MB", "10")),
        allowed_extensions=extensions,
        make_public=os.getenv("S3_MAKE_PUBLIC", "false").lower() == "true",
    )
