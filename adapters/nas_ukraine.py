# adapters/nas_ukraine.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class NasUkraineAdapter(BaseAdapter):
    """
    烏克蘭國家科學院主要天文台 (MAO NASU) 適配器
    索引國家科學院雙基站光學與全色感測器近地空間異常物體科學監測評估報告
    """
    TARGET_RECORDS = [
        {
            "id": "UA-NAS-MAO-UAP-2022",
            "title": "Main Astronomical Observatory of the National Academy of Sciences of Ukraine: Technical Observations of UAP",
            "zh_title": "烏克蘭國家科學院主要天文台：近地異常空中現象多基站光學技術監測報告",
            "zh_summary": "烏克蘭國家科學院主要天文台學者利用基輔與維納里夫卡雙站同步彩色高速感測器，針對對流層與平流層高速移動未知物體進行之光度學與立體成像技術分析。",
            "date": "2022-08-23",
            "url": "https://arxiv.org/abs/2208.11215",
            "agencies": ["National Academy of Sciences of Ukraine", "Main Astronomical Observatory (MAO)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "nas_ukraine"

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
                "evidence_level": "official_scientific_observational_study",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Observational and photometric measurement study conducted by researchers at the Main Astronomical Observatory, National Academy of Sciences of Ukraine."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"NAS Ukraine Observatory Publication ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
