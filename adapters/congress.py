"""
Congress.gov UAP Legislative Tracking Adapter
美國國會 API 法案與情報授權條款動態適配器 (對齊 Schema v2.0.0)
"""
import os
from typing import Any, Dict, List
import requests
from adapters.base import BaseAdapter


class CongressAdapter(BaseAdapter):
    """
    美國國會 API 適配器 (對齊 Schema v2.0.0)
    """
    BASE_URL = "https://api.congress.gov/v3"

    TARGET_BILLS = [
        {"congress": 118, "type": "hr", "number": 2670},   # FY2024 NDAA
        {"congress": 118, "type": "s", "number": 2226},    # Schumer UAPDA
        {"congress": 118, "type": "hr", "number": 8070},   # FY2025 NDAA
    ]

    def __init__(self, api_key: str = ""):
        super().__init__(source_name="congress_gov")
        self.api_key = api_key or os.getenv("CONGRESS_API_KEY", "").strip()

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        if not self.api_key:
            print("[CongressAdapter] ℹ 未檢測到 CONGRESS_API_KEY，跳過國會法案抓取（優雅降級）。")
            return []

        results: List[Dict[str, Any]] = []

        for target in self.TARGET_BILLS:
            cong = target["congress"]
            b_type = target["type"]
            b_num = target["number"]

            url = f"{self.BASE_URL}/bill/{cong}/{b_type}/{b_num}"
            headers = {"x-api-key": self.api_key}
            params = {"format": "json"}

            try:
                res = requests.get(url, headers=headers, params=params, timeout=15)
                if res.status_code == 404:
                    continue
                res.raise_for_status()
                data = res.json().get("bill", {})

                summary_text = self._fetch_summary(cong, b_type, b_num, self.api_key)
                if not summary_text:
                    summary_text = data.get("title", "")

                data["fetched_summary"] = summary_text
                results.append(self._normalize(data))
            except Exception as e:
                print(f"[CongressAdapter] ⚠️ 獲取法案 {cong}-{b_type}-{b_num} 失敗: {e}")

        return results

    def _fetch_summary(self, congress: int, bill_type: str, bill_num: int, api_key: str) -> str:
        url = f"{self.BASE_URL}/bill/{congress}/{bill_type}/{bill_num}/summaries"
        try:
            r = requests.get(url, headers={"x-api-key": api_key}, params={"format": "json"}, timeout=10)
            if r.status_code == 200:
                summaries = r.json().get("summaries", [])
                if summaries:
                    return summaries[-1].get("text", "")
        except Exception:
            pass
        return ""

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        cong = raw.get("congress")
        b_type = str(raw.get("type", "")).upper()
        b_num = raw.get("number")
        doc_id = f"CONG-{cong}-{b_type}-{b_num}"

        latest_action = raw.get("latestAction", {})
        action_date = latest_action.get("actionDate") or raw.get("updateDate", "2024-01-01")

        title = raw.get("title", f"{cong}th Congress {b_type} {b_num}")
        summary = raw.get("fetched_summary") or title

        clean_summary = summary.replace("<p>", "").replace("</p>", "").replace("<br>", "").replace("\n", " ").strip()
        if len(clean_summary) > 300:
            clean_summary = clean_summary[:300] + "..."

        bill_url = f"https://www.congress.gov/bill/{cong}th-congress/{b_type.lower()}-bill/{b_num}"

        return {
            "id": doc_id,
            "type": "bill",
            "date": {
                "val": action_date,
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
                    "title": title,
                    "executive_summary": clean_summary
                },
                "zh_hk": {
                    "title": f"第 {cong} 屆美國國會 {b_type} {b_num} 號法案（含 UAP 披露條款）",
                    "executive_summary": f"法案最新進展：{latest_action.get('text', '審議中')}。涵蓋國防部異常現象調查撥款與跨部會解密審查程序要求。"
                }
            },
            "entities": {
                "agencies": ["United States Congress"],
                "people": []
            },
            "sources": [
                {
                    "label": "Congress.gov Official Portal",
                    "url": bill_url,
                    "sha256": None
                }
            ],
            "tags": ["Congress", "Legislation", "NDAA", "UAPDA", "Statutory"]
        }


# 別名相容
CongressGovAdapter = CongressAdapter
