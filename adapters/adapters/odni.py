# adapters/odni.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class OdniAdapter(BaseAdapter):
    """
    美國國家情報總監辦公室 (ODNI) 官方報告適配器
    索引由美國情報界 (Intelligence Community) 呈交國會之法定年度評估報告
    """
    TARGET_REPORTS = [
        {
            "id": "ODNI-UAP-2021-PE",
            "title": "Preliminary Assessment: Unidentified Aerial Phenomena",
            "zh_title": "國家情報總監辦公室：不明空中現象初步評估官方報告 (2021)",
            "zh_summary": "美國情報界歷史上首份呈交國會之官方公開評估，統整 2004 至 2021 年間 144 起美軍飛行員遭遇事件，確立異常現象對飛航安全與國家安全構成實質挑戰。",
            "date": "2021-06-25",
            "url": "https://www.dni.gov/files/ODNI/documents/assessments/Preliminary-Assessment-UAP-20210625.pdf",
            "agencies": ["Office of the Director of National Intelligence", "Unidentified Aerial Phenomena Task Force (UAPTF)"]
        },
        {
            "id": "ODNI-UAP-2023-ANNUAL",
            "title": "Annual Report on Unidentified Anomalous Phenomena (2023)",
            "zh_title": "國家情報總監辦公室：2023 年度 UAP 法定綜合評估報告",
            "zh_summary": "依據 NDAA 條款編撰之情報界年度報告，詳細載明新通報之數百起跨領域異常案例、感測器特徵分類及跨部會聯絡機制運作現況。",
            "date": "2023-10-17",
            "url": "https://www.dni.gov/files/ODNI/documents/assessments/Unclassified-2023-Annual-Report-on-UAP.pdf",
            "agencies": ["Office of the Director of National Intelligence", "All-Domain Anomaly Resolution Office (AARO)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "odni"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_REPORTS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "intelligence_assessment",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_intelligence_assessment",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Unclassified intelligence community strategic assessment prepared for Congress pursuant to statutory oversight requirements."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"ODNI Official Publication ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
