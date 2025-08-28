import boto3
from core.config import settings
from datetime import datetime
from typing import Dict, Any, List

def get_dynamodb_resource():
    kwargs = {"region_name": settings.AWS_REGION}

    if settings.DYNAMODB_ENDPOINT:
        kwargs["endpoint_url"] = settings.DYNAMODB_ENDPOINT

    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY

    return boto3.resource("dynamodb", **kwargs)


# テーブルハンドル
_dynamo = get_dynamodb_resource()
settings_table = _dynamo.Table(settings.SETTINGS_TABLE_NAME)
templates_table = _dynamo.Table(settings.TEMPLATES_TABLE_NAME)
posts_table = _dynamo.Table(settings.POSTS_TABLE_NAME)


# 投稿データ取得
def get_post_data() -> List[Dict[str, Any]]:
    try:
        items: List[Dict[str, Any]] = []
        start_key = None
        while True:
            if start_key:
                resp = posts_table.scan(ExclusiveStartKey=start_key)
            else:
                resp = posts_table.scan()
            items.extend(resp.get("Items", []))
            start_key = resp.get("LastEvaluatedKey")
            if not start_key:
                break
        return items
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
        items: List[Dict[str, Any]] = []
        start_key = None
        while True:
            if start_key:
                resp = templates_table.scan(ExclusiveStartKey=start_key)
            else:
                resp = templates_table.scan()
            items.extend(resp.get("Items", []))
            start_key = resp.get("LastEvaluatedKey")
            if not start_key:
                break
        return items
    except Exception as e:
        print(f"テンプレート一覧の取得に失敗しました: {e}")
        return []

# テンプレート作成
def create_template_data(template: Dict[str, Any]) -> Dict[str, Any]:
    try:
        from uuid import uuid4
        now = datetime.utcnow().isoformat()
        item = {
            "PK": "TEMPLATES",
            "SK": now,
            "id": template.get("id", str(uuid4())),
            "template": template.get("template", ""),
            "is_active": template.get("is_active", 0),
            "created_at": now,
            "updated_at": now,
            # 他に必要な属性があれば追加
        }
        templates_table.put_item(Item=item)
        return {"message": "テンプレートを登録しました。"}
    except Exception as e:
        print(f"テンプレートの作成に失敗しました: {e}")
        return {"message": "テンプレートの作成に失敗しました。"}

# テンプレート更新
def update_template_data(template_id: str, template: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # idからPK, SKを特定
        resp = templates_table.scan(
            FilterExpression="id = :tid",
            ExpressionAttributeValues={":tid": template_id}
        )
        items = resp.get("Items", [])
        if not items:
            return {"message": "テンプレートが見つかりませんでした。"}
        item = items[0]
        # 更新内容を反映
        item.update(template)
        item["updated_at"] = datetime.utcnow().isoformat()
        templates_table.put_item(Item=item)
        return {"message": "テンプレートを更新しました。"}
    except Exception as e:
        print(f"テンプレートの更新に失敗しました: {e}")
        return {"message": "テンプレートの更新に失敗しました。"}

# テンプレート削除
def delete_template_data(template_id: str) -> Dict[str, str]:
    try:
        # idからPK, SKを特定
        resp = templates_table.scan(
            FilterExpression="id = :tid",
            ExpressionAttributeValues={":tid": template_id}
        )
        items = resp.get("Items", [])
        if not items:
            return {"message": "テンプレートが見つかりませんでした。"}
        item = items[0]
        templates_table.delete_item(Key={"PK": item["PK"], "SK": item["SK"]})
        return {"message": "テンプレートを削除しました。"}
    except Exception as e:
        print(f"テンプレートの削除に失敗しました: {e}")
        return {"message": "テンプレートの削除に失敗しました。"}

# テンプレート有効化
def activate_template_data(template_id: str) -> Dict[str, str]:
    try:
        # 全件取得して一括更新
        items: List[Dict[str, Any]] = []
        start_key = None
        while True:
            if start_key:
                resp = templates_table.scan(ExclusiveStartKey=start_key)
            else:
                resp = templates_table.scan()
            items.extend(resp.get("Items", []))
            start_key = resp.get("LastEvaluatedKey")
            if not start_key:
                break

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