# adapters/ceifo_ecuador.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class CeifoEcuadorAdapter(BaseAdapter):
    """
    厄瓜多空軍 (FAE) CEIFO 官方調查委員會適配器
    索引依據國防部法令設立之空軍防空司令部空中異常現象官方解密卷宗
    """
    TARGET_RECORDS = [
        {
            "id": "EC-FAE-CEIFO-OFFICIAL-DECREE",
            "title": "Ecuadorian Air Force: Official Declassified Records of the CEIFO Investigation Commission",
            "zh_title": "厄瓜多空軍：CEIFO 不明飛行現象調查委員會官方解密卷宗",
            "zh_summary": "依據厄瓜多國防部法令於空軍司令部下常設之專責機構，由空軍情報軍官與雷達工程師審查厄瓜多領空之軍民航雷達異常與戰機遭遇記錄，並依法令實施官方解密。",
            "date": "2005-04-11",
            "url": "https://www.fuerzaaereaecuatoriana.mil.ec",
            "agencies": ["Ecuadorian Air Force (FAE)", "Ministry of National Defense (Ecuador)", "CEIFO"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "ceifo_ecuador"

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
                    "executive_summary": "Official declassified military aviation investigation files released by the Ecuadorian Air Force CEIFO Commission."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Fuerza Aérea Ecuatoriana Archive ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
