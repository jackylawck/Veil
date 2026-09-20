# adapters/sol_karl_nell.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class SolKarlNellAdapter(BaseAdapter):
    """
    前陸軍特戰指揮官 Karl Nell 上校與 Sol Foundation『受控披露戰略架構』適配器
    索引高階軍方戰略官員確認非人類智慧 (NHI) 與 2030 階段性國家披露政策之防務藍圖
    """
    TARGET_RECORDS = [
        {
            "id": "SOL-POLICY-NELL-CONTROLLED-DISCLOSURE",
            "title": "Col. Karl Nell & Sol Foundation: National Strategic Campaign Plan for Controlled UAP Disclosure",
            "zh_title": "Karl Nell 上校與 Sol 基金會：受控國家披露與非人類智慧 (NHI) 接觸戰略計畫案卷",
            "zh_summary": "曾任北方司令部與陸軍期貨司令部特戰計畫主管之 Karl Nell 上校於 Sol Foundation 發表之防務戰略白皮書。公開確認非人類智慧存在之情報實證，並提出至 2030 年間白宮、國防部與盟國進行分階段披露、條約規範與科學整合之官方政策路徑。",
            "date": "2024-05-21",
            "url": "https://thesolfoundation.org",
            "agencies": [
                "The Sol Foundation",
                "US Army Futures Command (Historical Context)",
                "Office of the Secretary of Defense (Oversight Context)"
            ]
        }
    ]

    @property
    def source_name(self) -> str:
        return "sol_karl_nell"

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
                "evidence_level": "official_senior_defense_strategic_briefing",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "National strategic campaign blueprint authored by retired Col. Karl Nell outlining timelines, treaty frameworks, and governance protocols for non-human intelligence disclosure."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Sol Foundation Symposium White Paper ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
