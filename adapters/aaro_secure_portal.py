# adapters/aaro_secure_portal.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class AaroSecurePortalAdapter(BaseAdapter):
    """
    五角大廈 AARO 官方安全吹哨者機制 (Secure Reporting Mechanism) 適配器
    索引美國聯邦法令授權豁免 NDA 之國防部官方專案通報與歷史遺留計畫登錄架構
    """
    TARGET_RECORDS = [
        {
            "id": "DOD-AARO-SECURE-REPORTING-PORTAL",
            "title": "DoD AARO: Official Secure Reporting Mechanism for USG & Contractor Personnel with Direct Knowledge",
            "zh_title": "美國國防部 AARO：政府與國防承包商涉密人員官方安全通報機制與專案登記體系",
            "zh_summary": "依據聯邦法律授權建立之官方安全渠道，受國會吹哨人保護條款支持，專門接收知悉 1945 年以來美國政府涉密計畫、材料逆向工程及未受國會審計之特殊權限專案 (SAP) 的現退役人員宣誓呈報。",
            "date": "2023-10-31",
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
        return "aaro_secure_portal"

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
                "evidence_level": "official_statutory_whistleblower_portal",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official Department of Defense statutory secure intake channel for authorized personnel reporting legacy special access programs and materials recovery."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"AARO Official Secure Intake Mechanism ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
