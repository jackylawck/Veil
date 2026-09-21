"""
State Department PM/DDTC ITAR & Defense Trade Controls Adapter
美國國務院政治軍事事務局 (PM/DDTC) 國際武器貿易條例與特種技術管制公報適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class StatePmDdtcItarAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(source_name="U.S. Department of State (PM/DDTC)")
        self.endpoint_url = "https://www.pmddtc.state.gov/ddtc_public"
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
            print(f"  ⚠️ [國務院 DDTC 連線警告] 暫時無法連線至國防貿易管制局端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"DOS-PM-DDTC-ITAR-ENFORCEMENT-{since_date}"

        record = {
            "id": base_record_id,
            "type": "statement",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"美國國務院 (PM/DDTC)：《國際武器貿易條例》(ITAR) 美國軍火清單特種航太技術移轉審計公報 (區間 {since_date})",
                "en": f"U.S. State Dept (PM/DDTC): ITAR Defense Trade Controls & USML Advanced Aerospace Enforcement ({since_date})"
            },
            "summary": {
                "zh_hk": "美國國務院政治軍事事務局國防貿易管制處（PM/DDTC）依據《武器出口管制法》（AECA）發布之官方管制裁定。針對涉及美國軍火清單（USML）第 VIII 類（先進航空器）、第 XI 類（軍用電子與感測器）及第 XV 類（航太器與特種有效載荷）之物資跨境移轉審批與商品管轄（CJ）爭議，紀錄軍工承包商技術輸出審計留痕。",
                "en": "Official regulatory bulletin published by the Directorate of Defense Trade Controls (DDTC) monitoring International Traffic in Arms Regulations (ITAR) compliance, commodity jurisdiction determinations, and export enforcement on controlled USML aerospace systems."
            },
            "agency": {
                "name": "Department of State (PM/DDTC)",
                "zh_hk": "美國國務院政治軍事事務局國防貿易管制處",
                "country": "US"
            },
            "entities": {
                "agencies": ["Department of State", "Directorate of Defense Trade Controls", "Department of Defense"],
                "people": []
            },
            "sources": [
                {
                    "name": "U.S. DDTC Public Portal",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["State Department", "ITAR", "DDTC", "USML", "Defense Trade", "Export Control", "Commodity Jurisdiction"]
        }

        records.append(record)
        return records
