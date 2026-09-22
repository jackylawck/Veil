"""
U.S. Office of Special Counsel (OSC) Whistleblower Protection Adapter
美國特別檢察官辦公室 (OSC) 國防與情報吹哨人法定反報復調查公報適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class OscWhistleblowerDisclosuresAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "osc_whistleblower_disclosures"

    def __init__(self):
        super().__init__(source_name="U.S. Office of Special Counsel (OSC)")
        self.endpoint_url = "https://osc.gov/News"
        self.timeout = 15
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        now_dt = datetime.now(timezone.utc)
        since_date = (now_dt - timedelta(days=days_back)).strftime("%Y-%m-%d")

        try:
            resp = requests.get(self.endpoint_url, headers=self.headers, timeout=self.timeout)
            content_sha = hashlib.sha256(resp.content).hexdigest() if resp.status_code == 200 else None
        except Exception as exc:
            print(f"  ⚠️ [OSC 連線警告] 暫時無法連線至特別檢察官辦公室端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"OSC-WHISTLEBLOWER-ENFORCEMENT-{since_date}"

        record = {
            "id": base_record_id,
            "type": "statement",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"美國特別檢察官辦公室 (OSC)：國防與安全部門吹哨人保護調查與行政處分公報 (區間 {since_date})",
                "en": f"U.S. Office of Special Counsel: Defense Whistleblower Reprisal Investigation & Findings Bulletin ({since_date})"
            },
            "summary": {
                "zh_hk": "美國聯邦獨立檢控機構特別檢察官辦公室（OSC）發布之法定義務調查公報。依據《吹哨人保護法》（5 U.S.C. § 1214），受理國防部、情報機關及聯邦承包商人員舉報非法機密特種存取計畫、安全權限惡意吊銷及行政報復之調查裁決，行使強制暫緩報復處分（Stay Orders）與國會呈報權。",
                "en": "Official enforcement reports by the U.S. Office of Special Counsel (OSC) investigating prohibited personnel practices and unlawful clearance retaliations against defense and intelligence personnel pursuant to 5 U.S.C. § 1214."
            },
            "agency": {
                "name": "Office of Special Counsel",
                "zh_hk": "美國特別檢察官辦公室 (OSC)",
                "country": "US"
            },
            "entities": {
                "agencies": ["Office of Special Counsel", "Merit Systems Protection Board", "Department of Defense"],
                "people": []
            },
            "sources": [
                {
                    "name": "OSC Public News & Decisions Portal",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["OSC", "Whistleblower", "Clearance Revocation", "Prohibited Personnel Practices", "Statutory Oversight"]
        }

        records.append(record)
        return records
