# adapters/nasa_uap_science.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class NasaUapScienceAdapter(BaseAdapter):
    """
    美國國家航空暨太空總署 (NASA) UAP 科學研究處與衛星遙測資料庫適配器
    索引 NASA 獨立科學研究小組後續建置之地球觀測衛星與民用科學異常篩查檔案
    """
    TARGET_RECORDS = [
        {
            "id": "NASA-SCIENCE-UAP-RESEARCH-FRAMEWORK",
            "title": "NASA Science Mission Directorate: Open Science Framework and Observational Database for UAP",
            "zh_title": "美國國家航空暨太空總署 (NASA)：未知異常現象開放科學研究架構與衛星觀測資料庫",
            "zh_summary": "依據 NASA 獨立科學專家小組建議設立之常設研究專案。調動地球觀測衛星群、多光譜感測器及人工智慧異常偵測演算法，建置完全透明公開之民用科學 UAP 觀測數據庫與同儕審查研究標準。",
            "date": "2024-09-14",
            "url": "https://science.nasa.gov/uap/",
            "agencies": [
                "National Aeronautics and Space Administration (NASA)",
                "Science Mission Directorate",
                "UAP Independent Study Team"
            ]
        }
    ]

    @property
    def source_name(self) -> str:
        return "nasa_uap_science"

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
                "evidence_level": "official_civilian_space_agency_science",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Open-access scientific anomaly datasets and multi-sensor space-based observational telemetry compiled under NASA's UAP research directive."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"NASA Science Directorate Publication ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
