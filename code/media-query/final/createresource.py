import os
import uuid
import json
import argparse

import boto3


def create_resource(resource_type, stage):
    resource_name = 'media-query-%s' % str(uuid.uuid4())
    if resource_type == 'bucket':
        create_bucket(resource_name)
        record_as_env_var('MEDIA_BUCKET_NAME', resource_name, stage)
    elif resource_type == 'table':
        create_table(resource_name)
        record_as_env_var('MEDIA_TABLE_NAME', resource_name, stage)
    elif resource_type == 'topic':
        topic_arn, role_arn = create_topic_with_role(resource_name)
        record_as_env_var('VIDEO_TOPIC_NAME', resource_name, stage)
        record_as_env_var('VIDEO_TOPIC_ARN', topic_arn, stage)
        record_as_env_var('VIDEO_ROLE_ARN', role_arn, stage)
    print('Created %s resource: %s' % (resource_type, resource_name))


def create_bucket(bucket_name):
    s3 = boto3.client('s3')
    client_params = {
        'Bucket': bucket_name
    }
    if s3.meta.region_name not in [None, 'us-east-1']:
        client_params['CreateBucketConfiguration'] = {
            'LocationConstraint': s3.meta.region_name
        }

    s3.create_bucket(**client_params)


def create_table(table_name):
    client = boto3.client('dynamodb')
    key_schema = [
        {
            'AttributeName': 'name',
            'KeyType': 'HASH',
        }
    ]
    attribute_definitions = [
        {
            'AttributeName': 'name',
            'AttributeType': 'S',
        }
    ]
    client.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    )
    waiter = client.get_waiter('table_exists')
    waiter.wait(TableName=table_name, WaiterConfig={'Delay': 1})


def create_topic_with_role(topic_name):
    topic_arn = _create_sns_topic(topic_name)
    role_arn = _create_iam_role(role_name=topic_name, topic_arn=topic_arn)
    return topic_arn, role_arn


def _create_sns_topic(topic_name):
    client = boto3.client('sns')
    response = client.create_topic(Name=topic_name)
    return response['TopicArn']


def _create_iam_role(role_name, topic_arn):
    client = boto3.client('iam')
    response = client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(
            {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Principal': {
                            'Service': 'rekognition.amazonaws.com'
                        },
                        'Action': 'sts:AssumeRole',
                        'Condition': {}
                    }
                ]
            }
        )
    )
    client.put_role_policy(
            RoleName=role_name,
            PolicyName=role_name,
            PolicyDocument=json.dumps(
                {
                    'Version': '2012-10-17',
                    'Statement': [
                        {
                            'Action': [
                                'sns:Publish'
                            ],
                            'Effect': 'Allow',
                            'Resource': topic_arn
                        }
                    ]
                }
            )
    )
    return response['Role']['Arn']


def _get_random_resource_name():
    return 'media-query-%s' % str(uuid.uuid4())


def record_as_env_var(key, value, stage):
    with open(os.path.join('.chalice', 'config.json')) as f:
        data = json.load(f)
        data['stages'].setdefault(stage, {}).setdefault(
            'environment_variables', {}
        )[key] = value
    with open(os.path.join('.chalice', 'config.json'), 'w') as f:
        serialized = json.dumps(data, indent=2, separators=(',', ': '))
        f.write(serialized + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stage', default='dev')
    parser.add_argument(
        '-t', '--type', required=True, choices=['bucket', 'table', 'topic'])
    args = parser.parse_args()
    create_resource(resource_type=args.type, stage=args.stage)


if __name__ == '__main__':
    main()
