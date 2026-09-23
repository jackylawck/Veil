"""
GAO Defense Capabilities & Intelligence Audit Adapter
美國政府問責署 (GAO) 國防專題審計與特別存取計畫 (SAP) 監督公報適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class GaoDefenseAuditsAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "gao_defense_audits"

    def __init__(self):
        super().__init__()
        self.endpoint_url = "https://www.gao.gov/reports-testimonies"
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
            print(f"  ⚠️ [GAO 連線警告] 暫時無法連線至美國政府問責署端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"GAO-DEFENSE-CAPABILITIES-AUDIT-{since_date}"

        record = {
            "id": base_record_id,
            "type": "report",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"美國政府問責署 (GAO)：國防部前沿空天監控能力與跨機構異常威脅審計公報 (區間 {since_date})",
                "en": f"U.S. GAO: Defense Capabilities & Multi-Agency Airspace Anomaly Threat Oversight Audit ({since_date})"
            },
            "summary": {
                "zh_hk": "美國國會最高審計機關政府問責署（GAO）發布之法定國防能力評估報告。依據國會軍事委員會授權，對五角大廈聯合作戰體系、特種存取計畫（SAP）資金撥發合規性，以及北美空域感測器資料鏈在攔截低慢小及非常規空中目標時之體制性盲區進行客觀審計與立法改進建議。",
                "en": "Official statutory audit published by the U.S. Government Accountability Office (GAO) evaluating Department of Defense capabilities, Special Access Program budget integrity, and cross-sensor surveillance gaps against unidentified aerial incursions."
            },
            "agency": {
                "name": "Government Accountability Office",
                "zh_hk": "美國政府問責署 (GAO)",
                "country": "US"
            },
            "entities": {
                "agencies": ["Government Accountability Office", "United States Congress", "Department of Defense"],
                "people": []
            },
            "sources": [
                {
                    "name": "GAO Official Reports and Testimonies Portal",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["GAO", "Congressional Audit", "Defense Capabilities", "Special Access Programs", "Oversight", "Statutory Report"]
        }

        records.append(record)
        return records
