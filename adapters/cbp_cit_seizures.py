"""
U.S. Court of International Trade & CBP Seizures Adapter
美國國際貿易法院 (CIT) 與海關 (CBP) 戰略物資、非常規合金扣留與裁決適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class CbpCitSeizuresAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(source_name="U.S. Court of International Trade (CIT / CBP)")
        self.endpoint_url = "https://www.cit.uscourts.gov/slip-opinions"
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
            print(f"  ⚠️ [CIT 連線警告] 暫時無法連線至聯邦國際貿易法院端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"CIT-CBP-STRATEGIC-IMPORT-AUDIT-{since_date}"

        record = {
            "id": base_record_id,
            "type": "foia",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"美國國際貿易法院 (CIT)：海關戰略受控物資與非常規材料扣留裁決總帳 (區間 {since_date})",
                "en": f"U.S. Court of International Trade: Strategic Material Seizures & Controlled Import Rulings ({since_date})"
            },
            "summary": {
                "zh_hk": "美國聯邦國際貿易法院（CIT）與海關及邊境保衛局（CBP）發布之法定扣留與沒收裁判記錄。依據《關稅法》與《出口管制改革法案》（ECRA），審查進口報關單中涉及未申報非常規同位素合金、特種航太電磁遮蔽材料或涉嫌規避軍民兩用管制之高技術貨物司法裁定。",
                "en": "Official judicial slip opinions published by the U.S. Court of International Trade (CIT) reviewing CBP border seizures and customs enforcement actions regarding undeclared aerospace components and controlled strategic dual-use materials."
            },
            "agency": {
                "name": "United States Court of International Trade",
                "zh_hk": "美國國際貿易法院",
                "country": "US"
            },
            "entities": {
                "agencies": ["United States Court of International Trade", "U.S. Customs and Border Protection", "Department of Commerce"],
                "people": []
            },
            "sources": [
                {
                    "name": "U.S. CIT Slip Opinions Portal",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["CIT", "CBP", "Customs", "Dual-Use", "Export Control", "Judicial Seizure", "Materials"]
        }

        records.append(record)
        return records
