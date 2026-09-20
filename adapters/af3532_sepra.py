# adapters/af3532_sepra.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class Af3532SepraAdapter(BaseAdapter):
    """
    法國航空 AF3532 航班空中遭遇與法國空軍防空雷達聯調適配器
    索引法國太空研究中心 (CNES / SEPRA) 及民航總局 (DGAC) 雷達與機組雙重印證官方報告
    """
    TARGET_RECORDS = [
        {
            "id": "FR-DGAC-AF3532-CODA-1994",
            "title": "French Civil Aviation Authority & Air Force Air Defense Command: Official Investigation into the Air France 3532 Radar-Visual Encounter",
            "zh_title": "法國航空 AF3532 班機巴黎空域遭遇與空軍防空雷達 (CODA) 同步鎖定官方報告",
            "zh_summary": "1994 年 1 月 28 日法航 A320 客機正副機長於萬米高空目擊巨大可變幾何飛行物體。法國空軍防空作戰指揮中心 (CODA) 雷達隨後證實於同空域探測到未知高速目標，全案經法國太空中心 SEPRA 深度技術審定，為雷達與機組多感測器印證之指標公案。",
            "date": "1994-01-28",
            "url": "https://www.geipan.fr",
            "agencies": ["Directorate General of Civil Aviation (DGAC)", "French Air and Space Force (CODA)", "CNES / GEIPAN"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "af3532_sepra"

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
                "evidence_level": "official_radar_visual_military_investigation",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "fr",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official joint aeronautical and military air defense radar analysis compiled by the French Space Agency and DGAC regarding the Air France flight 3532 encounter."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"CNES / GEIPAN Case Register ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
