# adapters/cefaa.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class CefaaAdapter(BaseAdapter):
    """
    智利民航總局 (DGAC) 與 CEFAA 官方適配器
    索引智利海軍、空軍與民用雷達跨部門異常飛行現象官方調查檔案
    """
    TARGET_RECORDS = [
        {
            "id": "CL-DGAC-CEFAA-20141111",
            "title": "Chilean Navy & DGAC: Official Investigation into the Naval Helicopter Infrared Anomaly Case",
            "zh_title": "智利海軍與民航總局 (CEFAA)：海軍巡邏直升機紅外異常遭遇事件官方調查報告",
            "zh_summary": "2014 年 11 月 11 日智利海軍直升機進行沿海巡邏時，機載高解析度前視紅外感測器 (FLIR) 鎖定並錄製高速異常飛行目標及其熱排放現象。經智利官方委員會歷經兩年跨學科調查後，全卷結論向國際公開。",
            "date": "2014-11-11",
            "url": "https://www.cefaa.gob.cl",
            "agencies": ["Directorate General of Civil Aviation (DGAC)", "Chilean Navy", "CEFAA"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "cefaa"

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
                "evidence_level": "official_aviation_safety_report",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "es",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official military aviation telemetry and forward-looking infrared investigation dossier released by the Chilean Directorate General of Civil Aviation."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"DGAC / CEFAA Official Dossier ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
