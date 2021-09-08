
import decimal
import os
import json

import boto3


s3 = boto3.resource('s3')
S3_BUCKET = os.getenv("S3_BUCKET")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))


def list(event, context):

    # fetch all coupons from the dynamodb
    result = table.scan()

    body = json.dumps(result['Items'], cls=decimal_encoder, ensure_ascii=False)
    ids = [int(i["id"]) for i in result["Items"]]

    ids = []
    for i in result["Items"]:
        i["id"] = format(int(i["id"]), '07')
        ids.append(i['id'])

    # create a response
    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": body
    }

    return response


def post(event, context):
    result = table.scan()

    # 7-digit zero-filled ID
    max_id = max([i["id"] for i in result["Items"]]) if result["Items"] else '0'
    file_id = format(int(max_id) + 1, '07')

    s3.Bucket(S3_BUCKET).upload_file(f"{S3_BUCKET}/coupon-img-1/coupon-img-1.png", f"coupon-img-{file_id}/coupon-img-{file_id}.png")
    s3.Bucket(S3_BUCKET).upload_file(f"{S3_BUCKET}/coupon-img-1/qr-code-coupon-img-1.png", f"coupon-img-{file_id}/qr-code-coupon-img-{file_id}.png")

    path = f"coupon-images/coupon-img-{file_id}/"

    table.put_item(
        Item={
            'id': file_id,
            'title': f'クーポン{file_id}',
            'path': path,
            'description': f'クーポン{file_id}' * 5,
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }


class decimal_encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(decimal_encoder, self).default(obj)
