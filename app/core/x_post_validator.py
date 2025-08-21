from __future__ import annotations
import unicodedata
from dataclasses import dataclass

# 半角=1, 全角=2 の合計で280まで許容
MAX_X_POST_UNITS = 280


def _char_units(ch: str) -> int:
    # East Asian Width に基づいて全角扱いを判定
    # "W","F" を全角=2 として、それ以外は半角=1 でカウント
    eaw = unicodedata.east_asian_width(ch)
    return 2 if eaw in ("W", "F") else 1


def count_units(text: str) -> int:
    # テキスト全体のカウントを算出
    if not text:
        return 0
    return sum(_char_units(ch) for ch in text)


@dataclass(frozen=True)
class XPostLengthResult:
    # バリデーション結果のDTO
    ok: bool
    units: int
    limit: int
    remaining: int


def validate_x_post_length(text: str) -> XPostLengthResult:
    # 文字数カウントの結果からOK/NGと残りカウントを返す
    units = count_units(text or "")
    return XPostLengthResult(
        ok=units <= MAX_X_POST_UNITS,
        units=units,
        limit=MAX_X_POST_UNITS,
        remaining=MAX_X_POST_UNITS - units,
    )