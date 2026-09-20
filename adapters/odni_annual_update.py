# adapters/odni_annual_update.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class OdniAnnualUpdateAdapter(BaseAdapter):
    """
    美國國家情報總監辦公室 (ODNI) 法定年度 UAP 威脅與案例評估更新適配器
    索引依據國防授權法與情報授權法每年向國會呈送之全美情報界 (IC) 官方解密審計年報
    """
    TARGET_RECORDS = [
        {
            "id": "ODNI-ANNUAL-UAP-ASSESSMENT-STATUTORY",
            "title": "Office of the Director of National Intelligence: Statutory Annual Assessment on Unidentified Anomalous Phenomena",
            "zh_title": "美國國家情報總監辦公室 (ODNI)：未知異常現象 (UAP) 全美情報界法定年度解密評估報告",
            "zh_summary": "依據聯邦情報法規常態化條款，統籌全美 18 個情報機構、三軍各戰區司令部及感測器網絡之數據。發布年度官方通報案例數、感測器特徵分類、跨介質目標比例及國家安全威脅評估結論。",
            "date": "2024-11-14",
            "url": "https://www.dni.gov",
            "agencies": [
                "Office of the Director of National Intelligence (ODNI)",
                "National Intelligence Council",
                "Department of Defense"
            ]
        }
    ]

    @property
    def source_name(self) -> str:
        return "odni_annual_update"

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
                "evidence_level": "official_statutory_intelligence_community_assessment",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Mandated statutory assessment prepared annually by the Director of National Intelligence synthesizing military intelligence and aerospace sensor logs across the US Intelligence Community."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"ODNI Official Statutory Release ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
