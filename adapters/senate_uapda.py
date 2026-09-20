# adapters/senate_uapda.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class SenateUapdaAdapter(BaseAdapter):
    """
    美國參議院跨黨派《未知異常現象披露法案》(UAP Disclosure Act - UAPDA) 適配器
    索引參議院多數黨領袖 Schumer 與參議員 Rounds 提案之法定非人類智慧 (NHI) 與聯邦徵收權法案條文
    """
    TARGET_RECORDS = [
        {
            "id": "US-SENATE-UAPDA-SCHUMER-ROUNDS",
            "title": "US Senate: Unidentified Anomalous Phenomena Disclosure Act (Schumer-Rounds Amendment)",
            "zh_title": "美國參議院：未知異常現象披露法案 (UAPDA / 舒默-朗茲跨黨派法案)",
            "zh_summary": "由參議院多數黨領袖 Chuck Schumer 與參議員 Mike Rounds 跨黨派提出之重大立法。歷史首次於聯邦法律文本中正式定義『非人類智慧 (NHI)』、『未知來源技術』與『歷史遺留專案』，並設立直屬總統之獨立審查委員會及私營承包商物證國家徵收權條款。",
            "date": "2024-07-11",
            "url": "https://www.congress.gov",
            "agencies": [
                "United States Senate",
                "Senate Select Committee on Intelligence",
                "Senate Armed Services Committee"
            ]
        }
    ]

    @property
    def source_name(self) -> str:
        return "senate_uapda"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "legislation",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_statutory_bipartisan_legislation",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Landmark Senate legislative mandate proposing the creation of a presidential Records Review Board and defining Non-Human Intelligence (NHI) within federal law."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"US Senate Congressional Record ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
