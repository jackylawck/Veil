"""
Mexico SEDENA & FAM Air Force Aerial Anomaly Adapter
墨西哥國防部 (SEDENA) 與墨西哥空軍 (FAM) 軍用紅外空巡解密公報適配器
"""
import hashlib
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class MexicoSedenaFafAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "mexico_sedena_faf"

    def __init__(self):
        super().__init__(source_name="Secretariat of National Defense (SEDENA - Mexico)")
        self.endpoint_url = "https://www.gob.mx/defensa"
        self.timeout = 15
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []

        base_record_id = "MEXICO-SEDENA-FAM-FLIR-AIR-INTERCEPT"
        sedena_url = self.endpoint_url

        try:
            resp = requests.get(sedena_url, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                content_sha = hashlib.sha256(resp.content).hexdigest()
            else:
                content_sha = None
        except Exception as exc:
            print(f"  ⚠️ [墨西哥國防部連線警告] 暫時無法連線至 SEDENA 端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = datetime.now(timezone.utc).isoformat()

        record = {
            "id": base_record_id,
            "type": "foia",
            "evidence_level": "official_document",
            "date": {
                "val": "2004-05-11",
                "precision": "day"
            },
            "title": {
                "zh_hk": "墨西哥國防部 (SEDENA)：空軍第 501 空中巡邏中隊 FLIR 雙波段紅外追蹤解密案卷",
                "en": "Mexican Secretariat of National Defense (SEDENA): Air Force 501 Squadron FLIR Multi-Target Intercept Dossier"
            },
            "summary": {
                "zh_hk": "由墨西哥國防部長（Ricardo Vega García 將軍）正式批准解密之空軍官方作戰公報。記錄墨西哥空軍 C-26 Metroliner 偵察巡邏機於坎佩切州上空執行反毒巡航時，以 Star SAFIRE II 軍規 FLIR 紅外系統鎖定並追蹤 11 個肉眼不可見、高速伴飛之未知空中編隊，機載氣象雷達未檢測到常規應答機信號。",
                "en": "Official military intercept file declassified by SEDENA authorization, detailing the Mexican Air Force 501st Squadron reconnaissance aircraft tracking 11 infrared-only anomalous targets over Campeche using Star SAFIRE II thermal sensors."
            },
            "agency": {
                "name": "Secretaría de la Defensa Nacional (SEDENA)",
                "zh_hk": "墨西哥國防部 (SEDENA)",
                "country": "MX"
            },
            "entities": {
                "agencies": [
                    "Secretaría de la Defensa Nacional",
                    "Fuerza Aérea Mexicana",
                    "501 Escuadrón Aéreo"
                ],
                "people": [
                    "General Ricardo Vega García"
                ]
            },
            "sources": [
                {
                    "name": "Mexico SEDENA Official Government Portal",
                    "url": sedena_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": [
                "Mexico",
                "SEDENA",
                "Fuerza Aerea Mexicana",
                "FLIR",
                "Thermal Imaging",
                "Declassified"
            ]
        }

        records.append(record)
        return records
