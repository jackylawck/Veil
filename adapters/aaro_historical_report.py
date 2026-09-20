# adapters/aaro_historical_report.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class AaroHistoricalReportAdapter(BaseAdapter):
    """
    美國國防部全域異常解析辦公室 (AARO) 歷史記錄報告第一卷 (HR2 Vol. 1) 適配器
    索引依據國防授權法編纂之 1945 年以來美國政府涉 UAP 機密專案官方歷史審計全卷
    """
    TARGET_RECORDS = [
        {
            "id": "DOD-AARO-HISTORICAL-VOL1-2024",
            "title": "DoD AARO: Report on the Historical Record of USG Involvement with Unidentified Anomalous Phenomena (Volume 1)",
            "zh_title": "美國國防部 AARO：美國政府參與未知異常現象歷史記錄官方審查報告 (第一卷)",
            "zh_summary": "依據 2023 財年國防授權法要求，五角大廈 AARO 調閱 1945 年以來的全部涉密檔案與訪談後發布之 63 頁法定審計報告。全面公開歷代官方機密調查全貌，並揭露國土安全部曾秘密提案之 Kona Blue 逆向工程計畫。",
            "date": "2024-03-08",
            "url": "https://www.aaro.mil",
            "agencies": [
                "Department of Defense",
                "All-domain Anomaly Resolution Office (AARO)",
                "Office of the Under Secretary of Defense for Intelligence and Security"
            ]
        }
    ]

    @property
    def source_name(self) -> str:
        return "aaro_historical_report"

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
                "evidence_level": "official_dod_historical_record_review",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official statutory historical review by the Department of Defense examining U.S. government investigations, alleged legacy programs, and special access projects since 1945."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"DoD AARO Official Report Archive ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
