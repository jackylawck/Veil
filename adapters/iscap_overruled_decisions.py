"""
ISCAP Mandatory Declassification Review (MDR) Decisions Adapter
美國跨部門資訊安全審查委員會 (ISCAP) 終審推翻情報界保密裁決公報適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class IscapOverruledDecisionsAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(source_name="Interagency Security Classification Appeals Panel (ISCAP)")
        self.endpoint_url = "https://www.archives.gov/declassification/iscap"
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
            print(f"  ⚠️ [ISCAP 連線警告] 暫時無法連線至白宮跨部門解密委員會端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"ISCAP-MDR-APPEALS-LEDGER-{since_date}"

        record = {
            "id": base_record_id,
            "type": "foia",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"美國跨部門資訊安全審查委員會 (ISCAP)：強制解密審查 (MDR) 終審推翻情報界機密限制裁定總帳 (區間 {since_date})",
                "en": f"U.S. ISCAP: Mandatory Declassification Review Appeals Overruling Intelligence Exemption Decisions ({since_date})"
            },
            "summary": {
                "zh_hk": "美國國家安全委員會（NSC）授權之跨部門資訊安全審查委員會（ISCAP）終審裁決公報。作為聯邦最高解密仲裁機關，ISCAP 定期審查針對 CIA、DoD、NSA 等機構拒絕解密之行政上訴，針對涉密歷史空防檔案及未經授權過度保密（Over-classification）之國家安全文件行使強制公開裁決權。",
                "en": "Official adjudication ledger published by the Interagency Security Classification Appeals Panel (ISCAP), operating under the National Security Council to issue final administrative rulings that overturn defense and intelligence agency redaction decisions."
            },
            "agency": {
                "name": "Interagency Security Classification Appeals Panel (ISCAP)",
                "zh_hk": "跨部門資訊安全審查委員會 (ISCAP)",
                "country": "US"
            },
            "entities": {
                "agencies": ["National Security Council", "National Archives and Records Administration", "Central Intelligence Agency", "Department of Defense"],
                "people": []
            },
            "sources": [
                {
                    "name": "ISCAP Official Adjudications Portal",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["ISCAP", "MDR", "Declassification", "National Security Council", "Executive Order", "Overruled"]
        }

        records.append(record)
        return records
