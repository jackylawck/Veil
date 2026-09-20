# adapters/naa.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class NaaAdapter(BaseAdapter):
    """
    澳洲國家檔案館 (NAA) 適配器
    索引五眼聯盟盟國澳洲皇家空軍 (RAAF) 與國防部 DSTO 官方解密檔案 (Series A703 / A705)
    """
    TARGET_RECORDS = [
        {
            "id": "NAA-A703-580-1-1",
            "title": "Royal Australian Air Force: Scientific Investigation of UFOs (Series A703, Control 580/1/1)",
            "zh_title": "澳洲皇家空軍 (RAAF)：未知飛行物科學調查官方全卷",
            "zh_summary": "澳洲國防部與皇家空軍技術情報處於 1950 至 1970 年代建立之官方檔案，收錄空軍雷達與飛行員目擊調查，由澳洲國家檔案館依解密程序全面開放檢索。",
            "date": "1971-06-03",
            "url": "https://recordsearch.naa.gov.au",
            "agencies": ["National Archives of Australia", "Royal Australian Air Force (RAAF)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "naa"

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
                "evidence_level": "official_five_eyes_archive",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Historical Five Eyes intelligence records preserved and digitized by the National Archives of Australia."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"NAA RecordSearch ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
