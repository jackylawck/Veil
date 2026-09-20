# adapters/nasa.py
import json
from typing import Any, Dict, List
import requests
from .base import BaseAdapter


class NasaAdapter(BaseAdapter):
    """
    美國國家航空暨太空總署 (NASA) 官方技術研究適配器
    專門索引 NASA 獨立研究團隊 (Independent Study Team) 官方發布報告與科學數據
    """
    BASE_URL = "https://ntrs.nasa.gov/api/citations"

    TARGET_REPORTS = [
        {
            "id": "NASA-UAP-IST-2023",
            "title": "NASA Unidentified Anomalous Phenomena Independent Study Team Report",
            "zh_title": "NASA 未知異常現象 (UAP) 獨立科學研究團隊官方正式報告",
            "zh_summary": "由 16 位橫跨天體物理學、數據科學、航空安全等領域專家歷時一年編撰之官方里程碑報告，提出將民間衛星、大數據及人工智慧導入異常現象跨機構校準之法定科學藍圖。",
            "date": "2023-09-14",
            "url": "https://science.nasa.gov/uap/",
            "agencies": ["NASA", "NASA Science Mission Directorate"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "nasa"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        for item in self.TARGET_REPORTS:
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
                "evidence_level": "official_scientific_report",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official scientific advisory report outlining rigorous methodologies, sensor calibration, and open-source data analytics frameworks for aerospace anomaly tracking."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": "NASA Science Directorate Official Publication",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
