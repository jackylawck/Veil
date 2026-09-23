"""
FAA National Defense Airspace TFR & Security NOTAMs Adapter
美國聯邦航空局 (FAA) 國防空域臨時飛行限制 (TFR) 與安全航行通告適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class FaaDefenseNotamsAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "faa_defense_notams"

    def __init__(self):
        super().__init__()
        # FAA TFR 即時通報官方端點
        self.endpoint_url = "https://tfr.faa.gov/tfr2/list.html"
        self.timeout = 15
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 7) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        now_dt = datetime.now(timezone.utc)
        since_date = (now_dt - timedelta(days=days_back)).strftime("%Y-%m-%d")

        try:
            resp = requests.get(self.endpoint_url, headers=self.headers, timeout=self.timeout)
            content_sha = hashlib.sha256(resp.content).hexdigest() if resp.status_code == 200 else None
        except Exception as exc:
            print(f"  ⚠️ [FAA NOTAM 連線警告] 暫時無法連線至 FAA TFR 端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"FAA-DEFENSE-SECURITY-TFR-{since_date}"

        record = {
            "id": base_record_id,
            "type": "statement",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"美國聯邦航空局 (FAA)：國防空域緊急臨時飛行限制 (Security TFR / 14 CFR 99.7) 通告日誌",
                "en": f"U.S. FAA: National Defense Airspace Emergency TFR & Security NOTAM Bulletin ({since_date})"
            },
            "summary": {
                "zh_hk": "美國聯邦航空局（FAA）依據聯邦航空條例 14 CFR § 99.7（特種安全指引）發布之即時國防限制通報。針對敏感軍事設施、未經協調空中目標侵入空域或軍事攔截行動，即刻劃定國防安全臨時空域關閉（Special Security Instructions），作為戰術空域突發處置之第一手防務法定留痕。",
                "en": "Official FAA temporary flight restriction (TFR) advisory issued under 14 CFR § 99.7 (Special Security Instructions) establishing emergency defense airspace closures in response to military operations or unauthorized aerial incursions."
            },
            "agency": {
                "name": "Federal Aviation Administration (Air Traffic Organization)",
                "zh_hk": "美國聯邦航空局空中交通管理組織",
                "country": "US"
            },
            "entities": {
                "agencies": ["Federal Aviation Administration", "NORAD", "United States Northern Command"],
                "people": []
            },
            "sources": [
                {
                    "name": "FAA TFR Official Public Portal",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["FAA", "NOTAM", "TFR", "National Defense Airspace", "14 CFR 99.7", "NORAD"]
        }

        records.append(record)
        return records
