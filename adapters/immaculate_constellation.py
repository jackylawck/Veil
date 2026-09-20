# adapters/immaculate_constellation.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class ImmaculateConstellationAdapter(BaseAdapter):
    """
    五角大廈秘密專案『無瑕星座 (Immaculate Constellation)』國會存證吹哨報告適配器
    索引 2024 年 11 月由眾議院監督委員會正式批准列入國會永久記錄 (Congressional Record) 之官方報告
    """
    TARGET_RECORDS = [
        {
            "id": "CONG-RECORD-IMMACULATE-CONST-2024",
            "title": "US Congressional Record: Whistleblower Report on DoD Unacknowledged SAP 'Immaculate Constellation'",
            "zh_title": "美國國會公報：國防部未公開特殊權限專案『無瑕星座 (Immaculate Constellation)』吹哨者存證報告",
            "zh_summary": "由現任及前任國防官員吹哨並經眾議院監督委員會主席正式准予載入國會紀錄之 12 頁官方報告。揭露五角大廈自 2017 年起設立專門隔離專案，對全軍截獲之高解析度異常光學與多光譜遙測數據實施集中封存與審查迴避。",
            "date": "2024-11-13",
            "url": "https://www.congress.gov",
            "agencies": ["US House of Representatives", "Department of Defense", "Congressional Record"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "immaculate_constellation"

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
                "evidence_level": "official_congressional_record_entry",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Whistleblower dossier officially entered into the US Congressional Record detailing an alleged unacknowledged special access program managing military anomaly sensor captures."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Congressional Record / House Oversight Package ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
