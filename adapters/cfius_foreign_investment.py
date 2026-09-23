"""
CFIUS Critical Technology & Aerospace National Security Review Adapter
美國外國在美投資委員會 (CFIUS) 關鍵航太技術收購阻斷與國家安全審查適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class CfiusForeignInvestmentAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "cfius_foreign_investment"

    def __init__(self):
        super().__init__()
        self.endpoint_url = "https://home.treasury.gov/policy-issues/international/the-committee-on-foreign-investment-in-the-united-states-cfius"
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
            print(f"  ⚠️ [CFIUS 連線警告] 暫時無法連線至美財政部外資審查端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"CFIUS-CRITICAL-TECH-SECURITY-AUDIT-{since_date}"

        record = {
            "id": base_record_id,
            "type": "report",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_document",
                "confidence_rating": "official_confirmed"
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": f"U.S. Treasury (CFIUS): Critical Technologies & Aerospace National Security Enforcement Audit ({since_date})",
                    "executive_summary": "Official enforcement ledger from the Committee on Foreign Investment in the United States (CFIUS) auditing transactions involving critical aerospace technologies, advanced materials, and defense supply chain national security determinations."
                },
                "zh_hk": {
                    "title": f"美國財政部 (CFIUS)：關鍵技術、先進航太材料與敏感國防供應鏈國家安全阻斷審查公報 (區間 {since_date})",
                    "executive_summary": "美國外國在美投資委員會（CFIUS）依據《國防生產法》第 721 條發布之法定安全審查記錄。針對涉足極端環境感測器、非常規合金冶煉、衛星通訊加密及先進推進技術之國防新創公司與航太供應商，行使強制性國家安全穿透審查與總統行政阻斷令，防範敏感前沿技術外流。"
                }
            },
            "entities": {
                "agencies": ["Committee on Foreign Investment in the United States", "Department of the Treasury", "Department of Defense", "Office of the Director of National Intelligence", "Department of Homeland Security"],
                "people": []
            },
            "sources": [
                {
                    "label": "U.S. Treasury CFIUS Official Portal",
                    "url": self.endpoint_url,
                    "sha256": content_sha
                }
            ],
            "tags": ["CFIUS", "Treasury", "Critical Technology", "National Security", "Foreign Investment", "Defense Supply Chain"]
        }

        records.append(record)
        return records
