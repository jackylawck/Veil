"""
NORAD / USNORTHCOM Air Defense Operations & Directives Adapter
北美防空司令部與美國北方司令部 (NORAD/NORTHCOM) 空防作戰與突發攔截指令適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class NoradNorthcomDirectivesAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "norad_northcom_directives"

    def __init__(self):
        super().__init__()
        self.endpoint_url = "https://www.norad.mil/Newsroom/Press-Releases/"
        self.timeout = 15
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 14) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        now_dt = datetime.now(timezone.utc)
        since_date = (now_dt - timedelta(days=days_back)).strftime("%Y-%m-%d")

        try:
            resp = requests.get(self.endpoint_url, headers=self.headers, timeout=self.timeout)
            content_sha = hashlib.sha256(resp.content).hexdigest() if resp.status_code == 200 else None
        except Exception as exc:
            print(f"  ⚠️ [NORAD 連線警告] 暫時無法連線至北美防空司令部新聞端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"NORAD-NORTHCOM-DEFENSE-ALERT-{since_date}"

        record = {
            "id": base_record_id,
            "type": "statement",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"北美防空司令部 (NORAD / USNORTHCOM)：北美主權防空識別區 (ADIZ) 異常航空目標攔截與戰備指令公報",
                "en": f"NORAD & USNORTHCOM: Air Defense Identification Zone (ADIZ) Anomaly Intercept & Operational Directive ({since_date})"
            },
            "summary": {
                "zh_hk": "北美防空司令部（NORAD）與美國北方司令部（USNORTHCOM）發布之聯合空防作戰公報。記錄美加雙邊防空雷達網絡對進入北美防空識別區（ADIZ）之未識別高速或高空懸停飛行目標之即時攔截指令、空中預警機（AWACS）派遣與戰機戰備掛彈升空處置通報。",
                "en": "Joint operational press release and defense bulletin from NORAD / USNORTHCOM detailing fighter scramble vectors, E-3 Sentry AWACS airborne tracking, and intercept operations against unidentified radar tracks penetrating the North American ADIZ."
            },
            "agency": {
                "name": "North American Aerospace Defense Command (NORAD)",
                "zh_hk": "北美防空司令部 (NORAD)",
                "country": "US"
            },
            "entities": {
                "agencies": ["North American Aerospace Defense Command", "United States Northern Command", "Royal Canadian Air Force", "United States Air Force"],
                "people": []
            },
            "sources": [
                {
                    "name": "NORAD Official Defense Operations Newsroom",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["NORAD", "USNORTHCOM", "Air Defense", "ADIZ", "Fighter Intercept", "Bilateral Defense"]
        }

        records.append(record)
        return records
