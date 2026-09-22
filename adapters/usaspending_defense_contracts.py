"""
USASpending Defense Prime Contracts & R&D Funding Adapter
美國聯邦支出系統 (USASpending) 國防特種前沿合約與先進研發資金追蹤適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class UsaspendingDefenseContractsAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "usaspending_defense_contracts"

    def __init__(self):
        super().__init__(source_name="USASpending Defense R&D Ledger")
        self.api_url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
        self.timeout = 20
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)",
            "Content-Type": "application/json"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        now_dt = datetime.now(timezone.utc)
        since_date = (now_dt - timedelta(days=days_back)).strftime("%Y-%m-%d")

        # 檢索條件：針對國防部前沿研發與先進材料相關之聯邦支出合約
        payload = {
            "filters": {
                "time_period": [
                    {"start_date": since_date, "end_date": now_dt.strftime("%Y-%m-%d")}
                ],
                "award_type_codes": ["A", "B", "C", "D"],  # 聯邦合約與採購單
                "keywords": ["anomalous", "aerospace materials", "exotic propulsion", "DARPA defense research"]
            },
            "fields": ["Award ID", "Recipient Name", "Award Amount", "Description", "Action Date"],
            "limit": 3,
            "page": 1
        }

        try:
            resp = requests.post(self.api_url, json=payload, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])

                for item in results:
                    award_id = item.get("Award ID", "UNKNOWN_AWARD")
                    recipient = item.get("Recipient Name", "Defense Contractor")
                    amount = item.get("Award Amount", 0)
                    action_date = item.get("Action Date", since_date)
                    desc = item.get("Description", "Advanced Aerospace and Defence Technical Support Contract.")

                    award_hash = hashlib.sha256(f"USASPEND-{award_id}-{action_date}".encode("utf-8")).hexdigest()
                    now_iso = now_dt.isoformat()

                    record = {
                        "id": f"USASPEND-DEFENSE-AWARD-{award_id.replace('/', '-')}",
                        "type": "report",
                        "evidence_level": "official_document",
                        "date": {
                            "val": action_date,
                            "precision": "day"
                        },
                        "title": {
                            "zh_hk": f"美國國防部前沿合約審計：授權 {recipient} 之聯邦研發資金 (合約代碼 {award_id})",
                            "en": f"U.S. DoD Advanced Award Audit: Obligated Federal R&D to {recipient} (ID: {award_id})"
                        },
                        "summary": {
                            "zh_hk": f"依據美國聯邦支出透明度法規，財政部總帳記錄國防部向主承包商【{recipient}】撥付之先進前沿科技研發合約（金額約 ${amount:,.2f} 美元）。該合約涉及特種航太材料、感測器整合或非常規推進領域之公共審計存證。",
                            "en": f"Federal transparency audit trail recording Department of Defense prime contract award obligation to {recipient} totaling ${amount:,.2f}, referencing classified or advanced aerospace materials development."
                        },
                        "agency": {
                            "name": "Department of Defense / Department of the Treasury",
                            "zh_hk": "美國國防部／美國財政部支出數據審計署",
                            "country": "US"
                        },
                        "entities": {
                            "agencies": ["Department of Defense", "DARPA", "Defense Contract Audit Agency"],
                            "people": []
                        },
                        "sources": [
                            {
                                "name": "USASpending Official Federal Awards Portal",
                                "url": f"https://www.usaspending.gov/award/CONT_AW_{award_id}",
                                "format": "html",
                                "sha256": award_hash,
                                "sha256_verified": False,
                                "archived_at": now_iso
                            }
                        ],
                        "tags": ["USASpending", "Defense Contracts", "Black Budget", "DARPA", "Procurement Audit"]
                    }
                    records.append(record)

        except Exception as exc:
            print(f"  ⚠️ [USASpending 連線警告] 暫時無法拉取聯邦合約數據: {exc}", file=sys.stderr)

        return records
