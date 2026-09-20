# adapters/un.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class UnAdapter(BaseAdapter):
    """
    聯合國 (United Nations) 官方文件適配器
    索引聯合國大會全體會議通過之歷史性官方決議與國際多邊治理紀錄
    """
    TARGET_RECORDS = [
        {
            "id": "UN-GA-RES-33-426",
            "title": "United Nations General Assembly Resolution 33/426: Research on Unidentified Flying Objects",
            "zh_title": "聯合國大會第 33/426 號決議：關於協調不明飛行物與相關現象研究之專項決議",
            "zh_summary": "1978 年 12 月 18 日聯合國大會第 87 次全體會議正式審議並通過之官方決議案，正式邀請各成員國採取適當步驟協調異常飛行物之科學研究，並由秘書長進行跨國數據通報與轉發。",
            "date": "1978-12-18",
            "url": "https://digitallibrary.un.org/record/614352",
            "agencies": ["United Nations", "General Assembly", "Special Political Committee"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "un"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "official_notice",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_multilateral_resolution",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official United Nations General Assembly plenary resolution adopted on multilateral scientific coordination of aerial phenomenon research."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"UN Digital Library Official Record ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
