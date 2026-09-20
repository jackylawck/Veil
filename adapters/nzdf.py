# adapters/nzdf.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class NzdfAdapter(BaseAdapter):
    """
    紐西蘭國防軍 (NZDF) 與紐西蘭國家檔案館 (Archives New Zealand) 適配器
    索引五眼聯盟盟國紐西蘭國防軍 1952-2009 年官方解密軍事全卷 (含 1978 凱庫拉雷達光學事件)
    """
    TARGET_RECORDS = [
        {
            "id": "NZ-NZDF-AIR-KAIKOURA-1978",
            "title": "New Zealand Defence Force: Official Declassified Files on the Kaikoura Lights Radar-Visual Incident",
            "zh_title": "紐西蘭國防軍：1978 年凱庫拉空中雷達與光學影像遭遇事件官方解密全卷",
            "zh_summary": "1978 年 12 月貨機機組、隨機記者（錄下彩色錄影）與地面航空管制雷達同步探測到異常飛行目標。紐西蘭空軍與國防科學家進行全面調查，全案於 2010 年由紐西蘭國防軍依官方資訊法全面解密並由國家檔案館典藏。",
            "date": "1978-12-21",
            "url": "https://www.archives.govt.nz",
            "agencies": ["New Zealand Defence Force (NZDF)", "Royal New Zealand Air Force (RNZAF)", "Archives New Zealand"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "nzdf"

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
                "evidence_level": "official_five_eyes_declassified_archive",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Historical declassified defense intelligence files released by the New Zealand Defence Force under the Official Information Act."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Archives New Zealand Official Release ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
