# adapters/aaro_historical_vol2.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class AaroHistoricalVol2Adapter(BaseAdapter):
    """
    美國國防部 AARO 歷史記錄報告第二卷 (Historical Record Report Vol. 2) 適配器
    索引依據 NDAA 法定要求編纂之當代國會吹哨人指控、機密專案審計與官方調查結論更新案卷
    """
    TARGET_RECORDS = [
        {
            "id": "DOD-AARO-HISTORICAL-VOL2-STATUTORY",
            "title": "DoD AARO: Report on the Historical Record of USG Involvement with UAP (Volume 2 - Contemporary Allegations Review)",
            "zh_title": "美國國防部 AARO：美國政府涉 UAP 歷史記錄審查報告 (第二卷 - 當代吹哨指控與專案審計)",
            "zh_summary": "依據國防授權法法定審查義務，AARO 針對近期國會宣誓聽證會吹哨人指控、非公開特殊權限專案 (USAP) 傳聞、敏感國防承包商實體物證查驗及跨機構情報訪談所發布之官方審計報告第二卷。",
            "date": "2024-11-20",
            "url": "https://www.aaro.mil",
            "agencies": [
                "Department of Defense",
                "All-domain Anomaly Resolution Office (AARO)",
                "Office of the Director of National Intelligence"
            ]
        }
    ]

    @property
    def source_name(self) -> str:
        return "aaro_historical_vol2"

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
                "evidence_level": "official_statutory_historical_audit_vol2",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Statutory Volume 2 historical evaluation compiled by AARO investigating contemporary whistleblower allegations, special access architectures, and material verification."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"DoD AARO Statutory Publication ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
