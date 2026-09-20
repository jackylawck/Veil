# adapters/house_uap_nov2024.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class HouseUapNov2024Adapter(BaseAdapter):
    """
    美國眾議院監督委員會 2024 年 11 月 13 日『揭示真相』聯合宣誓聽證會適配器
    索引前國防情報官員 Elizondo、前海軍少將 Gallaudet 及 NASA 官員 Gold 之法定證詞
    """
    TARGET_RECORDS = [
        {
            "id": "GPO-CHRG-118-HHRG-UAP-20241113",
            "title": "Unidentified Anomalous Phenomena: Exposing the Truth (House Oversight Hearing)",
            "zh_title": "眾議院監督委員會：未知異常現象 (UAP) 揭示真相聯合宣誓聽證會正式出版紀錄本",
            "zh_summary": "2024 年 11 月 13 日眾議院國家安全與網絡安全小組委員會聯合聽證會。前國防官員與海軍少將宣誓作證確認敏感國防設施遭異常科技監控，並將跨部會機密隱匿體系載入國會正式公報。",
            "date": "2024-11-13",
            "url": "https://www.congress.gov",
            "agencies": [
                "House Committee on Oversight and Accountability",
                "Subcommittee on National Security, the Border, and Foreign Affairs",
                "Subcommittee on Cybersecurity, Information Technology, and Government Innovation"
            ]
        }
    ]

    @property
    def source_name(self) -> str:
        return "house_uap_nov2024"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "official_report",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_hearing_record",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official joint congressional hearing transcript examining Department of Defense over-classification, crash retrieval program allegations, and advanced aerospace incursions."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"House Oversight Committee Official Record ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
