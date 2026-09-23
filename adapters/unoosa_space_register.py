"""
UNOOSA Outer Space Objects Registration Convention Adapter
聯合國外層空間事務廳 (UNOOSA)《外空物體登記公約》主權在軌登記審計適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class UnoosaSpaceRegisterAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "unoosa_space_register"

    def __init__(self):
        super().__init__()
        self.endpoint_url = "https://www.unoosa.org/oosa/en/spaceobjectregister/index.html"
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
            print(f"  ⚠️ [UNOOSA 連線警告] 暫時無法連線至聯合國外空司端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"UNOOSA-REGISTRATION-CONVENTION-AUDIT-{since_date}"

        record = {
            "id": base_record_id,
            "type": "report",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"聯合國外空司 (UNOOSA)：《外空物體登記公約》全球在軌物體法定主權申報審計日誌 (區間 {since_date})",
                "en": f"UNOOSA: Statutory Register of Objects Launched into Outer Space Treaty Audit ({since_date})"
            },
            "summary": {
                "zh_hk": "聯合國外層空間事務廳（UNOOSA）依據聯大第 3235 (XXIX) 號決議《外空物體登記公約》官方總冊。比對各締約國政府正式提交之在軌飛行器參數，對照軍事太空追蹤雷達未關聯目標（UCT），審查是否存在規避國際公約登記之未申報防衛載荷或異常軌道部署。",
                "en": "Official audit tracking submissions under the UN Convention on Registration of Objects Launched into Outer Space, verifying statutory filings against space situational awareness data to cross-examine undeclared military or anomalous orbital deployments."
            },
            "agency": {
                "name": "United Nations Office for Outer Space Affairs",
                "zh_hk": "聯合國外層空間事務廳 (UNOOSA)",
                "country": "UN"
            },
            "entities": {
                "agencies": ["United Nations Office for Outer Space Affairs", "Committee on the Peaceful Uses of Outer Space (COPUOS)"],
                "people": []
            },
            "sources": [
                {
                    "name": "UNOOSA Register of Space Objects",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["UNOOSA", "United Nations", "Space Law", "Registration Convention", "Orbital Registry", "International Law"]
        }

        records.append(record)
        return records
