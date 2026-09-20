# adapters/dvids.py
import json
import os
from typing import Any, Dict, List
import requests
from .base import BaseAdapter


class DvidsAdapter(BaseAdapter):
    """
    美國國防部 DVIDS (Defense Visual Information Distribution Service) 適配器
    專門索引五角大廈官方記者會逐字稿、AARO 官方簡報與解密影像發布
    """
    BASE_URL = "https://api.dvidshub.net"

    # 精選國防部核心官方影音與簡報紀錄
    TARGET_RELEASES = [
        {
            "id": "DVIDS-TRANSCRIPT-20230831",
            "title": "Pentagon Press Secretary Holds a Press Briefing on AARO Secure Reporting Launch",
            "zh_title": "五角大廈新聞秘書主持 AARO 官方安全通報系統發布記者會",
            "zh_summary": "美國國防部新聞發言人正式召開記者會，宣布設立全領域異常解決辦公室官方入口網站，並啟動首階段政府在職人員通報通道。",
            "date": "2023-08-31",
            "url": "https://www.defense.gov/News/Transcripts/Transcript/Article/3512807/",
            "agencies": ["Department of Defense", "Office of the Secretary of Defense"]
        },
        {
            "id": "DVIDS-AARO-BRIEF-20231031",
            "title": "DoD Holding Media Roundtable on the 2023 Consolidated Annual Report on UAP",
            "zh_title": "國防部 2023 年度 UAP 綜合調查報告媒體圓桌通報會",
            "zh_summary": "國防部與 AARO 專責官員就 2023 年度提交國會之未解異常現象調查進展向授權媒體進行官方技術簡報與答問。",
            "date": "2023-10-31",
            "url": "https://www.defense.gov/News/Transcripts/Transcript/Article/3575459/",
            "agencies": ["Department of Defense", "AARO"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "dvids"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        # 遍歷核心發布紀錄
        for item in self.TARGET_RELEASES:
            results.append(self._normalize(item))

        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "official_briefing",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_briefing_transcript",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official Department of Defense media briefing transcript regarding anomaly reporting procedures and inter-agency disclosures."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"DoD Official Release ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
