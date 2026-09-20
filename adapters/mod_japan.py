# adapters/mod_japan.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class ModJapanAdapter(BaseAdapter):
    """
    日本防衛省 (Ministry of Defense, Japan) 適配器
    索引防衛省對自衛隊頒布之不明飛行物遭遇官方通報程序與雷達紀錄大臣訓令
    """
    TARGET_RECORDS = [
        {
            "id": "JP-MOD-DIRECTIVE-20200914",
            "title": "Ministry of Defense Directive: Operational Procedures for Unidentified Flying Objects Encountered by the Self-Defense Forces",
            "zh_title": "日本防衛省：自衛隊遭遇不明飛行物時之官方應對與分析程序大臣訓令",
            "zh_summary": "2020 年 9 月 14 日防衛大臣正式下達防衛省訓令，強制自衛隊戰機、艦艇在遭遇未知飛行物體時執行標準攝影、雷達信號留存與統合幕僚監部專項通報機制，建立東亞首個官方防衛通報標準流程。",
            "date": "2020-09-14",
            "url": "https://www.mod.go.jp",
            "agencies": ["Ministry of Defense (Japan)", "Joint Staff Office", "Japan Air Self-Defense Force"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "mod_japan"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "official_notice",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_ministerial_directive",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "ja",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Official ministerial directive establishing defense telemetry recording, optical tracking, and reporting protocols for the Japan Self-Defense Forces."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"Japan MoD Official Press Release ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
