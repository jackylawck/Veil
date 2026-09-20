# adapters/ciaa_argentina.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class CiaaArgentinaAdapter(BaseAdapter):
    """
    阿根廷空軍航天識別中心 (CIAA / FAA) 適配器
    索引阿根廷空軍作戰司令部發布之領空異常飛行目標官方年度鑑定報告
    """
    TARGET_RECORDS = [
        {
            "id": "AR-FAA-CIAA-ANNUAL-REPORT",
            "title": "Argentine Air Force Aerospace Identification Center: Official Resolution and Annual Case Dossier",
            "zh_title": "阿根廷空軍航天識別中心 (CIAA)：領空異常現象官方調查與年度鑑定全卷",
            "zh_summary": "由阿根廷空軍作戰司令部常設之航天識別中心 (CIAA) 發布之官方報告，詳細記錄軍用雷達軌跡、多光譜光學鑑定結論與軍航遭遇事件之官方審查結果。",
            "date": "2021-12-30",
            "url": "https://www.argentina.gob.ar/fuerzaaerea",
            "agencies": ["Argentine Air Force (FAA)", "Ministry of Defense (Argentina)", "CIAA"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "ciaa_argentina"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "scientific_report",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_air_force_aerospace_report",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "es",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official aerospace anomaly identification dossiers and sensor analysis released annually by the Argentine Air Force Aerospace Identification Center."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Fuerza Aérea Argentina Official Dossier ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
