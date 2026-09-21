"""
DOE OSTI National Laboratories Research Adapter
美國能源部科學與技術資訊辦公室 (OSTI) 國家實驗室先進材料與同位素研究適配器
"""
import hashlib
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import requests

from adapters.base import BaseAdapter


class DoeOstiMaterialsAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(source_name="DOE Office of Scientific and Technical Information (OSTI)")
        self.api_url = "https://www.osti.gov/api/v1/records"
        self.timeout = 20
        self.headers = {
            "User-Agent": "TheVeil-OSINT-Ledger/2.0 (+https://jackylawck.github.io/veil/)",
            "Accept": "application/json"
        }

    def fetch_records(self, days_back: int = 30) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        now_dt = datetime.now(timezone.utc)
        since_date = (now_dt - timedelta(days=days_back)).strftime("%m/%d/%Y")

        # 檢索條件：搜尋 Los Alamos, Sandia, Oak Ridge 關於同位素比率、超材料與非常規等離子體的解密技術報告
        params = {
            "keywords": '"metamaterial" OR "anomalous isotopic" OR "unconventional propulsion" OR "terahertz radiation"',
            "publication_date_start": since_date,
            "rows": 2
        }

        try:
            resp = requests.get(self.api_url, params=params, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                results = data if isinstance(data, list) else data.get("records", [])

                for doc in results[:2]:
                    osti_id = doc.get("osti_id", "UNKNOWN")
                    title = doc.get("title", "DOE National Laboratory Research Record")
                    pub_date = doc.get("publication_date", now_dt.strftime("%Y-%m-%d"))
                    abstract = doc.get("description") or "Technical research paper published across U.S. National Laboratories."
                    lab_name = doc.get("research_org") or "DOE National Laboratory"

                    report_hash = hashlib.sha256(f"OSTI-{osti_id}-{pub_date}".encode("utf-8")).hexdigest()
                    now_iso = now_dt.isoformat()

                    record = {
                        "id": f"DOE-OSTI-TECH-REPORT-{osti_id}",
                        "type": "report",
                        "evidence_level": "official_document",
                        "date": {
                            "val": pub_date,
                            "precision": "day"
                        },
                        "title": {
                            "zh_hk": f"美國能源部國家實驗室 ({lab_name})：先進材料與同位素光譜技術報告 (OSTI ID: {osti_id})",
                            "en": f"U.S. DOE National Labs ({lab_name}): Advanced Materials & Isotopic Technical Report ({osti_id})"
                        },
                        "summary": {
                            "zh_hk": f"美國能源部國家實驗室（含 LANL、Sandia、ORNL）經由 OSTI 官方解密歸檔之物理與材料研究公報。涵蓋超材料微結構、非平衡態等離子體物理或特種同位素比率分析，為外來科技逆向工程與物理檢驗提供基礎科學存證：{abstract[:180]}...",
                            "en": f"Official Department of Energy National Laboratories declassified research record (OSTI: {osti_id}) addressing anomalous physical characteristics, metamaterial waveguides, or isotope ratios."
                        },
                        "agency": {
                            "name": "Department of Energy (OSTI / National Laboratories)",
                            "zh_hk": "美國能源部科學與技術資訊辦公室",
                            "country": "US"
                        },
                        "entities": {
                            "agencies": ["Department of Energy", "Los Alamos National Laboratory", "Sandia National Laboratories", "Oak Ridge National Laboratory"],
                            "people": []
                        },
                        "sources": [
                            {
                                "name": "DOE OSTI Official Public Database",
                                "url": f"https://www.osti.gov/biblio/{osti_id}",
                                "format": "html",
                                "sha256": report_hash,
                                "sha256_verified": False,
                                "archived_at": now_iso
                            }
                        ],
                        "tags": ["DOE", "OSTI", "National Labs", "Metamaterials", "Isotope Analysis", "Restricted Data"]
                    }
                    records.append(record)

        except Exception as exc:
            print(f"  ⚠️ [DOE OSTI API 警告] 暫時無法連線至能源部技術公報端點: {exc}", file=sys.stderr)

        return records
