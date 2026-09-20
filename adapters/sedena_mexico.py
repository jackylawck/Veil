# adapters/sedena_mexico.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class SedenaMexicoAdapter(BaseAdapter):
    """
    墨西哥國防部 (SEDENA) 與墨西哥空軍 (FAM) 適配器
    索引 2004 年空軍 C-26A 巡邏機前視紅外 (FLIR) 異常飛行物體軍方官方解密卷宗
    """
    TARGET_RECORDS = [
        {
            "id": "MX-SEDENA-FAM-FLIR-20040305",
            "title": "Mexican Air Force Command: Official Release of the C-26A Patrol Aircraft FLIR Infrared Anomaly Dossier",
            "zh_title": "墨西哥國防部與空軍：C-26A 巡邏機前視紅外 (FLIR) 異常目標遭遇事件軍方官方解密報告",
            "zh_summary": "2004 年 3 月 5 日墨西哥空軍巡邏機於坎佩切上空執行任務時，機載軍用紅外感測系統錄下多個高速異常發熱目標。經墨西哥國防部長授權，軍方正式向公眾解密公開原始熱成像影片與機組作戰通訊全卷。",
            "date": "2004-03-05",
            "url": "https://www.gob.mx/defensa",
            "agencies": ["Secretaría de la Defensa Nacional (SEDENA)", "Fuerza Aérea Mexicana (FAM)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "sedena_mexico"

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
                "evidence_level": "official_military_flir_telemetry",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "es",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Declassified Mexican Air Force aerial reconnaissance telemetry and infrared sensor records approved for public release by the Secretariat of National Defense."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"SEDENA Official Dossier ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
