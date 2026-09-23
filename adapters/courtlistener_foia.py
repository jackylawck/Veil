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

    @property
    def source_name(self) -> str:
        return "courtlistener_foia"

    def __init__(self):
        super().__init__()
        self.api_url = "https://www.courtlistener.com/api/rest/v4/dockets/"
        self.timeout = 20
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        
        since_date = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        params = {
            "q": 'UAP OR "All-domain Anomaly Resolution Office" OR "Unidentified Anomalous Phenomena"',
            "court": "dcd",
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
                    
                    payload_raw = f"{docket_id}_{case_name}_{date_filed}".encode("utf-8")
                    content_sha = hashlib.sha256(payload_raw).hexdigest()
                    
                    record = {
                        "id": f"COURT-FOIA-DOCKET-{docket_id}",
                        "type": "foia",
                        "date": {
                            "val": date_filed,
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
                                "title": f"U.S. Federal Court Docket: {case_name}",
                                "executive_summary": "Official U.S. Federal District Court civil proceeding regarding FOIA statutory disclosure claims against defense or intelligence agencies seeking unredacted records."
                            },
                            "zh_hk": {
                                "title": f"美國聯邦法院訴訟卷宗：{case_name}",
                                "executive_summary": "美國聯邦地區法院受理事涉不明異常現象（UAP）之《資訊自由法》（FOIA）強制解密訴訟。原告要求聯邦法官下令國防部或情報界公佈機密清單（Vaughn Index）並檢驗行政機關濫用豁免權情事。"
                            }
                        },
                        "entities": {
                            "agencies": ["United States District Court", "Department of Defense", "Department of Justice"],
                            "people": []
                        },
                        "sources": [
                            {
                                "label": "CourtListener Judicial Database",
                                "url": docket_url,
                                "sha256": content_sha
                            }
                        ],
                        "tags": ["FOIA", "Federal Court", "CourtListener", "Judicial Discovery", "Legal Action"]
                    }
                    records.append(record)

        except Exception as exc:
            print(f"  ⚠️ [CourtListener API 警告] 動態調用司法 API 異常: {exc}", file=sys.stderr)

        return records
