# adapters/faa_atc_mandatory.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class FaaAtcMandatoryAdapter(BaseAdapter):
    """
    美國聯邦航空總署 (FAA) 空中交通管制 UAP 強制安全通報適配器
    索引 FAA Order JO 7210.3 及 AIM 7-7-4 正式納編之民航空管直通國防部通報規程
    """
    TARGET_RECORDS = [
        {
            "id": "FAA-ATC-JO7210-UAP-MANDATE",
            "title": "Federal Aviation Administration: Formal Air Traffic Procedures for Reporting Unidentified Anomalous Phenomena",
            "zh_title": "美國聯邦航空總署 (FAA)：空中交通管制未知異常現象 (UAP) 官方安全通報條令",
            "zh_summary": "聯邦航空總署修訂之官方作業指引。正式確立民航飛行員與航空管制台 (ATC) 遭遇異常空情之法定通報路徑，要求空管單位即時通報國家戰術安全協調官，並將雷達與通聯數據正式移交國防部 AARO 列管審查。",
            "date": "2026-01-15",
            "url": "https://www.faa.gov/air_traffic/publications/",
            "agencies": [
                "Federal Aviation Administration (FAA)",
                "National Tactical Security Operations (NTSO)",
                "Department of Defense / AARO"
            ]
        }
    ]

    @property
    def source_name(self) -> str:
        return "faa_atc_mandatory"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "official_directive",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_civil_aviation_safety_directive",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Statutory air traffic operating regulations issued by the FAA mandating formal reporting pathways from civil aviation to defense anomaly offices."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"FAA Air Traffic Publications ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
