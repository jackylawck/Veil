# adapters/nara_records_collection.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class NaraRecordsCollectionAdapter(BaseAdapter):
    """
    美國國家檔案館 (NARA) 法定 UAP 專屬記錄典藏庫適配器
    索引依據 NDAA FY2024 聯邦法案強制移交、持續解密更新之官方全宗資料庫
    """
    TARGET_RECORDS = [
        {
            "id": "NARA-STATUTORY-UAP-COLLECTION",
            "title": "National Archives and Records Administration: Statutory UAP Records Collection (NDAA FY24 Mandate)",
            "zh_title": "美國國家檔案局 (NARA)：聯邦法定未知異常現象專屬典藏庫 (持續解密更新專案)",
            "zh_summary": "依據 2024 財年國防授權法第 1841-1843 條設立之聯邦常設典藏專案。明令國防部、情報界、能源部等全體聯邦機關限期移交所有涉密歷史檔案、照片、遙測圖譜與軍事日誌，並由國家檔案館向全球公眾持續動態解密公開。",
            "date": "2024-03-15",
            "url": "https://www.archives.gov/research/topics/uaps",
            "agencies": [
                "National Archives and Records Administration (NARA)",
                "Department of Defense",
                "Central Intelligence Agency",
                "Department of Energy"
            ]
        }
    ]

    @property
    def source_name(self) -> str:
        return "nara_records_collection"

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
                "evidence_level": "official_statutory_national_archives_collection",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Statutory permanent collection established by federal mandate at the US National Archives preserving government-wide declassified anomaly dossiers."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"NARA Centralized UAP Collection ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
