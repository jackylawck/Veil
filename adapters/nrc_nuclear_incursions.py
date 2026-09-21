"""
NRC Nuclear Facilities Airspace Incursions Adapter
美國核能管理委員會 (NRC) 核設施未授權空中侵入與異常事件動態適配器
"""
import hashlib
import re
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class NrcNuclearIncursionsAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(source_name="U.S. Nuclear Regulatory Commission (NRC Events)")
        # NRC 每日官方公開事件通報日誌端點
        self.base_url = "https://www.nrc.gov/reading-rm/doc-collections/event-status/event/"
        self.timeout = 20
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """
        動態掃描 NRC 近日核能設施安全通報日誌，
        自動檢索未授權無人機、未知航空器侵入核安全禁區之法定呈報案卷。
        """
        records: List[Dict[str, Any]] = []
        now_dt = datetime.now(timezone.utc)

        # 檢查最近幾天的事件通報日誌
        for day_offset in range(min(days_back, 5)):
            target_date = now_dt - timedelta(days=day_offset)
            # NRC 日誌命名格式通常為 /YYYY/YYYYMMDDen.html
            year_str = target_date.strftime("%Y")
            date_str = target_date.strftime("%Y%m%d")
            log_url = f"{self.base_url}{year_str}/{date_str}en.html"

            try:
                resp = requests.get(log_url, headers=self.headers, timeout=self.timeout)
                if resp.status_code != 200:
                    continue

                content_text = resp.text
                content_lower = content_text.lower()

                # 關鍵字檢索：無人機侵入、未知空中飛行體、空域侵犯
                keywords = ["drone", "unauthorized aircraft", "airspace incursion", "unidentified flying", "uap"]
                matched_keywords = [kw for kw in keywords if kw in content_lower]

                if matched_keywords:
                    event_sha = hashlib.sha256(resp.content).hexdigest()
                    date_iso = target_date.strftime("%Y-%m-%d")
                    now_iso = now_dt.isoformat()

                    record = {
                        "id": f"NRC-NUCLEAR-AIRSPACE-ALERT-{date_str}",
                        "type": "report",
                        "evidence_level": "official_document",
                        "date": {
                            "val": date_iso,
                            "precision": "day"
                        },
                        "title": {
                            "zh_hk": f"美國核能管理委員會 (NRC)：戰略核設施空域異常與未授權飛行物通報 (日誌 {date_iso})",
                            "en": f"U.S. NRC: Nuclear Facility Airspace Security & Aerial Incursion Report ({date_iso})"
                        },
                        "summary": {
                            "zh_hk": f"依據美國聯邦法規 10 CFR 50.72，核設施營運商於今日通報日誌中正式登錄空域安全警戒事件。檢測到關鍵詞【{', '.join(matched_keywords)}】，涉及核反應爐或核廢料儲存設施周邊限制空域之未經授權飛行活動。",
                            "en": f"Official U.S. Nuclear Regulatory Commission (NRC) daily event notification log identifying security reporting triggers [{', '.join(matched_keywords)}] over licensed nuclear facilities pursuant to 10 CFR 50.72."
                        },
                        "agency": {
                            "name": "Nuclear Regulatory Commission",
                            "zh_hk": "美國核能管理委員會 (NRC)",
                            "country": "US"
                        },
                        "entities": {
                            "agencies": ["Nuclear Regulatory Commission", "Federal Bureau of Investigation", "Federal Aviation Administration"],
                            "people": []
                        },
                        "sources": [
                            {
                                "name": "NRC Daily Event Status Reports",
                                "url": log_url,
                                "format": "html",
                                "sha256": event_sha,
                                "sha256_verified": False,
                                "archived_at": now_iso
                            }
                        ],
                        "tags": ["NRC", "Nuclear Security", "Airspace Incursion", "Critical Infrastructure", "10 CFR 50.72"]
                    }
                    records.append(record)

            except Exception as exc:
                print(f"  ⚠️ [NRC 通報掃描警告] 檢查 {log_url} 異常: {exc}", file=sys.stderr)

        return records
