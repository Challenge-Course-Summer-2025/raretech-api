from __future__ import annotations
from typing import Optional, List, Dict, Any
from datetime import datetime
from clients.dynamodb import get_post_data
from schemas.posts import PostListItem
from core.x_post_validator import validate_x_post_length, XPostLengthResult
from .dashboard import _get_article_clicks_map


def _to_post_list_item_dict(src: Dict[str, Any]) -> Dict[str, Any]:
    # 既存データの互換のため、idエイリアスを補完
    normalized = {
        "id": src.get("id") or src.get("post_id"),
        "qiita_id": src.get("qiita_id", ""),
        "title": src.get("title", ""),
        "author": src.get("author", ""),
        "template_id": src.get("template_id"),
        "created_at": src.get("created_at", datetime.utcnow().isoformat()),
        "clicks_article": src.get("clicks_article", 0),  # ← 追加
    }
    item = PostListItem.model_validate(normalized)
    return item.model_dump(by_alias=True)

async def get_posts(page: int = 1, limit: int = 10, search: Optional[str] = None):
    # DynamoDB から全投稿を取得（メタデータのみ）
    posts = get_post_data()

    # 検索条件があればフィルタリング
    if search:
        q = search.lower()
        posts = [p for p in posts if q in (p.get("title", "")).lower()]

    # created_atで降順ソート
    try:
        posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    except Exception:
        pass

    # ページング処理
    total = len(posts)
    start = max((page - 1) * limit, 0)
    end = start + limit
    page_items = posts[start:end]

    # クリック数マップを取得
    article_clicks_map = _get_article_clicks_map()

    # 各投稿にclicks_articleを付与
    for post in page_items:
        post_id = post.get("id") or post.get("post_id")
        post["clicks_article"] = article_clicks_map.get(post_id, 0)

    # PostListItemに整形して返す
    dto_list: List[Dict[str, Any]] = []
    for p in page_items:
        try:
            dto_list.append(_to_post_list_item_dict(p))
        except Exception:
            dto_list.append(
                _to_post_list_item_dict(
                    {
                        "id": p.get("id") or p.get("post_id") or "unknown",
                        "qiita_id": p.get("qiita_id", ""),
                        "title": p.get("title", ""),
                        "author": p.get("author", ""),
                        "template_id": p.get("template_id"),
                        "created_at": p.get("created_at", datetime.utcnow().isoformat()),
                    }
                )
            )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "posts": dto_list,
    }

# X投稿テキストをサーバー側で検証する公開関数
def validate_x_post_text(text: str) -> XPostLengthResult:
    # エンドポイント層からそのまま呼べるように services に用意
    return validate_x_post_length(text or "")