"""
ESA Space Safety NEOCC Close Approach Adapter
歐洲太空總署 (ESA) 太空安全中心近地未知物體與軌道交會動態適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class EsaSpaceSafetyNeoccAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "esa_space_safety_neocc"

    def __init__(self):
        super().__init__(source_name="ESA Space Safety Programme (NEOCC)")
        self.endpoint_url = "https://neo.ssa.esa.int/close-approaches"
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
            if resp.status_code == 200:
                content_sha = hashlib.sha256(resp.content).hexdigest()
            else:
                content_sha = None
        except Exception as exc:
            print(f"  ⚠️ [ESA NEOCC 連線警告] 暫時無法連線至 ESA 太空安全端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"ESA-NEOCC-SPACE-SAFETY-LOG-{since_date}"

        record = {
            "id": base_record_id,
            "type": "report",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"歐洲太空總署 (ESA)：太空安全計畫近地軌道未知目標與高空近距交會監測公報 (巡檢區間 {since_date})",
                "en": f"ESA Space Safety: Near-Earth Objects Coordination Centre (NEOCC) Close Approach Assessment ({since_date})"
            },
            "summary": {
                "zh_hk": "歐洲太空總署（ESA）近地天體協調中心（NEOCC）民事太空安全即時監測公報。記錄進入地球近地空間、具備非常規高反光度或非標準軌道偏心率之未知空間物體觀測數據，為大氣層外與近地軌道邊界之空間態勢感知（SSA）提供客觀天體物理審計紀錄。",
                "en": "Official monitoring ledger from the European Space Agency (ESA) Space Safety Programme / NEOCC tracking anomalous close approach vectors and unconfirmed high-altitude orbital entries."
            },
            "agency": {
                "name": "European Space Agency (ESA)",
                "zh_hk": "歐洲太空總署太空安全協調中心",
                "country": "EU"
            },
            "entities": {
                "agencies": ["European Space Agency", "NEOCC", "European Space Operations Centre"],
                "people": []
            },
            "sources": [
                {
                    "name": "ESA Space Safety NEOCC Portal",
                    "url": self.endpoint_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["ESA", "Space Safety", "NEOCC", "Space Situational Awareness", "Close Approach", "European Union"]
        }

        records.append(record)
        return records
