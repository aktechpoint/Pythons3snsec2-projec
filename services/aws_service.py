import boto3

s3 = boto3.client('s3', region_name='ap-northeast-1')
sns = boto3.client('sns', region_name='ap-northeast-1')

BUCKET_NAME = 'rjalalaclasssss'
TOPIC_ARN = 'arn:aws:sns:ap-northeast-1:668425683981:myfirsttopic'

def upload_file_to_s3(file, filename):
    s3.upload_fileobj(
        file,
        BUCKET_NAME,
        filename,
        ExtraArgs={'ACL': 'public-read'}
    )
    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

def send_sns_notification(filename, file_url):
    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=f"New file uploaded: {filename}\nURL: {file_url}",
        Subject="File Upload Notification"
    )