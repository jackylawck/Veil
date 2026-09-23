"""
Federal Register Administrative Rules & Executive Orders Adapter
美國聯邦公報 (Federal Register) 國家安全解密指引與出口管制動態適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class FederalRegisterRulesAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "federal_register_rules"

    def __init__(self):
        super().__init__()
        self.api_url = "https://www.federalregister.gov/api/v1/documents.json"
        self.timeout = 20
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        now_dt = datetime.now(timezone.utc)
        since_date = (now_dt - timedelta(days=days_back)).strftime("%Y-%m-%d")

        # 檢索涉及國防部、情報總監辦公室及新興航空技術管制的聯邦法規
        params = {
            "conditions[term]": "unidentified aerial OR anomaly resolution OR aerospace export control",
            "conditions[publication_date][gte]": since_date,
            "order": "newest",
            "per_page": 2
        }

        try:
            resp = requests.get(self.api_url, params=params, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])

                for doc in results:
                    doc_num = doc.get("document_number", "UNKNOWN")
                    title = doc.get("title", "Federal Administrative Order")
                    pub_date = doc.get("publication_date", since_date)
                    html_url = doc.get("html_url", "https://www.federalregister.gov")
                    abstract = doc.get("abstract") or "Official executive regulatory document published in the Federal Register."

                    rule_hash = hashlib.sha256(f"FEDREG-{doc_num}-{pub_date}".encode("utf-8")).hexdigest()
                    now_iso = now_dt.isoformat()

                    record = {
                        "id": f"FEDERAL-REGISTER-RULE-{doc_num}",
                        "type": "statement",
                        "evidence_level": "official_document",
                        "date": {
                            "val": pub_date,
                            "precision": "day"
                        },
                        "title": {
                            "zh_hk": f"美國聯邦公報 (Federal Register)：行政法規公報第 {doc_num} 號",
                            "en": f"Federal Register Rule: Official Publication {doc_num}"
                        },
                        "summary": {
                            "zh_hk": f"美國行政部門於《聯邦公報》刊載之正式法律公報。涉及國家安全機密標準、跨機構異常現象數據共享或受控軍事技術之法律規範修正：{abstract[:180]}...",
                            "en": f"Official administrative rule published in the U.S. Federal Register enacting binding national security directives or aerospace technological reporting standards: {abstract[:200]}..."
                        },
                        "agency": {
                            "name": "National Archives and Records Administration (Federal Register)",
                            "zh_hk": "美國聯邦公報處 (OFR)",
                            "country": "US"
                        },
                        "entities": {
                            "agencies": ["National Archives and Records Administration", "Department of Defense", "Office of the Director of National Intelligence"],
                            "people": []
                        },
                        "sources": [
                            {
                                "name": "Federal Register Official Government API",
                                "url": html_url,
                                "format": "html",
                                "sha256": rule_hash,
                                "sha256_verified": False,
                                "archived_at": now_iso
                            }
                        ],
                        "tags": ["Federal Register", "Administrative Law", "Executive Order", "ODNI", "Compliance"]
                    }
                    records.append(record)

        except Exception as exc:
            print(f"  ⚠️ [Federal Register 連線警告] 無法拉取聯邦法規動態: {exc}", file=sys.stderr)

        return records
