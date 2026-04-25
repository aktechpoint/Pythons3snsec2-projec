import io

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_success(monkeypatch):
    monkeypatch.setenv("S3_BUCKET_NAME", "demo-bucket")
    monkeypatch.setenv("SNS_TOPIC_ARN", "arn:aws:sns:ap-northeast-1:123456789012:topic")
    monkeypatch.setenv("ALLOWED_EXTENSIONS", ".txt")
    monkeypatch.setenv("MAX_UPLOAD_MB", "2")

    def fake_upload(file_obj, object_key):
        assert object_key.startswith("uploads/")
        return "https://example.com/uploads/test.txt"

    def fake_notify(filename, file_url):
        assert filename == "test.txt"
        assert file_url.startswith("https://example.com/")

    monkeypatch.setattr("controllers.upload_controller.upload_file_to_s3", fake_upload)
    monkeypatch.setattr("controllers.upload_controller.send_sns_notification", fake_notify)

    response = client.post(
        "/",
        files={"file": ("test.txt", io.BytesIO(b"hello world"), "text/plain")},
    )
    assert response.status_code == 200
    assert "File uploaded successfully!" in response.text


def test_upload_rejects_bad_extension(monkeypatch):
    monkeypatch.setenv("S3_BUCKET_NAME", "demo-bucket")
    monkeypatch.setenv("SNS_TOPIC_ARN", "arn:aws:sns:ap-northeast-1:123456789012:topic")
    monkeypatch.setenv("ALLOWED_EXTENSIONS", ".txt")

    response = client.post(
        "/",
        files={"file": ("image.exe", io.BytesIO(b"binary"), "application/octet-stream")},
    )
    assert response.status_code == 200
    assert "Unsupported file extension" in response.text
