# adapters/aerocivil_colombia.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class AerocivilColombiaAdapter(BaseAdapter):
    """
    哥倫比亞民航特別行政局 (Aerocivil) 航空安全調查委員會適配器
    索引安地斯山空域民航客機緊急避讓、空管雷達通聯與空軍防空聯調之官方安全卷宗
    """
    TARGET_RECORDS = [
        {
            "id": "CO-AEROCIVIL-AIR-SAFETY-DOSSIER",
            "title": "Special Administrative Unit of Civil Aeronautics: Official Aviation Safety Investigation Dossier",
            "zh_title": "哥倫比亞民航局 (Aerocivil)：民航客機空中異常遭遇與雷達聯調官方安全調查報告",
            "zh_summary": "哥倫比亞民航局空中事故調查處依據法定航空安全規範，針對境內民航機組員通報之未識別空中目標、防相撞避讓動作及地面長程二次雷達記錄進行之官方審查報告。",
            "date": "2020-01-28",
            "url": "https://www.aerocivil.gov.co",
            "agencies": ["Civil Aeronautics (Aerocivil Colombia)", "Colombian Air Force (FAC)", "Ministry of Transport (Colombia)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "aerocivil_colombia"

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
                "evidence_level": "official_aviation_safety_investigation",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "es",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official aviation safety dossiers and secondary radar records released by the Special Administrative Unit of Civil Aeronautics."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Aerocivil Colombia Safety Registry ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
