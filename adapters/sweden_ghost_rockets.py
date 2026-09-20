# adapters/sweden_ghost_rockets.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class SwedenGhostRocketsAdapter(BaseAdapter):
    """
    瑞典國防軍 (Försvarsmakten) 與國家檔案館 (Riksarkivet) 適配器
    索引 1946 年瑞典軍方『幽靈火箭 (Ghost Rockets) 特別調查委員會』官方解密軍事全卷
    """
    TARGET_RECORDS = [
        {
            "id": "SE-MIL-GHOST-ROCKETS-1946",
            "title": "Swedish Armed Forces General Staff: Official Declassified Investigation on the Ghost Rockets",
            "zh_title": "瑞典國防軍總參謀部：1946 年『幽靈火箭』官方軍事調查與雷達追蹤解密檔案",
            "zh_summary": "1946 年瑞典空防體系探測到大量未知火箭狀物體穿越領空。瑞典國防軍設立軍事專門委員會進行跨兵種調查與湖泊打撈作業，全案雷達記錄與軍事結論經瑞典國防軍解密後由國家檔案館典藏。",
            "date": "1946-12-10",
            "url": "https://sok.riksarkivet.se",
            "agencies": ["Swedish Armed Forces (Försvarsmakten)", "Defence Research Agency (FOI)", "National Archives of Sweden"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "sweden_ghost_rockets"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "declassified_archive",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_military_standing_commission",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "sv",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official military investigation dossiers and radar telemetry preserved by the Swedish Armed Forces regarding the 1946 Ghost Rockets occurrences."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Riksarkivet Official Dossier ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
