"""
Sweden Military Defence Archives (Krigsarkivet / Ghost Rockets) Adapter
瑞典國防軍軍事情報局 (MUST) 與國防檔案館 (Krigsarkivet) 解密公報適配器
"""
import hashlib
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class SwedenUfoSverigeAfiseAdapter(BaseAdapter):

    @property
    def source_name(self) -> str:
        return "sweden_ufo_sverige_afise"

    def __init__(self):
        super().__init__()
        self.endpoint_url = "https://riksarkivet.se/krigsarkivet"
        self.timeout = 15
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []

        base_record_id = "SWEDEN-MUST-KRIGSARKIVET-GHOST-ROCKETS-ARCHIVE"
        archive_url = self.endpoint_url

        try:
            resp = requests.get(archive_url, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                content_sha = hashlib.sha256(resp.content).hexdigest()
            else:
                content_sha = None
        except Exception as exc:
            print(f"  ⚠️ [瑞典國防檔案館連線警告] 暫時無法連線至 Krigsarkivet 端點: {exc}", file=sys.stderr)
            content_sha = None

        now_iso = datetime.now(timezone.utc).isoformat()

        record = {
            "id": base_record_id,
            "type": "foia",
            "evidence_level": "official_document",
            "date": {
                "val": "2023-09-01",
                "precision": "day"
            },
            "title": {
                "zh_hk": "瑞典國防軍與國家檔案館 (Krigsarkivet)：國防參謀部「幽靈火箭」與波羅的海空域異常軍事解密總卷",
                "en": "Swedish Armed Forces & National Archives (Krigsarkivet): Military Declassified Dossiers on Baltic Airspace Anomalies"
            },
            "summary": {
                "zh_hk": "瑞典國家國防檔案館（Krigsarkivet）依據解密指令移交之瑞典國防軍參謀部與軍事情報安全局（MUST）專題軍事公報。收錄 1946 年「幽靈火箭」跨國雷達觀測記錄、皇家瑞典空軍戰備雷達跟蹤、多處深水湖泊打撈打撈報告，以及冷戰至今波羅的海防禦空域之異常航空遙測原始檔案。",
                "en": "Official declassified defense dossiers transferred from the Swedish Armed Forces to the Military Archives (Krigsarkivet), documenting Baltic airspace radar intercepts, defense intelligence (MUST) assessments, and historical lake search operations."
            },
            "agency": {
                "name": "Swedish Armed Forces (Försvarsmakten) / Krigsarkivet",
                "zh_hk": "瑞典國防軍／瑞典軍事檔案館",
                "country": "SE"
            },
            "entities": {
                "agencies": [
                    "Försvarsmakten",
                    "Krigsarkivet",
                    "Militära underrättelse- och säkerhetstjänsten (MUST)"
                ],
                "people": []
            },
            "sources": [
                {
                    "name": "Swedish National Military Archives Portal",
                    "url": archive_url,
                    "format": "html",
                    "sha256": content_sha,
                    "sha256_verified": False,
                    "archived_at": now_iso
                }
            ],
            "tags": [
                "Sweden",
                "Forsvarsmakten",
                "Krigsarkivet",
                "MUST",
                "Ghost Rockets",
                "Baltic Sea",
                "NATO Ally"
            ]
        }

        records.append(record)
        return records
