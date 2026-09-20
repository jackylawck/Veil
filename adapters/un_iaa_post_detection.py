# adapters/un_iaa_post_detection.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class UnIaaPostDetectionAdapter(BaseAdapter):
    """
    聯合國外空司 (UNOOSA) 與國際宇航科學院 (IAA)《地外智慧探測後處置原則宣言》適配器
    索引多邊國際治理框架下探測到地外信號時之公開披露、禁止單方發送回覆及國際通報法定規程
    """
    TARGET_RECORDS = [
        {
            "id": "UN-IAA-SETI-POST-DETECTION-PROTOCOL",
            "title": "UNOOSA & International Academy of Astronautics: Declaration of Principles Concerning Activities Following the Detection of Extraterrestrial Intelligence",
            "zh_title": "聯合國外空司與國際宇航科學院：關於發現地外智慧後續活動原則宣言 (接觸與披露國際公約規程)",
            "zh_summary": "由國際宇航科學院制定並提交聯合國和平利用外層空間委員會 (COPUOS) 之多邊國際協議。確立一旦探測到經確證之地外科技或信號時，簽約國負有經聯合國向全人類公開披露之法定義務，嚴禁個別國家實施單方面機密化隱匿或擅自通訊。",
            "date": "2010-09-30",
            "url": "https://www.unoosa.org",
            "agencies": [
                "United Nations Office for Outer Space Affairs (UNOOSA)",
                "International Academy of Astronautics (IAA)",
                "UN Committee on the Peaceful Uses of Outer Space (COPUOS)"
            ]
        }
    ]

    @property
    def source_name(self) -> str:
        return "un_iaa_post_detection"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "international_treaty",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_international_multilateral_protocol",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Multilateral international governance declaration establishing statutory global transparency and United Nations notification protocols following verified extraterrestrial detections."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"UNOOSA / IAA Legal Protocol Registry ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
