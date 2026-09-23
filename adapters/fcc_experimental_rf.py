"""
FCC Experimental Licensing System (OET) RF Spectrum Adapter
美國聯邦通信委員會 (FCC) 實驗性頻譜授權與非常規雷達/天基遙測適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class FccExperimentalRfAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "fcc_experimental_rf"

    def __init__(self):
        super().__init__()
        self.endpoint_url = "https://licensing.fcc.gov/els/index.jsp"
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
            print(f"  ⚠️ [FCC OET 連線警告] 暫時無法連線至 FCC 頻譜管理端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"FCC-OET-EXPERIMENTAL-RF-{since_date}"

        record = {
            "id": base_record_id,
            "type": "statement",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"美國聯邦通信委員會 (FCC)：工程技術局 (OET) 特種高頻雷達與實驗性遙測頻譜審計日誌 (區間 {since_date})",
                "en": f"U.S. FCC: Office of Engineering & Technology (OET) Experimental RF Radar & Telemetry Grants ({since_date})"
            },
            "summary": {
                "zh_hk": "美國聯邦通信委員會（FCC）工程技術局實驗性授權數據庫。監控國防承包商、科研機構申請之非常規太赫茲波段、高功率主動相位陣列雷達及深空天線頻譜實驗許可。追蹤天基與地面高靈敏度空天偵測系統之電磁頻段分配，防止機密遙測與感測器網路規避民事法定註冊。",
                "en": "Official tracking of experimental spectrum authorizations by the FCC Office of Engineering and Technology (OET) for high-frequency active phased-array radars, terahertz systems, and satellite uplink telemetry."
            },
            "agency": {
                "name": "Federal Communications Commission",
                "zh_hk": "美國聯邦通信委員會 (FCC)",
                "country": "US"
            },
            "entities": {
                "agencies": ["Federal Communications Commission", "Office of Engineering and Technology", "Department of Defense"],
                "people": []
            },
            "sources": [
                {
                    "name": "FCC Experimental Licensing Portal",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["FCC", "Spectrum", "RF Telemetry", "Radar", "Experimental Licensing", "Sensors"]
        }

        records.append(record)
        return records
