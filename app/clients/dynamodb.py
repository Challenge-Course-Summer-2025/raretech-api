import boto3
from boto3.dynamodb.conditions import Key
from core.config import settings
from datetime import datetime
from typing import Dict, Any, List

# テーブル名
ADMIN_TABLE_NAME = settings.ADMIN_TABLE_NAME
SETTINGS_TABLE_NAME = "SettingsTable"
TEMPLATES_TABLE_NAME = "TemplatesTable"
POSTS_TABLE_NAME = "Posts"


# boto3 DynamoDB クライアント
dynamodb = boto3.resource(
    "dynamodb",
    region_name=settings.AWS_REGION,
    endpoint_url=settings.DYNAMODB_ENDPOINT,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)

# テーブルの定義
admins_table = dynamodb.Table(ADMIN_TABLE_NAME)
settings_table = dynamodb.Table(SETTINGS_TABLE_NAME)
templates_table = dynamodb.Table(TEMPLATES_TABLE_NAME)
posts_table = dynamodb.Table(POSTS_TABLE_NAME)

# 投稿データ取得
def get_post_data() -> List[Dict[str, Any]]:
    try:
        resp = posts_table.scan()
        return resp.get("Items", [])
    except Exception as e:
        print(f"DynamoDBからの投稿データ取得に失敗しました: {e}")
        return []

# 設定（ABテスト比率のみを保持・更新）
def get_settings_data() -> Dict[str, Any]:
    # SettingsTable からアプリ共通設定を取得
    try:
        resp = settings_table.get_item(Key={"id": "app_settings"})
        item = resp.get("Item", {})
        return {
            "id": item.get("id", "app_settings"),
            "ab_test_ratio": item.get("ab_test_ratio", {}),
        }
    except Exception as e:
        print(f"設定データの取得に失敗しました: {e}")
        return {
            "id": "app_settings",
            "ab_test_ratio": {},
        }

def update_settings_data(data: Dict[str, Any]) -> bool:
    # ABテスト比率のみを保存
    try:
        put_item = {
            "id": "app_settings",
            "ab_test_ratio": data.get("ab_test_ratio", {}),
        }
        settings_table.put_item(Item=put_item)
        return True
    except Exception as e:
        print(f"設定データの更新に失敗しました: {e}")
        return False


# テンプレート一覧取得
def get_templates_data() -> List[Dict[str, Any]]:
    try:
        resp = templates_table.scan()
        return resp.get("Items", [])
    except Exception as e:
        print(f"テンプレート一覧の取得に失敗しました: {e}")
        return []

# テンプレート作成
def create_template_data(template: Dict[str, Any]) -> Dict[str, Any]:
    try:
        templates_table.put_item(Item=template)
        return {"message": "テンプレートを登録しました。"}
    except Exception as e:
        print(f"テンプレートの作成に失敗しました: {e}")
        return {"message": "テンプレートの作成に失敗しました。"}

# テンプレート更新
def update_template_data(template_id: str, template: Dict[str, Any]) -> Dict[str, Any]:
    try:
        item = {**template, "id": template_id}
        templates_table.put_item(Item=item)
        return {"message": "テンプレートを更新しました。"}
    except Exception as e:
        print(f"テンプレートの更新に失敗しました: {e}")
        return {"message": "テンプレートの更新に失敗しました。"}

# テンプレート削除
def delete_template_data(template_id: str) -> Dict[str, str]:
    try:
        templates_table.delete_item(Key={"id": template_id})
        return {"message": "テンプレートを削除しました。"}
    except Exception as e:
        print(f"テンプレートの削除に失敗しました: {e}")
        return {"message": "テンプレートの削除に失敗しました。"}

# テンプレート有効化
def activate_template_data(template_id: str) -> Dict[str, str]:
    try:
        # 全件取得して一括更新
        resp = templates_table.scan()
        items = resp.get("Items", [])

        with templates_table.batch_writer() as batch:
            for it in items:
                tid = it.get("id")
                if not tid:
                    continue
                it["is_active"] = 1 if tid == template_id else 0
                it["updated_at"] = datetime.utcnow().isoformat()
                batch.put_item(Item=it)

        return {"message": "テンプレートを有効化しました。"}
    except Exception as e:
        print(f"テンプレートの有効化に失敗しました: {e}")
        return {"message": "テンプレートの有効化に失敗しました。"}    