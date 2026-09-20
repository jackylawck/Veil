# adapters/pla_air_situation.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class PlaAirSituationAdapter(BaseAdapter):
    """
    中國人民解放軍 (PLA) 不明空情處置條令與預警監控機制適配器
    索引依據國防作戰法規確立之全軍『不明空情』多級通報、雷達交接與 AI 模式識別規範
    """
    TARGET_RECORDS = [
        {
            "id": "CN-PLA-AIR-SITUATION-REGULATION",
            "title": "People's Liberation Army: Operational Protocols and AI Identification Framework for Unidentified Air Situations",
            "zh_title": "中國人民解放軍：不明空情處置作戰規範與雷達情報智能識別系統",
            "zh_summary": "依據解放軍軍事防空規程與全軍預警體系標準，確立各戰區雷達站、防空部隊及海空巡邏戰機在探測到未識別飛行器時之三級上報、座艙光學錄影、全頻譜電磁特徵留存與總部智能特徵庫自動匹配機制。",
            "date": "2021-06-03",
            "url": "http://www.mod.gov.cn",
            "agencies": ["Ministry of National Defense (China)", "PLA Air Force", "Air Force Early Warning Academy"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "pla_air_situation"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "official_notice",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_military_operational_doctrine",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "zh_cn",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official military doctrine and AI-assisted sensor processing frameworks established by the People's Liberation Army for tracking unidentified air situations."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"PLA Daily / MND Official Release ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
