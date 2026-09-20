# adapters/dod_oig_eval.py
import json
from typing import Any, Dict, List
from .base import BaseAdapter


class DodOigEvalAdapter(BaseAdapter):
    """
    美國國防部督察長辦公室 (DoD OIG) 官方審計報告適配器
    索引評估五角大廈 UAP 應對措施之法定監察報告 (DODIG-2023-109)
    """
    TARGET_RECORDS = [
        {
            "id": "DODIG-2023-109-UAP-EVAL",
            "title": "DoD Office of Inspector General: Evaluation of the DoD's Actions Regarding Unidentified Anomalous Phenomena (Report No. DODIG-2023-109)",
            "zh_title": "美國國防部督察長辦公室：國防部處理未知異常現象 (UAP) 行動之官方評估與審計報告",
            "zh_summary": "國防部最高獨立監察機關對五角大廈、三軍司令部及反情報機構進行全面審計後發布之官方解密報告。報告明確指出國防部缺乏統籌協調的處置政策，未能有效評估與消除 UAP 對國家安全與飛行安全構成之威脅，並提出 11 項強制整改建議。",
            "date": "2024-01-25",
            "url": "https://www.dodig.mil",
            "agencies": [
                "Department of Defense Office of Inspector General (DoD OIG)",
                "Office of the Secretary of Defense",
                "All-domain Anomaly Resolution Office (AARO)"
            ]
        }
    ]

    @property
    def source_name(self) -> str:
        return "dod_oig_eval"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self.TARGET_RECORDS:
            results.append(self._normalize(item))
        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        return {
            "id": raw["id"],
            "type": "official_report",
            "date": {
                "val": raw["date"],
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_statutory_inspector_general_audit",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": raw["agencies"]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": raw["title"],
                    "executive_summary": "Statutory oversight evaluation issued by the Inspector General determining that DoD's lack of a comprehensive approach to UAP poses national security risks."
                },
                "zh_hk": {
                    "title": raw["zh_title"],
                    "executive_summary": raw["zh_summary"]
                }
            },
            "sources": [
                {
                    "label": f"DoD OIG Oversight Publication ({raw['id']})",
                    "url": raw["url"],
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
