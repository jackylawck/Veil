# adapters/an_brazil.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class AnBrazilAdapter(BaseAdapter):
    """
    巴西國家檔案館 (Arquivo Nacional) 與巴西空軍 (FAB) 適配器
    索引 1986 年巴西空軍『官方 UFO 之夜』及柯拉瑞斯島『普拉托行動 (Operação Prato)』官方解密軍事全卷
    """
    TARGET_RECORDS = [
        {
            "id": "FAB-AN-OVNI-1986-BRIEF",
            "title": "Brazilian Air Force Command: Official Report on the Night of the UFOs (May 19, 1986)",
            "zh_title": "巴西空軍司令部：1986 年『UFO 官方之夜』戰鬥機攔截作戰解密報告全卷",
            "zh_summary": "1986 年 5 月 19 日巴西空軍緊急升空多架幻象 2000 與 F-5E 戰鬥機對多個雷達鎖定之高速異常目標進行攔截。空軍部長隨後召開全國記者會，全案調查報告、雷達軌跡及空軍司令部結論已移交巴西國家檔案館永久公開典藏。",
            "date": "1986-05-19",
            "url": "https://www.gov.br/arquivonacional",
            "agencies": ["Arquivo Nacional (Brazil)", "Força Aérea Brasileira (FAB)", "Ministry of Defence (Brazil)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "an_brazil"

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
                "evidence_level": "official_military_intercept_archive",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "pt",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Declassified Brazilian Air Force Command operational reports and radar telemetry transferred to the National Archives of Brazil under transparency decrees."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Arquivo Nacional Official Fundo ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
