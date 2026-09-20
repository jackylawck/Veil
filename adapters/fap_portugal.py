# adapters/fap_portugal.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class FapPortugalAdapter(BaseAdapter):
    """
    葡萄牙空軍司令部 (Força Aérea Portuguesa) 適配器
    索引葡萄牙國防部官方解密之空軍飛行員編隊飛行遭遇與雷達官方案卷
    """
    TARGET_RECORDS = [
        {
            "id": "PT-FAP-CASTRO-DAIRE-1982",
            "title": "Portuguese Air Force Command: Declassified Report on the Castro Daire Aerial Phenomenon Encounter",
            "zh_title": "葡萄牙空軍司令部：卡斯特羅達伊雷空軍編隊飛行遭遇事件官方解密作戰卷宗",
            "zh_summary": "1982 年 11 月 2 日葡萄牙空軍三名資深飛行教官於高空執行飛行任務時遭不明飛行體近距離盤旋繞飛。空軍參謀本部作戰情報組進行深入技術調查，調查卷宗後由空軍司令部依檔案法正式公開。",
            "date": "1982-11-02",
            "url": "https://www.emfa.pt",
            "agencies": ["Portuguese Air Force (FAP)", "Ministry of National Defence (Portugal)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "fap_portugal"

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
                "evidence_level": "official_nato_air_force_investigation",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "pt",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Declassified Portuguese Air Force operational reports documenting military formation pilot observations and telemetry."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Força Aérea Portuguesa Archive ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
