# adapters/difaa_peru.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class DifaaPeruAdapter(BaseAdapter):
    """
    秘魯空軍異常空天現象調查處 (DIFAA / FAP) 適配器
    索引秘魯空軍常設調查機構發布之領空防衛遭遇與官方軍事解密案卷
    """
    TARGET_RECORDS = [
        {
            "id": "PE-FAP-DIFAA-LA-JOYA-1980",
            "title": "Peruvian Air Force: Official Declassified Dossier on the La Joya Air Base Intercept Incident",
            "zh_title": "秘魯空軍 (FAP / DIFAA)：拉荷亞空軍基地戰機實彈截擊未知目標官方解密報告",
            "zh_summary": "1980 年 4 月 11 日秘魯空軍基地防空雷達發現未授權目標，空軍緊急派遣 Su-22 噴射戰鬥機升空並以 30mm 機砲進行實彈射擊截擊。該案調查檔案由秘魯空軍專責常設機構 DIFAA 永久列管並向公眾發布解密結論。",
            "date": "1980-04-11",
            "url": "https://www.fap.mil.pe",
            "agencies": ["Peruvian Air Force (FAP)", "DIFAA", "Ministry of Defense (Peru)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "difaa_peru"

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
                    "executive_summary": "Official military aviation intercept records maintained by the Peruvian Air Force Aerospace Anomaly Investigation Department."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Fuerza Aérea del Perú Official Record ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
