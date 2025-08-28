import boto3
from botocore.exceptions import ClientError

# DynamoDB Local 接続設定（コンテナ内から接続する）
dynamodb = boto3.client(
    "dynamodb",
    region_name="ap-northeast-1",
    endpoint_url="http://dynamodb:8000",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)

def create_table(table_name, key_schema, attribute_definitions):
    try:
        resp = dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            BillingMode="PAY_PER_REQUEST",
        )
        print(f"✅ Created table: {table_name}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"⚠️ Table already exists: {table_name}")
        else:
            print(f"❌ Error creating {table_name}: {e}")

def main():
    # Admins テーブル（認証用）
    create_table(
        "Admins",
        key_schema=[{"AttributeName": "cognito_sub", "KeyType": "HASH"}],
        attribute_definitions=[{"AttributeName": "cognito_sub", "AttributeType": "S"}],
    )

    # Settings テーブル
    create_table(
        "Settings",
        key_schema=[{"AttributeName": "id", "KeyType": "HASH"}],
        attribute_definitions=[{"AttributeName": "id", "AttributeType": "S"}],
    )

    # Templates テーブル
    create_table(
        "Templates",
        key_schema=[
            {"AttributeName": "PK", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        attribute_definitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
        ],
    )

    # Posts テーブル
    create_table(
        "Posts",
        key_schema=[{"AttributeName": "id", "KeyType": "HASH"}],
        attribute_definitions=[{"AttributeName": "id", "AttributeType": "S"}],
    )

    # Article_link_clicks テーブル
    create_table(
        "Article_link_clicks",
        key_schema=[{"AttributeName": "id", "KeyType": "HASH"}],
        attribute_definitions=[{"AttributeName": "id", "AttributeType": "S"}],
    )

    # Static_link_clicks テーブル
    create_table(
        "Static_link_clicks",
        key_schema=[{"AttributeName": "id", "KeyType": "HASH"}],
        attribute_definitions=[{"AttributeName": "id", "AttributeType": "S"}],
    )

    # API_status テーブル
    create_table(
        "API_status",
        key_schema=[{"AttributeName": "id", "KeyType": "HASH"}],
        attribute_definitions=[{"AttributeName": "id", "AttributeType": "S"}],
    )

if __name__ == "__main__":
    main()
