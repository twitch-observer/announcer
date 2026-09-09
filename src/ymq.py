import json

import boto3

from settings import settings

sqs = boto3.client(
    service_name="sqs",
    endpoint_url="https://message-queue.api.cloud.yandex.net",
    region_name="ru-central1",
    aws_access_key_id=settings.cloud.ymq_access_key,
    aws_secret_access_key=settings.cloud.ymq_secret_key.get_secret_value(),
)


def send_to_ymq(body):
    sqs.send_message(
        QueueUrl=settings.cloud.ymq_queue_url,
        MessageBody=json.dumps(body),
    )
