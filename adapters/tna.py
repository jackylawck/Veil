# adapters/tna.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class TnaAdapter(BaseAdapter):
    """
    英國國家檔案館 (The National Archives, UK) 適配器
    索引英國國防部 (MoD) 官方解密移交之五眼聯盟歷史檔案 (DEFE 24 / DEFE 31 系列)
    """
    TARGET_RECORDS = [
        {
            "id": "TNA-DEFE-24-1925",
            "title": "Ministry of Defence: Air Technical Intelligence UFO Reports (DEFE 24/1925)",
            "zh_title": "英國國防部：空軍技術情報處 UFO 正式調查解密檔案卷",
            "zh_summary": "由英國國防部空軍情報組建立並移交英國國家檔案館永久典藏之官方解密卷宗，收錄冷戰時期英國皇家空軍 (RAF) 雷達截擊與目擊事件分析紀錄。",
            "date": "2009-08-17",
            "url": "https://discovery.nationalarchives.gov.uk/details/r/C10103138",
            "agencies": ["The National Archives (UK)", "Ministry of Defence (MoD)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "tna"

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
                "evidence_level": "official_foreign_archive",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Declassified UK Ministry of Defence records permanently transferred to The National Archives under the Freedom of Information Act."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"UK National Archives Discovery ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
