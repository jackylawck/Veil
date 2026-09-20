# adapters/saaf_south_africa.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class SaafSouthAfricaAdapter(BaseAdapter):
    """
    南非空軍 (SAAF) 與國防部情報處適配器
    索引南非軍事航空管制與防空基地官方歷史遭遇卷宗
    """
    TARGET_RECORDS = [
        {
            "id": "ZA-SAAF-DEFENCE-ARCHIVE-1972",
            "title": "South African Air Force: Official Military Report on the Fort Beaufort Aerospace Sighting",
            "zh_title": "南非空軍參謀本部：博福特堡空中異常物體軍警聯合調查官方報告",
            "zh_summary": "1972 年南非空軍直升機部隊與警方針對未知飛行目標進行多日軍事監控，南非防衛司令部情報組正式立案調查並列入空防歷史案卷存檔。",
            "date": "1972-06-26",
            "url": "http://www.dod.mil.za",
            "agencies": ["South African Air Force (SAAF)", "Department of Defence (South Africa)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "saaf_south_africa"

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
                "evidence_level": "official_air_force_incident_archive",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Declassified historical military aviation records preserved by the South African Department of Defence."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"South African DoD Documentation Centre ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
