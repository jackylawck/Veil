"""
CourtListener Federal FOIA Litigation Adapter
美國聯邦地區法院 FOIA 解密訴訟即時案件追蹤適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class CourtListenerFoiaAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(source_name="CourtListener Federal FOIA Docket")
        self.api_url = "https://www.courtlistener.com/api/rest/v4/dockets/"
        self.timeout = 20
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        動態查詢美國哥倫比亞特區 (D.D.C.) 等聯邦法院中，
        控告 DoD/CIA/AARO 違反 FOIA 之最新訴訟卷宗與司法傳票裁決。
        """
        records: List[Dict[str, Any]] = []
        
        # 動態計算回溯日期
        since_date = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        # 檢索關鍵字：UAP, AARO, "Unidentified Anomalous Phenomena"
        params = {
            "q": 'UAP OR "All-domain Anomaly Resolution Office" OR "Unidentified Anomalous Phenomena"',
            "court": "dcd",  # 主要鎖定 Washington D.C. 聯邦地區法院
            "filed_after": since_date,
            "order_by": "date_filed desc",
            "format": "json"
        }

        try:
            resp = requests.get(self.api_url, params=params, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                
                for item in results:
                    docket_id = item.get("id")
                    case_name = item.get("case_name") or "Federal FOIA Litigation Docket"
                    date_filed = item.get("date_filed") or datetime.now(timezone.utc).strftime("%Y-%m-%d")
                    docket_url = f"https://www.courtlistener.com{item.get('absolute_url')}" if item.get("absolute_url") else self.api_url
                    
                    # 計算該卷宗結構的特徵 SHA-256
                    payload_raw = f"{docket_id}_{case_name}_{date_filed}".encode("utf-8")
                    content_sha = hashlib.sha256(payload_raw).hexdigest()
                    now_iso = datetime.now(timezone.utc).isoformat()
                    
                    record = {
                        "id": f"COURT-FOIA-DOCKET-{docket_id}",
                        "type": "foia",
                        "evidence_level": "official_document",
                        "date": {
                            "val": date_filed,
                            "precision": "day"
                        },
                        "title": {
                            "zh_hk": f"美國聯邦法院訴訟卷宗：{case_name}",
                            "en": f"U.S. Federal Court Docket: {case_name}"
                        },
                        "summary": {
                            "zh_hk": f"美國聯邦地區法院受理事涉不明異常現象（UAP）之《資訊自由法》（FOIA）強制解密訴訟。原告要求聯邦法官下令國防部或情報界公佈機密清單（Vaughn Index）並檢驗行政機關濫用豁免權情事。",
                            "en": f"Official U.S. Federal District Court civil proceeding regarding FOIA statutory disclosure claims against defense or intelligence agencies seeking unredacted records."
                        },
                        "agency": {
                            "name": "United States District Court",
                            "zh_hk": "美國聯邦地區法院",
                            "country": "US"
                        },
                        "entities": {
                            "agencies": ["United States District Court", "Department of Defense", "Department of Justice"],
                            "people": []
                        },
                        "sources": [
                            {
                                "name": "CourtListener Judicial Database",
                                "url": docket_url,
                                "format": "html",
                                "sha256": content_sha,
                                "sha256_verified": False,
                                "archived_at": now_iso
                            }
                        ],
                        "tags": ["FOIA", "Federal Court", "CourtListener", "Judicial Discovery", "Legal Action"]
                    }
                    records.append(record)

        except Exception as exc:
            print(f"  ⚠️ [CourtListener API 警告] 動態調用司法 API 異常: {exc}", file=sys.stderr)

        return records
