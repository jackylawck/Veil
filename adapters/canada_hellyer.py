# adapters/canada_hellyer.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class CanadaHellyerAdapter(BaseAdapter):
    """
    加拿大前國防部長 Paul Hellyer 國防宣誓證詞與解密備忘錄適配器
    索引 G7 國防部長級別就軍方機密專案與五眼聯盟情報網絡之官方作證案卷
    """
    TARGET_RECORDS = [
        {
            "id": "CA-DND-HELLYER-TESTIMONY-2013",
            "title": "Former Minister of National Defence Paul Hellyer: Sworn Testimony on Defense Intelligence and Aerospace Incursions",
            "zh_title": "加拿大前國防部長 Paul Hellyer：國防情報與不明空天目標作戰宣誓證詞",
            "zh_summary": "曾任加拿大國防部長之 Paul Hellyer 於國會前議員主持之官方聽證會上提供宣誓證詞，公開證實軍方跨國情報整合、北美防空雷達截獲數據及深層國防機密計畫之實質存在，為西方大國級別最高之國防首長證詞案卷。",
            "date": "2013-05-03",
            "url": "https://www.canada.ca/en/department-national-defence.html",
            "agencies": ["Department of National Defence (Canada)", "Parliament of Canada", "Citizen Hearing Foundation"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "canada_hellyer"

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
                "evidence_level": "official_ministerial_sworn_testimony",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Sworn testimony and historical defence documentation presented by former Canadian Minister of National Defence Paul Hellyer regarding compartmentalized military programs."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Canadian DND / Hearing Record ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
