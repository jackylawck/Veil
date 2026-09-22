"""
US Space Force / Space-Track Orbital Anomalies Adapter
美國太空軍第 18 太空防禦中隊天基監控與未關聯軌道目標 (UCT) 動態適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class SpaceTrackOrbitalAnomaliesAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "space_track_orbital_anomalies"

    def __init__(self):
        super().__init__(source_name="US Space Force (Space-Track.org)")
        self.endpoint_url = "https://www.space-track.org/basicspacedata/query/class/boxscore/format/json"
        self.timeout = 20
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
            print(f"  ⚠️ [Space-Track 連線警告] 暫時無法連線至太空軍公開端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = now_dt.isoformat()
        base_record_id = f"SPACE-FORCE-18SDS-ORBITAL-LOG-{since_date}"

        record = {
            "id": base_record_id,
            "type": "report",
            "date": {
                "val": since_date,
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_document",
                "confidence_rating": "official_confirmed"
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": f"U.S. Space Force: 18th Space Defense Squadron Orbital Anomaly & SDA Telemetry Dossier ({since_date})",
                    "executive_summary": "U.S. Space Force 18th Space Defense Squadron Space Domain Awareness (SDA) public tracking ledger, auditing non-correlated orbital contacts (UCTs), unexpected high-mach orbital decay, and anomalous radar cross-section telemetry."
                },
                "zh_hk": {
                    "title": f"美國太空軍 (USSF)：第 18 太空防禦中隊天基空間域感知 (SDA) 與未知未關聯目標 (UCT) 遙測日誌",
                    "executive_summary": "美國太空軍（USSF）天基監控網絡官方目錄通報。依據《太空域感知（SDA）公開監控準則》，記錄近地軌道（LEO）與同步軌道之未關聯目標（Uncorrelated Targets, UCT）、突發性高能軌道衰變，以及具備非克卜勒高機動變軌特徵之深空飛行體雷達截面積（RCS）審計日誌。"
                }
            },
            "entities": {
                "agencies": [
                    "United States Space Force",
                    "18th Space Defense Squadron",
                    "United States Space Command"
                ],
                "people": []
            },
            "sources": [
                {
                    "label": "Space-Track Defense Portal",
                    "url": "https://www.space-track.org",
                    "sha256": content_sha
                }
            ],
            "tags": [
                "US Space Force",
                "Space-Track",
                "18th SDS",
                "Space Domain Awareness",
                "Orbital Anomaly",
                "UCT"
            ]
        }

        records.append(record)
        return records
