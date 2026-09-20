# adapters/aeronautica_militare.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class AeronauticaMilitareAdapter(BaseAdapter):
    """
    義大利空軍總參謀部第二情報處 (Aeronautica Militare - RIS) 適配器
    索引依據義大利總理法令正式設立之軍事航空 OVNI 官方登記年度審計紀錄
    """
    TARGET_RECORDS = [
        {
            "id": "IT-AM-OVNI-REGISTRY-OFFICIAL",
            "title": "Italian Air Force General Staff: Official Registry of Unidentified Flying Objects (OVNI Reports)",
            "zh_title": "義大利空軍總參謀部情報處：不明飛行物體 (OVNI) 官方年度審計登記冊",
            "zh_summary": "依據 1978 年總理政令，義大利空軍總參謀部第二處受命負責軍民航目擊與軍用雷達異常數據之官方鑑定，每年依國防透明原則公開官方統計清單。",
            "date": "2020-12-31",
            "url": "http://www.aeronautica.difesa.it",
            "agencies": ["Italian Air Force (Aeronautica Militare)", "General Staff - 2nd Department (RIS)", "Ministry of Defence (Italy)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "aeronautica_militare"

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
                "precision": "year"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_nato_military_registry",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "it",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official military aviation register maintained by the Italian Air Force General Staff pursuant to prime ministerial intelligence decrees."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Aeronautica Militare Official Dossier ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
