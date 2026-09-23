"""
DoD Office of Inspector General (OIG) Audit Adapter
美國國防部監察長辦公室 (DoD OIG) 國防審計與 UAP 應對評估適配器
"""
import hashlib
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class DodOigEvaluationsAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "dod_oig_evaluations"

    def __init__(self):
        super().__init__()
        self.endpoint_url = "https://www.dodig.mil/Reports/"
        self.timeout = 15
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []

        base_record_id = "DOD-OIG-UAP-EVALUATION-AUDIT"
        oig_url = self.endpoint_url

        try:
            resp = requests.get(oig_url, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                content_sha = hashlib.sha256(resp.content).hexdigest()
            else:
                content_sha = None
        except Exception as exc:
            print(f"  ⚠️ [DoD OIG 連線警告] 暫時無法連線至國防監察長端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = datetime.now(timezone.utc).isoformat()

        record = {
            "id": base_record_id,
            "type": "report",
            "evidence_level": "official_document",
            "date": {
                "val": "2024-01-25",
                "precision": "day"
            },
            "title": {
                "zh_hk": "美國國防部監察長 (DoD OIG)：國防部應對不明異常現象 (UAP) 政策與軍事職責法定審計報告",
                "en": "DoD Office of Inspector General (OIG): Evaluation of the DoD's Actions Regarding Unidentified Anomalous Phenomena"
            },
            "summary": {
                "zh_hk": "美國國防部監察長辦公室（DoD OIG，報告代號 DODIG-2024-054）發布之獨立法定審計公報。評估美軍作戰司令部、參謀長聯席會議及各軍種在偵測、報告與分析 UAP 威脅上的政策完整性，指出全軍未協調一致之安全盲區，並針對黑預算計畫與吹哨人保護機制提出強制整改建議。",
                "en": "Independent statutory audit report by the DoD Office of Inspector General (Report No. DODIG-2024-054) evaluating military commands and intelligence components regarding systemic gaps in unidentified aerial threat detection and reporting compliance."
            },
            "agency": {
                "name": "Department of Defense Office of Inspector General",
                "zh_hk": "美國國防部監察長辦公室 (DoD OIG)",
                "country": "US"
            },
            "entities": {
                "agencies": [
                    "Department of Defense Office of Inspector General",
                    "Joint Chiefs of Staff",
                    "All-domain Anomaly Resolution Office",
                    "United States Northern Command"
                ],
                "people": []
            },
            "sources": [
                {
                    "name": "DoD OIG Official Publications Portal",
                    "url": oig_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": [
                "DoD OIG",
                "Inspector General",
                "Statutory Audit",
                "Internal Oversight",
                "Whistleblower Protection",
                "DODIG-2024-054"
            ]
        }

        records.append(record)
        return records
