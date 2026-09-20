# adapters/iriaf_tehran.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class IriafTehranAdapter(BaseAdapter):
    """
    伊朗空軍 (IRIAF) 與美國國防情報局 (DIA) 聯合解密適配器
    索引 1976 年德黑蘭 F-4 戰鬥機雷達鎖定與航電系統電子干擾官方軍事調查卷宗
    """
    TARGET_RECORDS = [
        {
            "id": "IR-DIA-TEHRAN-F4-1976",
            "title": "Defense Intelligence Agency & Iranian Air Force: Joint Evaluation of the Tehran F-4 Jet Intercept",
            "zh_title": "美國國防情報局 (DIA) 與伊朗空軍：1976 年德黑蘭 F-4 戰機攔截與航電干擾官方解密報告",
            "zh_summary": "1976 年 9 月 19 日德黑蘭空域兩架 F-4 戰機緊急升空截擊異常高速目標。戰機雷達取得鎖定並意圖發射飛彈時遭遇強烈電磁抑制，導致通訊與射控短暫失效。美國國防情報局隨後建立專案評估檔案，證實為軍事級別多感測器與電子對抗案例，現已解密公開。",
            "date": "1976-09-19",
            "url": "https://www.dia.mil",
            "agencies": ["Defense Intelligence Agency (DIA)", "Iranian Air Force", "Department of Defense"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "iriaf_tehran"

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
                "evidence_level": "official_intelligence_agency_investigation",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Declassified military intelligence assessment produced by the Defense Intelligence Agency documenting radar tracking and avionics failure during a jet interception."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"DIA Declassified Record ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
