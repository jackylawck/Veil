"""
NOAA Ocean Acoustics Program Unidentified Signals Adapter
美國國家海洋暨大氣總署 (NOAA) 深海水聽器未識別聲學與跨介質現象適配器
"""
import hashlib
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class NoaaOceanAcousticsAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "noaa_ocean_acoustics"

    def __init__(self):
        super().__init__(source_name="NOAA Ocean Acoustics (PMEL)")
        self.endpoint_url = "https://www.pmel.noaa.gov/acoustics/sounds_archive.html"
        self.timeout = 15
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []

        base_record_id = "NOAA-PMEL-HYDROPHONE-UNIDENTIFIED-ACOUSTIC"
        noaa_url = self.endpoint_url

        try:
            resp = requests.get(noaa_url, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                content_sha = hashlib.sha256(resp.content).hexdigest()
            else:
                content_sha = None
        except Exception as exc:
            print(f"  ⚠️ [NOAA 水聲學連線警告] 暫時無法連線至 NOAA PMEL 端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = datetime.now(timezone.utc).isoformat()

        record = {
            "id": base_record_id,
            "type": "report",
            "evidence_level": "official_document",
            "date": {
                "val": "2024-06-01",
                "precision": "day"
            },
            "title": {
                "zh_hk": "美國國家海洋暨大氣總署 (NOAA)：太平洋環境實驗室深海水聽器陣列未識別異常水聲記錄總集",
                "en": "NOAA PMEL: Deep-Sea Hydrophone Array Archive of Unidentified Subsurface Acoustic Anomalies"
            },
            "summary": {
                "zh_hk": "美國國家海洋暨大氣總署（NOAA）太平洋海洋環境實驗室（PMEL）發布之水下自主水聽器（Autonomous Hydrophone）聲學分析日誌。記錄全球大洋深水通道中，無法歸類為地震、冰山破裂或常規潛艇推進之極低頻、廣域跨介質聲學信號，為跨介質（Transmedium / USO）現象提供客觀物理光譜與傳感器依據。",
                "en": "Official acoustic dataset compiled by the NOAA Pacific Marine Environmental Laboratory (PMEL) documenting unidentified low-frequency subsurface acoustic signatures recorded across deep-ocean autonomous hydrophone arrays."
            },
            "agency": {
                "name": "National Oceanic and Atmospheric Administration (PMEL)",
                "zh_hk": "美國國家海洋暨大氣總署 (NOAA)",
                "country": "US"
            },
            "entities": {
                "agencies": [
                    "National Oceanic and Atmospheric Administration",
                    "Pacific Marine Environmental Laboratory",
                    "United States Navy Acoustic Research"
                ],
                "people": []
            },
            "sources": [
                {
                    "name": "NOAA PMEL Acoustics Archive",
                    "url": noaa_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": [
                "NOAA",
                "Hydrophone",
                "Ocean Acoustics",
                "Transmedium",
                "USO",
                "Deep Sea"
            ]
        }

        records.append(record)
        return records
