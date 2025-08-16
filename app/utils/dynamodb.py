import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import boto3

load_dotenv()

print("=== ENV DEBUG ===")
print("AWS_REGION:", os.environ.get("AWS_REGION"))
print("DYNAMODB_ENDPOINT:", os.environ.get("DYNAMODB_ENDPOINT"))
print("AWS_ACCESS_KEY_ID:", os.environ.get("AWS_ACCESS_KEY_ID"))
print("AWS_SECRET_ACCESS_KEY:", os.environ.get("AWS_SECRET_ACCESS_KEY"))
print("=================")

dynamodb_client = boto3.client(
    "dynamodb",
    region_name=os.environ["AWS_REGION"],
    endpoint_url=os.environ["DYNAMODB_ENDPOINT"],
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy"
)

def create_table_if_not_exists(**kwargs):
    table_name = kwargs["TableName"]
    try:
        existing_tables = dynamodb_client.list_tables()["TableNames"]
        if table_name in existing_tables:
            print(f"既にテーブルが存在します: {table_name}")
            return
        dynamodb_client.create_table(**kwargs)
        print(f"テーブルを作成しました: {table_name}")
    except ClientError as e:
        print(f"DynamoDB操作中にエラーが発生しました: {e.response['Error']['Message']}")
        raise

if __name__ == "__main__":
    # SettingsTable: PK=id
    create_table_if_not_exists(
        TableName=os.environ.get("SETTINGS_TABLE_NAME", "SettingsTable"),
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    # AdminsTable: PK=id, GSI=cognito_sub-index
    create_table_if_not_exists(
        TableName=os.environ.get("ADMIN_TABLE_NAME", "AdminsTable"),
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
            {"AttributeName": "cognito_sub", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "cognito_sub-index",
                "KeySchema": [{"AttributeName": "cognito_sub", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            }
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    # TemplatesTable: PK=id, GSI=is_active-index (Number)
    create_table_if_not_exists(
        TableName=os.environ.get("TEMPLATES_TABLE_NAME", "TemplatesTable"),
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
            {"AttributeName": "is_active", "AttributeType": "N"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "is_active-index",
                "KeySchema": [{"AttributeName": "is_active", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            }
        ],
        BillingMode="PAY_PER_REQUEST",
    )
