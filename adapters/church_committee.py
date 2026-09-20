# adapters/church_committee.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class ChurchCommitteeAdapter(BaseAdapter):
    """
    美國參議院丘奇委員會 (Church Committee) 官方調查報告適配器
    索引美國國會調查情報界非受控機密專案與憲制監督之法定歷史出版品 (Book I-VII)
    """
    TARGET_RECORDS = [
        {
            "id": "US-SENATE-CHURCH-COMM-1976",
            "title": "US Senate Select Committee: Final Report on Intelligence Activities and the Rights of Americans (Senate Report 94-755)",
            "zh_title": "美國參議院丘奇特別委員會：政府情報活動與跨部門特殊權限專案最終調查報告",
            "zh_summary": "美國參議院依據第 21 號決議成立之特別委員會正式發行之第 94-755 號參議院出版品。首度經國會聽證與解密調查，確認情報機構與軍方長期存在未受民選國會完整審計之機密專案體系，為外星政治學研究深層機密控制之法定依據。",
            "date": "1976-04-26",
            "url": "https://www.senate.gov",
            "agencies": ["US Senate", "Select Committee on Intelligence Activities", "Government Publishing Office (GPO)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "church_committee"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "official_report",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_senate_investigation_report",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Statutory congressional investigative reports published by the US Senate detailing compartmented defense and intelligence oversight structures."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"US Senate GPO Report ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
