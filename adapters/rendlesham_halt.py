# adapters/rendlesham_halt.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class RendleshamHaltAdapter(BaseAdapter):
    """
    北約駐英美軍基地副基地長 Halt 中校備忘錄與英國國防部官方解密檔案適配器
    索引 1980 年藍道申森林核打擊前哨基地空軍警衛部隊目擊與實體輻射殘留測量案卷
    """
    TARGET_RECORDS = [
        {
            "id": "NATO-USAF-HALT-MEMO-19810113",
            "title": "USAF 81st Tactical Fighter Wing: Official Memorandum on Unexplained Lights at RAF Woodbridge (The Halt Memo)",
            "zh_title": "美國空軍第 81 聯隊副基地長：伍德布里奇基地不明飛行目標與輻射痕跡官方備忘錄",
            "zh_summary": "1980 年 12 月北約美軍核基地周邊警衛部隊目視三角形幾何飛行器著陸並探測到著陸壓痕與異常輻射。副基地長 Halt 中校親筆簽署軍事備忘錄呈交英國國防部，全卷後由英國國家檔案館公開解密典藏。",
            "date": "1981-01-13",
            "url": "https://discovery.nationalarchives.gov.uk/details/r/C10103138",
            "agencies": ["US Air Force (USAF)", "UK Ministry of Defence (MoD)", "The National Archives (UK)"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "rendlesham_halt"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "declassified_archive",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_nato_base_commander_memorandum",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official military memorandum submitted by USAF Deputy Base Commander Lt Col Charles Halt to the UK Ministry of Defence documenting physical traces, radiation telemetry, and tactical security police observations."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"UK MoD / TNA Archive ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
