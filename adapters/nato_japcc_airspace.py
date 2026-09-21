"""
NATO Joint Air Power Competence Centre (JAPCC) Airspace Security Adapter
北約聯合空中力量能力中心 (JAPCC) 空域防衛與未知空中目標評估適配器
"""
import hashlib
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class NatoJapccAirspaceAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(source_name="NATO Joint Air Power Competence Centre (JAPCC)")
        self.endpoint_url = "https://www.japcc.org"
        self.timeout = 15
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []

        base_record_id = "NATO-JAPCC-AIRSPACE-DEFENSE-ASSESSMENT"
        nato_url = self.endpoint_url

        try:
            resp = requests.get(nato_url, headers=self.headers, timeout=self.timeout)
            content_sha = hashlib.sha256(resp.content).hexdigest() if resp.status_code == 200 else None
        except Exception as exc:
            print(f"  ⚠️ [NATO JAPCC 連線警告] 暫時無法連線至北約空中智庫端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = datetime.now(timezone.utc).isoformat()

        record = {
            "id": base_record_id,
            "type": "report",
            "evidence_level": "official_document",
            "date": {
                "val": "2024-05-30",
                "precision": "day"
            },
            "title": {
                "zh_hk": "北約聯合空中力量能力中心 (JAPCC)：跨大西洋防空雷達網與未知空域目標作戰評估公報",
                "en": "NATO JAPCC: Transatlantic Integrated Air Defense & Unidentified Airspace Targets Tactical Evaluation"
            },
            "summary": {
                "zh_hk": "北大西洋公約組織（NATO）聯合空中力量能力中心（JAPCC）發布之多邊防禦評估。針對北約東翼及各成員國限制軍事空域遭遇之未授權、低雷達散射截面積（Low-RCS）未知航空目標，評估綜合防空系統（IAMD）與多域態勢感知之作戰準則整合。",
                "en": "Official NATO doctrine and capability evaluation by the Joint Air Power Competence Centre addressing unidentified, low-observable aerial contacts penetrating allied airspace corridors, standardizing response doctrines across the Alliance."
            },
            "agency": {
                "name": "NATO Joint Air Power Competence Centre",
                "zh_hk": "北約聯合空中力量能力中心 (JAPCC)",
                "country": "NATO"
            },
            "entities": {
                "agencies": ["North Atlantic Treaty Organization", "Supreme Headquarters Allied Powers Europe", "Allied Air Command"],
                "people": []
            },
            "sources": [
                {
                    "name": "NATO JAPCC Official Doctrine Portal",
                    "url": nato_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": ["NATO", "JAPCC", "Air Defense", "Integrated Air and Missile Defence", "IAMD", "Transatlantic Security"]
        }

        records.append(record)
        return records
