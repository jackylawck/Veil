# adapters/federal_register.py
from datetime import datetime, timedelta
import json
from typing import Any, Dict, List
import requests
from .base import BaseAdapter


class FederalRegisterAdapter(BaseAdapter):
    BASE_URL = "https://www.federalregister.gov/api/v1/documents.json"

    @property
    def source_name(self) -> str:
        return "federal_register"

    def fetch_records(self, days_back: int = 7) -> List[Dict[str, Any]]:
        start_date = (datetime.utcnow() - timedelta(days=days_back)).strftime(
            "%Y-%m-%d"
        )

        # 採用嚴格精確短語搜尋，避免單字拆解雜訊
        params = {
            "conditions[term]": (
                '"unidentified anomalous phenomena" OR "AARO" OR "unidentified'
                ' aerial phenomena"'
            ),
            "conditions[publication_date][gte]": start_date,
            "conditions[type][]": ["RULE", "NOTICE", "PRESDOCU"],
            "conditions[agencies][]": [
                "defense-department",
                "national-aeronautics-and-space-administration",
                "federal-aviation-administration",
            ],
            "per_page": 100,
            "order": "newest",
            "fields[]": [
                "document_number",
                "title",
                "abstract",
                "publication_date",
                "html_url",
                "agencies",
                "type",
            ],
        }

        results: List[Dict[str, Any]] = []
        page = 1

        while True:
            params["page"] = page
            res = requests.get(self.BASE_URL, params=params, timeout=15)
            res.raise_for_status()
            data = res.json()
            raw_items = data.get("results", [])

            for item in raw_items:
                results.append(self._normalize(item))

            # 分頁終止判定
            total_count = data.get("count", 0)
            if len(results) >= total_count or not raw_items:
                break
            page += 1

        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        doc_num = raw.get("document_number", "UNKNOWN")

        return {
            "id": f"FR-{doc_num}",
            "type": "official_notice",
            "date": {"val": raw.get("publication_date"), "precision": "day"},
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_document",
                "confidence_rating": "official_confirmed",
            },
            "entities": {
                "agencies": [
                    a.get("raw_name") for a in raw.get("agencies", [])
                ],
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw.get("title", ""),
                    "executive_summary": raw.get("abstract") or "",
                },
                "zh_hk": {
                    "title": "",  # 留空供審查時編輯填寫
                    "executive_summary": "",
                },
            },
            "sources": [
                {
                    "label": f"Federal Register Doc #{doc_num}",
                    "url": raw.get("html_url"),
                    "sha256": self.calculate_sha256(raw_str),
                }
            ],
        }
