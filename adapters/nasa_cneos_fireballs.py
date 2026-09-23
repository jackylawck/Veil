"""
NASA JPL CNEOS Fireball and Atmospheric Impact Adapter
美國國家航空暨太空總署 (NASA) JPL 近地天體研究中心大氣撞擊與高能光學遙測適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class NasaCneosFireballsAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "nasa_cneos_fireballs"

    def __init__(self):
        super().__init__()
        # NASA JPL 官方大氣高能碰撞即時 API 端點
        self.api_url = "https://ssd-api.jpl.nasa.gov/fireball.api"
        self.timeout = 20
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        now_dt = datetime.now(timezone.utc)
        since_date = (now_dt - timedelta(days=days_back)).strftime("%Y-%m-%d")

        params = {
            "date-min": since_date,
            "req-loc": "true",
            "limit": 2
        }

        try:
            resp = requests.get(self.api_url, params=params, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                raw_records = data.get("data", [])
                fields = data.get("fields", [])

                for item in raw_records:
                    # 依據 fields 結構解析：date, energy, impact-e, lat, lat-dir, lon, lon-dir, alt, vel
                    record_dict = dict(zip(fields, item))
                    impact_date = record_dict.get("date", since_date).split()[0]
                    vel = record_dict.get("vel", "N/A")
                    alt = record_dict.get("alt", "N/A")
                    energy = record_dict.get("energy", "N/A")
                    lat = f"{record_dict.get('lat')}{record_dict.get('lat-dir', '')}"
                    lon = f"{record_dict.get('lon')}{record_dict.get('lon-dir', '')}"

                    impact_hash = hashlib.sha256(f"NASA-CNEOS-{impact_date}-{lat}-{lon}".encode("utf-8")).hexdigest()
                    now_iso = now_dt.isoformat()

                    record = {
                        "id": f"NASA-CNEOS-BOLIDE-{impact_date}-{lat.replace('.', '_')}",
                        "type": "report",
                        "evidence_level": "official_document",
                        "date": {
                            "val": impact_date,
                            "precision": "day"
                        },
                        "title": {
                            "zh_hk": f"NASA JPL (CNEOS)：高空大氣高能光學與紅外碰撞遙測記錄 (坐標 {lat}, {lon})",
                            "en": f"NASA JPL CNEOS: High-Energy Atmospheric Impact Optical/IR Telemetry ({impact_date})"
                        },
                        "summary": {
                            "zh_hk": f"美國國家航空暨太空總署（NASA）近地天體研究中心（CNEOS）官方解密數據流。由美國政府防空預警衛星感測器（如 SBIRS）在大氣頂層檢測到高空撞擊事件。紀錄飛行速度 {vel} km/s、爆炸高度 {alt} km、輻射總能量 {energy} GigaJoules，為大氣層高速切入物體提供客觀物理光度與速度向量存證。",
                            "en": "Official atmospheric entry event recorded by NASA JPL CNEOS utilizing declassified U.S. government sensor data, detailing trajectory velocity of {vel} km/s and energy radiation across upper atmosphere coordinates."
                        },
                        "agency": {
                            "name": "NASA Jet Propulsion Laboratory (CNEOS)",
                            "zh_hk": "美國國家航空暨太空總署噴射推進實驗室",
                            "country": "US"
                        },
                        "entities": {
                            "agencies": ["National Aeronautics and Space Administration", "Jet Propulsion Laboratory", "United States Space Command"],
                            "people": []
                        },
                        "sources": [
                            {
                                "name": "NASA JPL CNEOS Official Database",
                                "url": "https://cneos.jpl.nasa.gov/fireballs/",
                                "format": "html",
                                "sha256": impact_hash,
                                "sha256_verified": False,
                                "archived_at": now_iso
                            }
                        ],
                        "tags": ["NASA", "JPL", "CNEOS", "Atmospheric Entry", "Sensors", "Satellite IR", "High Mach"]
                    }
                    records.append(record)

        except Exception as exc:
            print(f"  ⚠️ [NASA CNEOS 連線警告] 暫時無法調用 NASA 火球 API: {exc}", file=sys.stderr)

        return records
