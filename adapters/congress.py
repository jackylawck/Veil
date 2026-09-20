# adapters/congress.py
import json
import os
from typing import Any, Dict, List
import requests
from .base import BaseAdapter

# 嚴格的 UAP 關鍵字過濾
UAP_KEYWORDS = [
    "unidentified anomalous phenomena",
    "unidentified aerial phenomena",
    "uap",
    "uapda",
    "aaro",
    "non-earth origin",
    "non-human intelligence",
    "nhi",
    "anomalous phenomena",
]

# 顯著行動過濾白名單（過濾掉毫無意義的 Referred to committee 雜訊）
SIGNIFICANT_ACTIONS = [
    "placed on",
    "passed",
    "reported by",
    "agreed to",
    "amendment",
    "motion to proceed",
    "cloture",
    "vetoed",
    "signed by the president",
    "became public law",
]


class CongressGovAdapter(BaseAdapter):
    BASE_URL = "https://api.congress.gov/v3"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("CONGRESS_API_KEY", "")

    @property
    def source_name(self) -> str:
        return "congress_gov"

    def _matches_uap(self, bill: Dict[str, Any]) -> bool:
        title = bill.get("title") or ""
        latest_action = (bill.get("latestAction") or {}).get("text") or ""
        combined_text = f"{title} {latest_action}".lower()
        return any(k in combined_text for k in UAP_KEYWORDS)

    def _is_significant_action(self, bill: Dict[str, Any]) -> bool:
        latest_action = (bill.get("latestAction") or {}).get("text") or ""
        return any(action in latest_action.lower() for action in SIGNIFICANT_ACTIONS)

    def fetch_records(self, congress: int = 119, limit: int = 250) -> List[Dict[str, Any]]:
        if not self.api_key:
            print("[!] CONGRESS_API_KEY not provided. Skipping congress adapter.")
            return []

        endpoint = f"{self.BASE_URL}/bill/{congress}"
        params = {
            "api_key": self.api_key,
            "format": "json",
            "limit": limit,
            "sort": "updateDate+desc",
        }

        res = requests.get(endpoint, params=params, timeout=20)
        res.raise_for_status()
        bills = res.json().get("bills", [])

        normalized_records = []
        for bill in bills:
            # 1. 關鍵字過濾
            if not self._matches_uap(bill):
                continue
            
            # 2. 顯著動作過濾（排除純 Committee 轉交雜訊）
            if not self._is_significant_action(bill):
                continue

            bill_type = (bill.get("type") or "bill").lower()
            bill_num = str(bill.get("number") or "0")
            bill_congress = bill.get("congress") or congress

            official_url = f"https://www.congress.gov/bill/{bill_congress}th-congress/{bill_type}-bill/{bill_num}"
            record_id = f"CONG-{bill_congress}-{bill_type.upper()}-{bill_num}"
            raw_str = json.dumps(bill, sort_keys=True)

            record = {
                "id": record_id,
                "type": "legislation",
                "date": {
                    "val": (bill.get("updateDate") or "").split("T")[0],
                    "precision": "day",
                },
                "governance": {
                    "source_tier": "Tier-1",
                    "evidence_level": "official_document",
                    "confidence_rating": "official_confirmed",
                },
                "entities": {
                    "agencies": ["US-CONGRESS"],
                    "legislation": [f"{bill_type.upper()}{bill_num}"],
                },
                "content": {
                    "original_language": "en",
                    "en": {
                        "title": bill.get("title") or "",
                        "executive_summary": (bill.get("latestAction") or {}).get("text") or "",
                    },
                    "zh_hk": {
                        "title": "",
                        "executive_summary": "",
                    },
                },
                "sources": [
                    {
                        "label": f"Congress.gov {bill_type.upper()} {bill_num} ({bill_congress}th)",
                        "url": official_url,
                        "sha256": self.calculate_sha256(raw_str),
                    }
                ],
            }
            normalized_records.append(record)

        return normalized_records
