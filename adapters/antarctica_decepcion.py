# adapters/antarctica_decepcion.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class AntarcticaDecepcionAdapter(BaseAdapter):
    """
    阿根廷海軍 (Armada Argentina) 與南極研究所 (IAA) 適配器
    索引 1965 年南極欺騙島多國科考基地聯合目擊與海軍司令部第 172 號官方公報
    """
    TARGET_RECORDS = [
        {
            "id": "AQ-ARMADA-DECEPCION-1965",
            "title": "Argentine Navy Command: Official Press Communique No. 172 on Deception Island Antarctic Aerial Sightings",
            "zh_title": "阿根廷海軍司令部：南極欺騙島空中異常現象第 172 號官方軍事公報",
            "zh_summary": "1965 年 7 月阿根廷海軍極地基地、智利科考站與英國觀測人員於南極欺騙島多方目擊高速金屬透鏡狀飛行物。阿根廷海軍作戰司令部經調查後，正式向公眾發布官方第 172 號軍事新聞公報確認該事件。",
            "date": "1965-07-07",
            "url": "https://www.argentina.gob.ar/armada",
            "agencies": ["Argentine Navy (Armada Argentina)", "Instituto Antártico Argentino", "Ministry of Defense (Argentina)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "antarctica_decepcion"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "official_notice",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_military_communique",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "es",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official military press release and polar base multi-sensor visual observation reports released by the Argentine Navy Secretariat."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Armada Argentina Official Archive ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
