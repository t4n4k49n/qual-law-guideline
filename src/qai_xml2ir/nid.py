from __future__ import annotations

import re
from typing import Dict, Optional

_IROHA_MAP: Dict[str, str] = {
    "イ": "i",
    "ロ": "ro",
    "ハ": "ha",
    "ニ": "ni",
    "ホ": "ho",
    "ヘ": "he",
    "ト": "to",
    "チ": "chi",
    "リ": "ri",
    "ヌ": "nu",
    "ル": "ru",
    "ヲ": "wo",
    "ワ": "wa",
    "カ": "ka",
    "ヨ": "yo",
    "タ": "ta",
    "レ": "re",
    "ソ": "so",
    "ツ": "tsu",
    "ネ": "ne",
    "ナ": "na",
    "ラ": "ra",
    "ム": "mu",
    "ウ": "u",
    "ヰ": "wi",
    "ノ": "no",
    "オ": "o",
    "ク": "ku",
    "ヤ": "ya",
    "マ": "ma",
    "ケ": "ke",
    "フ": "fu",
    "コ": "ko",
    "エ": "e",
    "テ": "te",
    "ア": "a",
    "サ": "sa",
    "キ": "ki",
    "ユ": "yu",
    "メ": "me",
    "ミ": "mi",
    "シ": "shi",
    "ヱ": "we",
    "ヒ": "hi",
    "モ": "mo",
    "セ": "se",
    "ス": "su",
}


def slug_iroha(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    text = text.strip()
    if text in _IROHA_MAP:
        return _IROHA_MAP[text]
    return None


def extract_digits(text: Optional[str]) -> Optional[int]:
    if not text:
        return None
    m = re.search(r"([0-9０-９]+)", text)
    if not m:
        return None
    raw = m.group(1)
    normalized = raw.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
    try:
        return int(normalized)
    except ValueError:
        return None


class NidBuilder:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def unique(self, nid: str) -> str:
        if nid not in self._seen:
            self._seen.add(nid)
            return nid
        i = 2
        while f"{nid}_{i}" in self._seen:
            i += 1
        uniq = f"{nid}_{i}"
        self._seen.add(uniq)
        return uniq
