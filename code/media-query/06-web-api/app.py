import os

import boto3
from chalice import Chalice
from chalicelib import db
from chalicelib import rekognition

app = Chalice(app_name='media-query')

_MEDIA_DB = None
_REKOGNITION_CLIENT = None
_SUPPORTED_IMAGE_EXTENSIONS = (
    '.jpg',
    '.png',
)


def get_media_db():
    global _MEDIA_DB
    if _MEDIA_DB is None:
        _MEDIA_DB = db.DynamoMediaDB(
            boto3.resource('dynamodb').Table(
                os.environ['MEDIA_TABLE_NAME']))
    return _MEDIA_DB


def get_rekognition_client():
    global _REKOGNITION_CLIENT
    if _REKOGNITION_CLIENT is None:
        _REKOGNITION_CLIENT = rekognition.RekognitonClient(
            boto3.client('rekognition'))
    return _REKOGNITION_CLIENT


@app.on_s3_event(bucket=os.environ['MEDIA_BUCKET_NAME'],
                 events=['s3:ObjectCreated:*'])
def handle_object_created(event):
    if _is_image(event.key):
        _handle_created_image(bucket=event.bucket, key=event.key)


@app.on_s3_event(bucket=os.environ['MEDIA_BUCKET_NAME'],
                 events=['s3:ObjectRemoved:*'])
def handle_object_removed(event):
    if _is_image(event.key):
        get_media_db().delete_media_file(event.key)


def _is_image(key):
    return key.endswith(_SUPPORTED_IMAGE_EXTENSIONS)


def _handle_created_image(bucket, key):
    labels = get_rekognition_client().get_image_labels(bucket=bucket, key=key)
    get_media_db().add_media_file(key, media_type=db.IMAGE_TYPE, labels=labels)
