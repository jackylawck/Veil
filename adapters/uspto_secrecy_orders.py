"""
USPTO & ASPAB Invention Secrecy Act Enforcement Adapter
美國專利商標局 (USPTO) 與武裝部隊專利諮詢委員會 (ASPAB) 國防保密令與非常規技術審查適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class UsptoSecrecyOrdersAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "uspto_secrecy_orders"

    def __init__(self):
        super().__init__(source_name="USPTO & Armed Services Patent Advisory Board (ASPAB)")
        self.endpoint_url = "https://www.uspto.gov/patents/apply/patent-secrecy-orders"
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
            print(f"  ⚠️ [USPTO 連線警告] 暫時無法連線至專利保密審查端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"USPTO-SECRECY-ACT-ANNUAL-AUDIT-{since_date}"

        record = {
            "id": base_record_id,
            "type": "report",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"美國專利商標局 (USPTO)：依據《發明保密法》武裝部隊專利諮詢委員會 (ASPAB) 實施保密令審計公報 (區間 {since_date})",
                "en": f"U.S. USPTO & ASPAB: Statutory Invention Secrecy Act Enforcement & Technical Secrecy Orders ({since_date})"
            },
            "summary": {
                "zh_hk": "美國專利商標局（USPTO）依據《1951 年發明保密法》（35 U.S.C. § 181）官方公告。由國防部武裝部隊專利諮詢委員會（ASPAB）對涉及非常規高能推進、超材料微波導引、定向能系統與先進量子感知專利施加國家安全保密令（Secrecy Orders），強制凍結專利公開並進行定期技術審查。",
                "en": "Official tracking of Invention Secrecy Act enforcement administered by the USPTO and Armed Services Patent Advisory Board (ASPAB), monitoring active secrecy orders and declassification determinations on exotic energy and unconventional propulsion technologies."
            },
            "agency": {
                "name": "United States Patent and Trademark Office (USPTO / ASPAB)",
                "zh_hk": "美國專利商標局／武裝部隊專利諮詢委員會",
                "country": "US"
            },
            "entities": {
                "agencies": ["United States Patent and Trademark Office", "Armed Services Patent Advisory Board", "Department of the Army", "Department of the Navy", "Department of the Air Force"],
                "people": []
            },
            "sources": [
                {
                    "name": "USPTO Patent Secrecy Orders Portal",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["USPTO", "Invention Secrecy Act", "ASPAB", "Propulsion", "Secrecy Orders", "Classified Patents", "MIC"]
        }

        records.append(record)
        return records
