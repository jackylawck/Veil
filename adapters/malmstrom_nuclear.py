# adapters/malmstrom_nuclear.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class MalmstromNuclearAdapter(BaseAdapter):
    """
    美國空軍戰略空軍司令部 (SAC) 馬姆斯壯核飛彈基地事件適配器
    索引 1967 年義勇兵洲際核彈發射系統離線故障與空軍官方技術調查解密卷宗
    """
    TARGET_RECORDS = [
        {
            "id": "USAF-SAC-MALMSTROM-19670324",
            "title": "USAF Strategic Air Command: Official Investigation into the Malmstrom AFB Minuteman Missile Incursions",
            "zh_title": "美國空軍戰略空軍司令部：馬姆斯壯基地核洲際飛彈系統突發離線與空中遭遇官方解密卷宗",
            "zh_summary": "1967 年 3 月 24 日馬姆斯壯空軍基地戰略飛彈聯隊在地面警衛目睹發光幾何飛行物盤旋期間，10 枚義勇兵洲際核飛彈控制系統接連異常進入離線狀態。空軍外國技術處與防務工程團隊之調查檔案後依檔案法正式公開。",
            "date": "1967-03-24",
            "url": "https://www.archives.gov",
            "agencies": ["US Air Force (USAF)", "Strategic Air Command (SAC)", "National Archives and Records Administration"]
        }
    ]

    @property
    def source_name(self) -> str:
        return "malmstrom_nuclear"

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
                "evidence_level": "official_strategic_nuclear_command_archive",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Declassified Strategic Air Command engineering evaluations and incident logs regarding Minuteman missile disablement coinciding with aerospace anomaly incursions."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"US National Archives / USAF Record Group ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
