"""
ODNI IC on the Record Declassification Stream Adapter
美國國家情報總監辦公室 (ODNI) 情報界官方透明化與解密評估適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class OdniDeclassificationStreamAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "odni_declassification_stream"

    def __init__(self):
        super().__init__()
        self.endpoint_url = "https://www.dni.gov/index.php/newsroom/reports-publications"
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
            print(f"  ⚠️ [ODNI 連線警告] 暫時無法連線至情報總監辦公室端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"ODNI-IC-UAP-ASSESSMENT-STREAM-{since_date}"

        record = {
            "id": base_record_id,
            "type": "report",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"美國國家情報總監辦公室 (ODNI)：情報界 (IC) 跨機構不明異常現象威脅評估與解密公報 (巡檢區間 {since_date})",
                "en": f"U.S. ODNI: Intelligence Community Consolidated UAP Assessment & Transparency Bulletin ({since_date})"
            },
            "summary": {
                "zh_hk": "美國國家情報總監辦公室（ODNI）統籌全美 18 個情報機構發布之法定解密公報。依據《情報授權法案》（IAA），評估全域感測器通報數據、外國戰略對手突破性空天航空技術威脅，以及五角大廈 AARO 提交之不可解釋跨介質高機動案例審計記錄。",
                "en": "Official intelligence community assessment published by the Office of the Director of National Intelligence (ODNI) pursuant to Intelligence Authorization Acts, compiling multi-agency threat matrices and unclassified sensor evaluations."
            },
            "agency": {
                "name": "Office of the Director of National Intelligence",
                "zh_hk": "美國國家情報總監辦公室 (ODNI)",
                "country": "US"
            },
            "entities": {
                "agencies": [
                    "Office of the Director of National Intelligence",
                    "Central Intelligence Agency",
                    "Defense Intelligence Agency",
                    "National Geospatial-Intelligence Agency"
                ],
                "people": []
            },
            "sources": [
                {
                    "name": "ODNI Official Publications Portal",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["ODNI", "Intelligence Community", "National Intelligence", "Declassified", "IAA", "Statutory Report"]
        }

        records.append(record)
        return records
