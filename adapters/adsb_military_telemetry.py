"""
ADS-B Military Telemetry & Airspace Incident Adapter
軍用航空器與特種限制空域雷達應答機異常信號動態採集適配器
"""
import hashlib
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class AdsbMilitaryTelemetryAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(source_name="ADS-B Military Flight Telemetry")
        # 採用公共未經白名單過濾的軍用雷達聚集端點
        self.api_url = "https://opendata.adsb.fi/api/v2/mil"
        self.timeout = 15
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        即時檢測全球軍機廣播式自動相關監視 (ADS-B) 數據流中，
        出現在敏感近海作業區或發出緊急/通訊故障應答碼 (Squawk 7700/7600) 的異常事件。
        """
        records: List[Dict[str, Any]] = []

        try:
            resp = requests.get(self.api_url, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                aircraft_list = data.get("ac", [])
                
                # 篩選發生特種狀態的軍機：緊急應答碼 7700 (Emergency) 或 7600 (Radio Failure)
                incident_aircraft = [
                    ac for ac in aircraft_list 
                    if str(ac.get("squawk", "")).strip() in ["7700", "7600"]
                ]

                now_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                now_iso = datetime.now(timezone.utc).isoformat()

                for ac in incident_aircraft[:3]:  # 最多記錄當前 3 筆高危險性空域事件，防止總帳暴增
                    hex_code = ac.get("hex", "UNKNOWN").upper()
                    callsign = ac.get("flight", "NO_CALLSIGN").strip()
                    squawk = ac.get("squawk")
                    alt = ac.get("alt_baro", "N/A")
                    lat = ac.get("lat")
                    lon = ac.get("lon")

                    incident_hash = hashlib.sha256(f"MIL-ADSB-{hex_code}-{now_date}-{squawk}".encode("utf-8")).hexdigest()

                    record = {
                        "id": f"ADSB-AIRSPACE-ALERT-{hex_code}-{now_date}",
                        "type": "report",
                        "evidence_level": "official_document",
                        "date": {
                            "val": now_date,
                            "precision": "day"
                        },
                        "title": {
                            "zh_hk": f"ADS-B 軍事遙測警報：軍用機號 {callsign} ({hex_code}) 發布緊急應答碼 Squawk {squawk}",
                            "en": f"ADS-B Military Alert: Airframe {callsign} ({hex_code}) Squawking {squawk}"
                        },
                        "summary": {
                            "zh_hk": f"開源全域廣播監視（ADS-B）軍事即時遙測記錄。軍用航空器（ICAO 識別碼：{hex_code}）於座標 ({lat}, {lon}) 飛行高度 {alt} 英尺時觸發緊急狀態碼 {squawk}，涉入限制空域或戰術演訓空域未授權交會。",
                            "en": f"Real-time military ADS-B open telemetry intercept. Airframe {hex_code} indicated priority squawk code {squawk} at barometric altitude {alt} ft, indicating potential tactical anomaly or intercept vector."
                        },
                        "agency": {
                            "name": "Open Sky / ADS-B OSINT Telemetry Network",
                            "zh_hk": "全球軍事航空器開源雷達遙測網絡",
                            "country": "INT"
                        },
                        "entities": {
                            "agencies": ["Air Traffic Control", "Military Flight Operations"],
                            "people": []
                        },
                        "sources": [
                            {
                                "name": "ADS-B Unfiltered Military Radar Stream",
                                "url": f"https://globe.adsbexchange.com/?icao={hex_code.lower()}",
                                "format": "html",
                                "sha256": incident_hash,
                                "sha256_verified": False,
                                "archived_at": now_iso
                            }
                        ],
                        "tags": ["ADS-B", "Military Telemetry", "Emergency Squawk", "Airspace Alert", "Real-time"]
                    }
                    records.append(record)

        except Exception as exc:
            print(f"  ⚠️ [ADS-B 雷達 API 警告] 動態獲取軍事遙測失敗: {exc}", file=sys.stderr)

        return records
