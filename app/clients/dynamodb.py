import boto3
from boto3.dynamodb.conditions import Key
from core.config import settings
from datetime import datetime

# テーブル名
ADMIN_TABLE_NAME = settings.ADMIN_TABLE_NAME
SETTINGS_TABLE_NAME = "SettingsTable"
TEMPLATES_TABLE_NAME = "TemplatesTable"

# boto3 DynamoDB クライアント
dynamodb = boto3.resource(
    "dynamodb",
    region_name=settings.AWS_REGION,
    endpoint_url=settings.DYNAMODB_ENDPOINT,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)

# テーブルの定義
post_table = dynamodb.Table(ADMIN_TABLE_NAME)
settings_table = dynamodb.Table(SETTINGS_TABLE_NAME)
templates_table = dynamodb.Table(TEMPLATES_TABLE_NAME)

# 投稿データ取得
def get_post_data():
    try:
        response = post_table.scan()
        items = response.get("Items", [])
        return items
    except Exception as e:
        print(f"DynamoDBからの投稿データ取得に失敗しました: {e}")
        return []

# 設定取得
def get_settings_data():
    try:
        response = settings_table.get_item(Key={"id": "app_settings"})
        item = response.get("Item", {})

        # 必須フィールドがない場合はデフォルト値を補完
        return {
            "id": item.get("id", "app_settings"),
            "check_interval": item.get("check_interval", 60),
            "excluded_users": item.get("excluded_users", []),
            "excluded_keywords": item.get("excluded_keywords", []),
            "trial_class_link": item.get("trial_class_link", ""),
            "counseling_link": item.get("counseling_link", ""),
            "last_checked_at": item.get("last_checked_at", datetime.utcnow().isoformat())
        }
    except Exception as e:
        print(f"設定データの取得に失敗しました: {e}")
        return {
            "id": "app_settings",
            "check_interval": 60,
            "excluded_users": [],
            "excluded_keywords": [],
            "trial_class_link": "",
            "counseling_link": "",
            "last_checked_at": datetime.utcnow().isoformat()
        }

# 設定更新
def update_settings_data(data: dict):
    try:
        data["id"] = "app_settings"
        settings_table.put_item(Item=data)
        return True
    except Exception as e:
        print(f"設定データの更新に失敗しました: {e}")
        return False

# テンプレート一覧取得
def get_templates_data():
    try:
        response = templates_table.scan()
        return response.get("Items", [])
    except Exception as e:
        print(f"テンプレート一覧の取得に失敗しました: {e}")
        return []

# テンプレート作成
def create_template_data(template: dict):
    try:
        templates_table.put_item(Item=template)
        return {"message": "テンプレートを登録しました。"}
    except Exception as e:
        print(f"テンプレートの作成に失敗しました: {e}")
        return {"message": "テンプレートの作成に失敗しました。"}

# テンプレート更新
def update_template_data(template_id: str, template: dict):
    try:
        templates_table.put_item(Item={**template, "id": template_id})
        return {"message": "テンプレートを更新しました。"}
    except Exception as e:
        print(f"テンプレートの更新に失敗しました: {e}")
        return {"message": "テンプレートの更新に失敗しました。"}

# テンプレート削除
def delete_template_data(template_id: str):
    try:
        templates_table.delete_item(Key={"id": template_id})
        return {"message": "テンプレートを削除しました。"}
    except Exception as e:
        print(f"テンプレートの削除に失敗しました: {e}")
        return {"message": "テンプレートの削除に失敗しました。"}
