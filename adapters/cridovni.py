# adapters/cridovni.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class CridovniAdapter(BaseAdapter):
    """
    烏拉圭空軍 (FAU) CRIDOVNI 官方調查委員會適配器
    索引自 1979 年起依空軍命令常設之軍民航異常飛行報告官方審查案卷
    """
    TARGET_RECORDS = [
        {
            "id": "UY-FAU-CRIDOVNI-FOUNDATION",
            "title": "Uruguayan Air Force: Official Mandate and Investigations of the CRIDOVNI Commission",
            "zh_title": "烏拉圭空軍：CRIDOVNI 不明飛行物調查委員會官方常設法規與調查案卷",
            "zh_summary": "1979 年由烏拉圭空軍司令部正式頒令成立之官方常設調查機構，由現役空軍技術軍官與科學顧問組成，專責接收、鑑定與解密空軍基地周邊及民航通報之空中異常現象。",
            "date": "1979-08-07",
            "url": "https://www.fau.mil.uy",
            "agencies": ["Uruguayan Air Force (FAU)", "Ministry of National Defence (Uruguay)", "CRIDOVNI"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "cridovni"

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
                "original_language": "es",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official military records maintained by the Uruguayan Air Force CRIDOVNI commission pursuant to permanent air force defense directives."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Fuerza Aérea Uruguaya Official Portal ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
