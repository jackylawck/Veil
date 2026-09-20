# adapters/lac.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class LacAdapter(BaseAdapter):
    """
    加拿大國家圖書館暨檔案館 (LAC) 適配器
    索引五眼聯盟盟國加拿大國防部 (DND) 與運輸部 Project Magnet 官方解密檔案
    """
    TARGET_RECORDS = [
        {
            "id": "LAC-RG24-PROJECT-MAGNET",
            "title": "Department of Transport: Project Magnet Official Memoranda (RG 24 / RG 77)",
            "zh_title": "加拿大運輸部與國防部：磁力計畫 (Project Magnet) 官方解密檔案",
            "zh_summary": "加拿大聯邦政府於 1950 年代設立之官方研究專案。由資深通訊工程師主持，在國防研究委員會（DRB）支援下，針對異常地磁波動與未知飛行器推進技術進行官方科學評估，全宗由加拿大國家檔案館永久典藏。",
            "date": "1950-11-20",
            "url": "https://www.bac-lac.gc.ca/eng/discover/unusual/ufo/Pages/default.aspx",
            "agencies": ["Library and Archives Canada", "Department of National Defence (Canada)", "Department of Transport"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "lac"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "declassified_archive",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_commonwealth_archive",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Historical Five Eyes alliance declassified records released by Library and Archives Canada under federal disclosure access."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"LAC Collection Search ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
