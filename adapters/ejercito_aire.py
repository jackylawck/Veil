# adapters/ejercito_aire.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class EjercitoAireAdapter(BaseAdapter):
    """
    西班牙航空與太空軍司令部 (Ejército del Aire y del Espacio) 適配器
    索引西班牙國防部官方解密圖書館 (Biblioteca Virtual de Defensa) 之空軍雷達與飛行員目擊調查案卷
    """
    TARGET_RECORDS = [
        {
            "id": "SP-EDA-EXPEDIENTE-791111",
            "title": "Spanish Air Force General Staff: Official Declassified Report on the Manises Commercial Flight Incident",
            "zh_title": "西班牙空軍參謀本部：曼埃塞斯客機遭遇事件官方解密作戰卷宗 (Expediente 791111)",
            "zh_summary": "1979 年 11 月 11 日載有逾百名乘客之民航客機遭遇不明物體逼近而迫降，空軍作戰司令部緊急派遣戰鬥機攔截之官方調查卷宗。由西班牙國防部官方圖書館依國家解密法令向全球完全公開。",
            "date": "1979-11-11",
            "url": "https://bibliotecavirtual.defensa.gob.es",
            "agencies": ["Ministry of Defence (Spain)", "Ejército del Aire", "Air Operational Command"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "ejercito_aire"

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
                "evidence_level": "official_nato_ally_declassified_archive",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "es",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official declassified military investigation dossiers released by the Spanish Ministry of Defence pursuant to military classification reform acts."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Biblioteca Virtual de Defensa ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
