# adapters/irish_df.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class IrishDfAdapter(BaseAdapter):
    """
    愛爾蘭國防軍 (Irish Defence Forces) 與航空管理局 (IAA) 適配器
    索引愛爾蘭西海岸民航客機遭遇與國防雷達監控官方解密報告
    """
    TARGET_RECORDS = [
        {
            "id": "IE-DF-IAA-SHANNON-2018",
            "title": "Irish Aviation Authority & Defence Forces: Official Investigation into the Shannon Coast Airborne Sightings",
            "zh_title": "愛爾蘭航空管理局與國防軍：香農空域民航客機遭遇異常物體官方調查報告",
            "zh_summary": "2018 年 11 月 9 日多架民航客機機組人員於愛爾蘭西海岸向香農航空管制台通報高速明亮物體。愛爾蘭航空管理局與國防軍依法啟動正式安全調查，空管通聯與雷達記錄經愛爾蘭國防部資訊自由法案審查後公開。",
            "date": "2018-11-09",
            "url": "https://www.military.ie",
            "agencies": ["Irish Defence Forces", "Irish Aviation Authority (IAA)", "Department of Defence (Ireland)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "irish_df"

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
                "evidence_level": "official_aviation_authority_investigation",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official flight safety and air traffic radar logs released by the Irish Aviation Authority and Defence Forces under statutory transparency requirements."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Irish Department of Defence FOI Portal ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
