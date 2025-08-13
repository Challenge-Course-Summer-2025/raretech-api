import time
import json
import urllib.request
from typing import Dict, Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, jwk
from jose.utils import base64url_decode

from core.config import settings
from services.auth import get_admin_by_sub

bearer_scheme = HTTPBearer(auto_error=True)

# JWKS をキャッシュ
_JWKS_CACHE: Optional[Dict[str, Any]] = None
_JWKS_CACHE_AT: float = 0.0
_JWKS_TTL = 60 * 60

def _load_jwks() -> Dict[str, Any]:
    global _JWKS_CACHE, _JWKS_CACHE_AT
    now = time.time()
    if _JWKS_CACHE and now - _JWKS_CACHE_AT < _JWKS_TTL:
        return _JWKS_CACHE
    with urllib.request.urlopen(settings.COGNITO_JWKS_URL) as resp:
        body = resp.read()
        _JWKS_CACHE = json.loads(body)
        _JWKS_CACHE_AT = now
        return _JWKS_CACHE

def _verify_signature(token: str, kid: str) -> Dict[str, Any]:
    jwks = _load_jwks()
    key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
    if not key:
        raise HTTPException(status_code=401, detail="JWKS key not found")

    # 署名検証
    message, encoded_signature = token.rsplit(".", 1)
    decoded_sig = base64url_decode(encoded_signature.encode("utf-8"))
    public_key = jwk.construct(key)
    if not public_key.verify(message.encode("utf-8"), decoded_sig):
        raise HTTPException(status_code=401, detail="Token signature invalid")

    # 署名OKなら未検証クレームを返す
    return jwt.get_unverified_claims(token)

def _validate_claims(claims: Dict[str, Any]) -> None:
    # iss
    if claims.get("iss") != settings.COGNITO_ISSUER:
        raise HTTPException(status_code=401, detail="Invalid issuer")

    # exp
    if int(claims.get("exp", 0)) < int(time.time()):
        raise HTTPException(status_code=401, detail="Token expired")

    # token_use
    accepted = {u.strip() for u in settings.COGNITO_ACCEPTED_TOKEN_USE.split(",")}
    if claims.get("token_use") not in accepted:
        raise HTTPException(status_code=401, detail="Invalid token use")

    # aud / client_id
    if settings.COGNITO_APP_CLIENT_ID:
        aud = claims.get("client_id") or claims.get("aud")
        if aud != settings.COGNITO_APP_CLIENT_ID:
            raise HTTPException(status_code=401, detail="Invalid audience")

async def verify_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Dict[str, Any]:
    token = credentials.credentials

    try:
        headers = jwt.get_unverified_header(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token header")
    kid = headers.get("kid")
    if not kid:
        raise HTTPException(status_code=401, detail="kid missing")

    claims = _verify_signature(token, kid)

    _validate_claims(claims)

    sub = claims.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="sub missing")

    # AdminsTable から管理者情報を取得
    admin = await get_admin_by_sub(sub)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin not registered"
        )

    return {
        "admin_id": admin.get("admin_id"),
        "email": admin.get("email"),
        "user_name": admin.get("user_name"),
        "created_at": admin.get("created_at"),
        "updated_at": admin.get("updated_at"),
    }
