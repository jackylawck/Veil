# adapters/aaro_annual_report.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class AaroAnnualReportAdapter(BaseAdapter):
    """
    五角大廈 AARO 法定財政年度綜合報告 (Consolidated Annual Report) 適配器
    索引依據 50 U.S.C. § 3373 法定要求提交國會之年度空域通報、核設施入侵與物證處置架構更新
    """
    TARGET_RECORDS = [
        {
            "id": "DOD-AARO-ANNUAL-REPORT-STATUTORY",
            "title": "DoD AARO: Consolidated Annual Report on Unidentified Anomalous Phenomena",
            "zh_title": "美國國防部 AARO：未知異常現象 (UAP) 法定財政年度綜合報告與核設施入侵審查",
            "zh_summary": "依據聯邦法規 50 U.S.C. § 3373 向國會提交之年度法定解密全卷。統整全美軍事與海軍艦隊最新通報、登錄多起核武器與戰略設施周邊異常空情，並首度載明五角大廈針對潛在回收異常實體材料所制定之跨部會官方處理處置規程。",
            "date": "2026-07-21",
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
        return "aaro_annual_report"

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
                "evidence_level": "official_statutory_annual_defense_report",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Mandated congressional annual report summarizing military sensor logs, nuclear installation incursions, and formal procedures for handling potential anomalous materials."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"DoD AARO Official Annual Release ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
