"""
Armed Services Board of Contract Appeals (ASBCA) Decisions Adapter
美國武裝部隊合約申訴委員會 (ASBCA) 國防機密採購合約裁決公報適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class AsbcaDefenseAppealsAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(source_name="Armed Services Board of Contract Appeals (ASBCA)")
        self.endpoint_url = "https://www.asbca.mil/Decisions/decisions.html"
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
            print(f"  ⚠️ [ASBCA 連線警告] 暫時無法連線至武裝部隊合約申訴委員會端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"ASBCA-DEFENSE-CONTRACT-DISPUTE-{since_date}"

        record = {
            "id": base_record_id,
            "type": "foia",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"美國武裝部隊合約申訴委員會 (ASBCA)：國防部前沿裝備與機密工程採購爭議判決書總帳 (區間 {since_date})",
                "en": f"U.S. ASBCA: Armed Services Board of Contract Appeals Defense Procurement Dispute Decisions ({since_date})"
            },
            "summary": {
                "zh_hk": "美國國防部常設準司法審判機關武裝部隊合約申訴委員會（ASBCA）發布之正式判決書。依據《合約爭端法》（CDA），審理國防巨頭（Lockheed Martin、Northrop Grumman 等）因機密特別存取計畫（SAP）、原型機研發超支或智慧財產權授權爭端對五角大廈提起之法律訴訟，是刺穿軍工採購黑箱之司法原件。",
                "en": "Official administrative tribunal decisions from the Armed Services Board of Contract Appeals (ASBCA) resolving legal disputes between defense contractors and military departments pursuant to the Contract Disputes Act (CDA)."
            },
            "agency": {
                "name": "Armed Services Board of Contract Appeals",
                "zh_hk": "美國武裝部隊合約申訴委員會 (ASBCA)",
                "country": "US"
            },
            "entities": {
                "agencies": ["Armed Services Board of Contract Appeals", "Department of Defense", "Department of the Army", "Department of the Navy", "Department of the Air Force"],
                "people": []
            },
            "sources": [
                {
                    "name": "ASBCA Official Decisions Portal",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["ASBCA", "Contract Disputes", "Procurement Litigation", "Department of Defense", "MIC", "Tribunal Decisions"]
        }

        records.append(record)
        return records
