# app/clients/shortio.py
import os
import httpx
from typing import Optional, Dict, Any

SHORTIO_API_BASE = "https://api.short.io"
SHORTIO_API_KEY = os.getenv("SHORTIO_API_KEY", "")
SHORTIO_DOMAIN = os.getenv("SHORTIO_DOMAIN", "")

HEADERS = {
    "Authorization": f"Bearer {SHORTIO_API_KEY}",
    "Content-Type": "application/json",
}

async def _get_json(method: str, url: str, **kwargs) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.request(method, url, headers=HEADERS, **kwargs)
        r.raise_for_status()
        if r.text:
            return r.json()
        return {}

async def get_domain_info(domain: str = SHORTIO_DOMAIN) -> Dict[str, Any]:
    # ドメイン情報を取得（links 検索で domain を直接渡せるなら不要）
    url = f"{SHORTIO_API_BASE}/domains?search={domain}"
    data = await _get_json("GET", url)
    # 複数返ることがあるので完全一致を拾う
    for d in data.get("domains", []):
        if d.get("hostname") == domain:
            return d
    return {}

async def find_link_by_path(path: str, domain: str = SHORTIO_DOMAIN) -> Optional[Dict[str, Any]]:
    # 既存リンク検索（path=スラッグ）
    url = f"{SHORTIO_API_BASE}/links?domain={domain}&path={path}"
    data = await _get_json("GET", url)
    items = data.get("links") if isinstance(data, dict) else data
    if items:
        return items[0]
    return None

async def upsert_link(path: str, original_url: str, domain: str = SHORTIO_DOMAIN) -> Dict[str, Any]:
    # 存在すれば更新、なければ作成
    exist = await find_link_by_path(path, domain)
    if not exist:
        url = f"{SHORTIO_API_BASE}/links"
        payload = {"domain": domain, "path": path, "originalURL": original_url}
        return await _get_json("POST", url, json=payload)
    else:
        link_id = exist.get("idString") or exist.get("id")
        url = f"{SHORTIO_API_BASE}/links/{link_id}"
        payload = {"originalURL": original_url}
        return await _get_json("PATCH", url, json=payload)

async def get_clicks_by_link_id(link_id: str, period: str = "all", unique: bool = True) -> int:
    # クリック数取得（必要に応じて period=7d,30d 等へ）
    u = "true" if unique else "false"
    url = f"{SHORTIO_API_BASE}/statistics/links/{link_id}/clicks?period={period}&unique={u}"
    data = await _get_json("GET", url)
    # 返却フォーマットにより調整（合計値を返す想定）
    return int(data.get("total", 0) or data.get("clicks", 0) or 0)

async def get_clicks_by_path(path: str, domain: str = SHORTIO_DOMAIN, period: str = "all") -> int:
    link = await find_link_by_path(path, domain)
    if not link:
        return 0
    link_id = link.get("idString") or link.get("id")
    return await get_clicks_by_link_id(link_id, period=period, unique=True)
