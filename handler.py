from base64 import b64decode, b64encode

import decimal
import os
import json

import boto3


s3 = boto3.resource('s3')
S3_BUCKET = os.getenv("S3_BUCKET")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))


def get(event, context):
    path = event.get('pathParameters')
    coupon_id = path['id']
    coupon_title = path['title']

    # fetch coupon from the dynamodb
    result = table.get_item(
        Key={
            'id': coupon_id, 'title': coupon_title
        }
    )

    coupon_img_obj = s3.Object(S3_BUCKET, f'coupon-img-{coupon_id}/coupon-img-{coupon_id}.png')
    coupon_img_data = coupon_img_obj.get()['Body'].read()
    coupon_img_base64 = b64encode(coupon_img_data)

    qr_code_img_obj = s3.Object(S3_BUCKET, f'coupon-img-{coupon_id}/coupon-img-{coupon_id}.png')
    qr_code_img_data = qr_code_img_obj.get()['Body'].read()
    qr_code_img_base64 = b64encode(qr_code_img_data)

    body = result.get('Item', {
        'id': coupon_id,
        'title': coupon_title
    })

    body.update(
        {
            'base64CouponImg': coupon_img_base64.decode(),
            'base64QrCodeImg': qr_code_img_base64.decode(),
            'dynamodbResult': result
        }
    )

    response_body = json.dumps(body, cls=decimal_encoder, ensure_ascii=False)

    # create a response
    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": response_body
    }

    return response


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

    img_string = event.get("body", "")
    body_dict = json.loads(img_string)

    base64_coupon_img = body_dict['couponImg'][22:]
    encode_coupon_img = base64_coupon_img.encode()

    base64_qr_code_img = body_dict['qrCodeImg'][22:]
    encode_qr_code_img = base64_qr_code_img.encode()

    coupon_title = body_dict['couponTitle']

    coupon_description = body_dict['couponDescription']

    result = table.scan()

    # 7-digit zero-filled ID
    max_id = max([i["id"] for i in result["Items"]]) if result["Items"] else '0'
    file_id = format(int(max_id) + 1, '07')

    # save the coupon img to s3
    s3_coupon_img_object = s3.Object(S3_BUCKET, f"coupon-img-{file_id}/coupon-img-{file_id}.png")
    s3_coupon_img_object.put(Body=b64decode(encode_coupon_img))

    # save the qr code img to s3
    s3_qr_code_img_object = s3.Object(S3_BUCKET, f"coupon-img-{file_id}/qr-code-coupon-img-{file_id}.png")
    s3_qr_code_img_object.put(Body=b64decode(encode_qr_code_img))

    path = f"coupon-images/coupon-img-{file_id}/"

    table.put_item(
        Item={
            'id': file_id,
            'title': coupon_title,
            'path': path,
            'description': coupon_description,
        }
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Success!')
    }


class decimal_encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(decimal_encoder, self).default(obj)
