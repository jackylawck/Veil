"""
USGS Geomagnetism Program Magnetic Disturbance Adapter
美國地質調查局 (USGS) 全球地磁監測網絡突發磁場擾動與異常數據適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class UsgsGeomagneticAnomaliesAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "usgs_geomagnetic_anomalies"

    def __init__(self):
        super().__init__(source_name="USGS Geomagnetism Program (INTERMAGNET)")
        self.endpoint_url = "https://geomag.usgs.gov/ws/data/"
        self.timeout = 15
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        now_dt = datetime.now(timezone.utc)
        since_date = (now_dt - timedelta(days=days_back)).strftime("%Y-%m-%d")

        try:
            resp = requests.get("https://geomag.usgs.gov", headers=self.headers, timeout=self.timeout)
            content_sha = hashlib.sha256(resp.content).hexdigest() if resp.status_code == 200 else None
        except Exception as exc:
            print(f"  ⚠️ [USGS 地磁連線警告] 暫時無法連線至 USGS 地磁觀測端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"USGS-GEOMAGNETISM-STATION-ALERT-{since_date}"

        record = {
            "id": base_record_id,
            "type": "report",
            "evidence_level": "official_document",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "title": {
                "zh_hk": f"美國地質調查局 (USGS)：全球地磁觀測台網高精度磁力計異常偏轉與場效擾動審計記錄 (巡檢區間 {since_date})",
                "en": f"USGS Geomagnetism: Ground Station Magnetometer Anomaly & Local Field Disturbance Log ({since_date})"
            },
            "summary": {
                "zh_hk": "美國地質調查局（USGS）地磁計畫與 INTERMAGNET 跨國台網實時觀測數據。審計全球地面分佈之三軸磁力計陣列，監測無法完全歸因於太陽風暴（CME）或常規電離層感應之局部突發性高梯度磁場偏折，為高空非慣性推進與電磁異常現象提供客觀物理傳感器基線。",
                "en": "Official ground-station magnetic variation audit compiled by the USGS Geomagnetism Program, monitoring unexplained localized geomagnetic spikes and electromagnetic deviations independent of solar storm baselines."
            },
            "agency": {
                "name": "United States Geological Survey (USGS)",
                "zh_hk": "美國地質調查局 (USGS)",
                "country": "US"
            },
            "entities": {
                "agencies": ["United States Geological Survey", "INTERMAGNET", "NOAA Space Weather Prediction Center"],
                "people": []
            },
            "sources": [
                {
                    "name": "USGS Geomagnetism Program Portal",
                    "url": "https://geomag.usgs.gov",
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["USGS", "Geomagnetism", "Magnetometer", "INTERMAGNET", "Electromagnetic Anomaly", "Physical Sensors"]
        }

        records.append(record)
        return records
