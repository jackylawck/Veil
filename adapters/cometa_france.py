# adapters/cometa_france.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class CometaFranceAdapter(BaseAdapter):
    """
    法國 COMETA 委員會（高等國防研究院將領專項研究組）適配器
    索引 1999 年呈交法國總統與總理之《國防與異常空中現象：我們應準備什麼？》官方防衛白皮書
    """
    TARGET_RECORDS = [
        {
            "id": "FR-IHEDN-COMETA-REPORT-1999",
            "title": "COMETA Committee: UFOs and Defense - What Should We Prepare For? (Official Defence Synthesis)",
            "zh_title": "法國高等國防研究院 COMETA 委員會：不明飛行物與國家防禦官方綜合白皮書",
            "zh_summary": "由法國空軍上將、國家太空研究中心前總裁及國防情報高官歷時三年編撰，並正式呈交法國總統與總理之防禦評估報告。報告針對全球軍事雷達印證案例進行戰略審查，並正式提出地外智慧假說 (ETH) 於國家安全防衛上之應對方針。",
            "date": "1999-07-16",
            "url": "https://www.ihedn.fr",
            "agencies": ["COMETA", "Institut des Hautes Études de Défense Nationale (IHEDN)", "French Air and Space Force"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "cometa_france"

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
                "evidence_level": "official_senior_military_defense_study",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "fr",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "High-level strategic defense white paper presented to the French President by senior military generals and aerospace scientists analyzing national security implications of aerial phenomena."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"COMETA Official Defense Dossier ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
