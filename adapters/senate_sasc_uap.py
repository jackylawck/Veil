# adapters/senate_sasc_uap.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class SenateSascUapAdapter(BaseAdapter):
    """
    美國參議院軍事委員會 (SASC) 新興威脅小組委員會 UAP 公開審查聽證會適配器
    索引 2024 年 11 月參議院就全域異常解析辦公室 (AARO) 調查與基地空域入侵之法定審查案卷
    """
    TARGET_RECORDS = [
        {
            "id": "US-SENATE-SASC-AARO-HEARING-20241119",
            "title": "Senate Armed Services Subcommittee on Emerging Threats: Open Hearing on the DoD All-Domain Anomaly Resolution Office",
            "zh_title": "美國參議院軍事委員會新興威脅小組：國防部全域異常解析辦公室 (AARO) 運作與空域威脅公開審查聽證會",
            "zh_summary": "由參議員 Kirsten Gillibrand 主持，AARO 主任 Jon Kosloski 博士就國防部年度調查進展、基地空域不明目標入侵事件及軍方跨部門去保密化進程，向參議院軍事委員會提供之正式宣誓聽證出版品。",
            "date": "2024-11-19",
            "url": "https://www.armed-services.senate.gov",
            "agencies": [
                "US Senate Committee on Armed Services",
                "Subcommittee on Emerging Threats and Capabilities",
                "All-domain Anomaly Resolution Office (AARO)"
            ]
        }
    ]

    @property
    def source_name(self) -> str:
        return "senate_sasc_uap"

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
                "evidence_level": "official_senate_subcommittee_hearing",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official Senate Armed Services hearing testimony and case analysis reviewing DoD anomaly tracking, sensor telemetry, and installation security."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Senate Armed Services Committee Hearing Record ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
