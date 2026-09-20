# adapters/govinfo.py
import json
import os
from typing import Any, Dict, List
import requests
from .base import BaseAdapter


class GovInfoAdapter(BaseAdapter):
    """
    美國政府出版局 (GPO) GovInfo API 適配器
    專門抓取 Tier-1 級別之國會聽證會宣誓逐字紀錄 (CHRG) 與政府問責報告 (GAO)
    """
    BASE_URL = "https://api.govinfo.gov"

    # 精確鎖定具有歷史與法定意義之 UAP 國會聽證會出版品 Package ID
    TARGET_PACKAGES = [
        # 2023-07-26 眾議院監督委員會 UAP 宣誓聽證會 (David Grusch 等人作證之官方出版紀錄)
        "CHRG-118hhrg52893",
        # 2022-05-17 眾議院情報委員會 UAP 公開聽證會 (半世紀以來首次國會公開聽證)
        "CHRG-117hhrg47894",
    ]

    @property
    def source_name(self) -> str:
        return "govinfo"

    def fetch_records(self, days_back: int = 365) -> List[Dict[str, Any]]:
        api_key = os.getenv("CONGRESS_API_KEY")
        if not api_key:
            print("[GovInfoAdapter] 未檢測到 CONGRESS_API_KEY，跳過 GovInfo 數據抓取。")
            return []

        results: List[Dict[str, Any]] = []

        for pkg_id in self.TARGET_PACKAGES:
            url = f"{self.BASE_URL}/packages/{pkg_id}/summary"
            params = {"api_key": api_key}

            try:
                res = requests.get(url, params=params, timeout=15)
                if res.status_code == 404:
                    continue
                res.raise_for_status()
                pkg_data = res.json()
                results.append(self._normalize(pkg_data))
            except Exception as e:
                print(f"[GovInfoAdapter] 獲取出版品 {pkg_id} 失敗: {e}")

        return results

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raw_str = json.dumps(raw, sort_keys=True)
        pkg_id = raw.get("packageId", "UNKNOWN")
        title = raw.get("title", "Congressional Hearing Record")
        date_issued = raw.get("dateIssued", "2023-07-26")

        # 擷取委員會機構資訊
        committees = raw.get("committees", [])
        committee_names = [c.get("committeeName", "") for c in committees if isinstance(c, dict)]
        if not committee_names:
            committee_names = ["US Congress", "Government Publishing Office (GPO)"]

        # 雙語摘要對應
        zh_title = f"美國國會官方聽證會正式紀錄：{title}"
        zh_summary = "美國政府出版局 (GPO) 正式刊印之國會宣誓聽證會法定逐字紀錄本（含證人宣誓證詞、委員質詢錄與官方送審附件）。"

        if "52893" in pkg_id:
            zh_title = "眾議院監督委員會 UAP 宣誓聽證會正式出版紀錄本（含證人 Grusch 證詞）"
            zh_summary = "眾議院監督與問責委員會舉行之『未知異常現象：對國家安全、公共安全及政府透明度的影響』正式聽證會紀錄本，收錄宣誓證詞與完整質詢記錄。"
        elif "47894" in pkg_id:
            zh_title = "眾議院反恐反情報小組委員會 UAP 歷史性公開聽證會紀錄本"
            zh_summary = "美國國會逾 50 年來首次召開之 UAP 公開聽證會官方公報，由海軍情報副局長與國防部次長出席作證。"

        pdf_url = f"https://www.govinfo.gov/content/pkg/{pkg_id}/pdf/{pkg_id}.pdf"

        return {
            "id": f"GPO-{pkg_id}",
            "type": "official_report",
            "date": {
                "val": date_issued,
                "precision": "day"
            },
            "governance": {
                "source_tier": "Tier-1",
                "evidence_level": "official_hearing_record",
                "confidence_rating": "official_confirmed"
            },
            "entities": {
                "agencies": committee_names[:3]
            },
            "content": {
                "original_language": "en",
                "en": {
                    "title": title,
                    "executive_summary": "Official printed transcript of congressional hearing proceedings published by the U.S. Government Publishing Office under Title 44 oversight."
                },
                "zh_hk": {
                    "title": zh_title,
                    "executive_summary": zh_summary
                }
            },
            "sources": [
                {
                    "label": f"GovInfo Official Package ({pkg_id})",
                    "url": pdf_url,
                    "sha256": self.calculate_sha256(raw_str)
                }
            ]
        }
