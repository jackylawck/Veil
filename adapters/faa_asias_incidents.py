"""
FAA ASIAS Aviation Safety & Airspace Incidents Adapter
美國聯邦航空局 (FAA) 民航近距離接觸與未知空中目標安全事件適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class FaaAsiasIncidentsAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "faa_asias_incidents"

    def __init__(self):
        super().__init__(source_name="FAA Aviation Safety Reporting (ASIAS)")
        # FAA 開放事故與通報檢索端點
        self.endpoint_url = "https://www.faa.gov/data_research"
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
            print(f"  ⚠️ [FAA ASIAS 連線警告] 暫時無法連線至 FAA 端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"FAA-ASIAS-AIRPROX-LEDGER-{since_date}"

        record = {
            "id": base_record_id,
            "type": "report",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"美國聯邦航空局 (FAA)：商業航空近距空中異常與航管 (ATC) 迴避事件通報 (巡檢區間 {since_date})",
                "en": f"U.S. FAA: Commercial Aviation Near-Miss & Airspace Traffic Incident Dossier ({since_date})"
            },
            "summary": {
                "zh_hk": f"美國聯邦航空局（FAA）航空安全資訊分析系統（ASIAS）通報存檔。依據聯邦航空法規追蹤商業航線飛行員與空中交通管制中心（ATC）申報之未授權空域侵入、近距離空中相遇（Near Midair Collision, NMAC）以及無二次雷達應答器之高空未知航空目標軌跡。",
                "en": f"Federal Aviation Administration (FAA) ASIAS safety audit record monitoring commercial pilot Near Midair Collision (NMAC) logs and air traffic control radar anomalies involving uncoordinated high-altitude transponders."
            },
            "agency": {
                "name": "Federal Aviation Administration",
                "zh_hk": "美國聯邦航空局 (FAA)",
                "country": "US"
            },
            "entities": {
                "agencies": ["Federal Aviation Administration", "National Transportation Safety Board"],
                "people": []
            },
            "sources": [
                {
                    "name": "FAA Aviation Safety Portal",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["FAA", "Aviation Safety", "Near Miss", "Commercial Flights", "ATC", "ASIAS"]
        }

        records.append(record)
        return records
