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

def create_table_if_not_exists(table_name, key_schema, attribute_definitions, billing_mode="PAY_PER_REQUEST"):
    try:
        existing_tables = dynamodb_client.list_tables()["TableNames"]
        if table_name in existing_tables:
            print(f"既にテーブルが存在します: {table_name}")
            return

        dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            BillingMode=billing_mode
        )
        print(f"テーブルを作成しました: {table_name}")

    except ClientError as e:
        print(f"DynamoDB操作中にエラーが発生しました: {e.response['Error']['Message']}")
        raise

if __name__ == "__main__":
    create_table_if_not_exists(
        table_name=os.environ.get("SETTINGS_TABLE_NAME", "SettingsTable"),
        key_schema=[
            {"AttributeName": "id", "KeyType": "HASH"}
        ],
        attribute_definitions=[
            {"AttributeName": "id", "AttributeType": "S"}
        ]
    )
