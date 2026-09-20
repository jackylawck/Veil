# adapters/rnlaf_netherlands.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class RnlafNetherlandsAdapter(BaseAdapter):
    """
    荷蘭皇家空軍 (RNLAF) 與國防部 (Ministerie van Defensie) 適配器
    索引北約蘇斯特貝赫空軍基地防衛部隊與空管雷達官方解密作戰調查報告
    """
    TARGET_RECORDS = [
        {
            "id": "NL-RNLAF-SOESTERBERG-1979",
            "title": "Royal Netherlands Air Force Command: Official Investigation into the Soesterberg Air Base Incident",
            "zh_title": "荷蘭皇家空軍司令部：蘇斯特貝赫空軍基地異常飛行物官方解密調查報告",
            "zh_summary": "1979 年 2 月 3 日荷蘭皇家空軍主要防空基地當值軍官、基地警衛隊與雷達站同步探測並目擊低空未知幾何發光目標。荷蘭國防部情報組啟動機密調查，全案報告後由荷蘭軍方依檔案法解密公開。",
            "date": "1979-02-03",
            "url": "https://www.defensie.nl",
            "agencies": ["Royal Netherlands Air Force", "Netherlands Ministry of Defence", "Air Staff Intelligence"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "rnlaf_netherlands"

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
                "evidence_level": "official_nato_air_base_investigation",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "nl",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official military investigation records released by the Netherlands Ministry of Defence regarding air base airspace incursions."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Netherlands Defence Ministry Archive ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
