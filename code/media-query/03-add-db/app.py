import boto3
from chalice import Chalice
from chalicelib import rekognition

app = Chalice(app_name='media-query')

_REKOGNITION_CLIENT = None


def get_rekognition_client():
    global _REKOGNITION_CLIENT
    if _REKOGNITION_CLIENT is None:
        _REKOGNITION_CLIENT = rekognition.RekognitonClient(
            boto3.client('rekognition'))
    return _REKOGNITION_CLIENT


@app.lambda_function()
def detect_labels_on_image(event, context):
    bucket = event['Bucket']
    key = event['Key']
    return get_rekognition_client().get_image_labels(bucket=bucket, key=key)
