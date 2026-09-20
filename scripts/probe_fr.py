# scripts/probe_fr.py
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import requests

BASE = "https://www.federalregister.gov/api/v1/documents.json"
HEADERS = {"User-Agent": "TheVeil-OSINT-Auditor/1.0 (Audit-Grade UAP Research)"}


def probe(label: str, params: Dict[str, Any]) -> int:
    try:
        r = requests.get(BASE, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        count = data.get("count", 0)
        results = data.get("results", [])

        print(f"\n[{label}]")
        print(f"   🔗 實際請求 URL : {r.url}")
        print(
            f"   📊 總數 count: {count:<4} | 本頁回傳: {len(results)}"
        )

        if results:
            for idx, item in enumerate(results[:3], start=1):
                agencies = [
                    a.get("raw_name") for a in item.get("agencies", [])
                ]
                print(
                    f"   └─ #{idx} [{item.get('publication_date')}] [{item.get('type'):<8}] {item.get('title')[:55]}..."
                )
                print(
                    f"      機關: {agencies[:2]} | Doc#: {item.get('document_number')}"
                )
        else:
            print("   ⚠️  本查詢條件下查無符合公報")

        return count
    except Exception as e:
        print(f"\n[{label}] -> ❌ 請求失敗: {e}")
        return -1


# 計算動態時間窗口（最近 365 天）
today = datetime.now(timezone.utc)
date_365d_ago = (today - timedelta(days=365)).strftime("%Y-%m-%d")

# 涵蓋 UAP 歷史沿革（含 2022 前的 aerial 與 2022 後的 anomalous）
SEARCH_TERM = (
    '"unidentified anomalous phenomena" '
    '"unidentified aerial phenomena" '
    '"All-domain Anomaly Resolution Office" '
    '"AARO"'
)

print("=" * 70)
print(
    f"🔍 Federal Register 階梯式診斷開始 (基準日: {today.strftime('%Y-%m-%d')} | 窗口: {date_365d_ago})"
)
print("=" * 70)

# 測試 1：全歷史全域搜尋（驗證底層資料庫命中度）
probe(
    "1. 全歷史寬鬆字串搜尋 (無任何時間/類型過濾)",
    {"conditions[term]": SEARCH_TERM, "per_page": 5, "order": "newest"},
)

# 測試 2：全歷史精確短語（測試雙引號在 API 中的有效性）
probe(
    "2. 全歷史特定短語 (專門鎖定 AARO 機構名稱)",
    {
        "conditions[term]": '"All-Domain Anomaly Resolution Office"',
        "per_page": 5,
        "order": "newest",
    },
)

# 測試 3：動態 365 天窗口
probe(
    f"3. 最近 365 天 (>= {date_365d_ago})",
    {
        "conditions[term]": SEARCH_TERM,
        "conditions[publication_date][gte]": date_365d_ago,
        "per_page": 5,
        "order": "newest",
    },
)

# 測試 4：動態 365 天 + 官方文件類型過濾 (NOTICE, RULE, PRESDOCU)
probe(
    "4. 最近 365 天 + 類型過濾 (NOTICE, RULE, PRESDOCU)",
    {
        "conditions[term]": SEARCH_TERM,
        "conditions[publication_date][gte]": date_365d_ago,
        "conditions[type][]": ["NOTICE", "RULE", "PRESDOCU"],
        "per_page": 5,
        "order": "newest",
    },
)

# 測試 5：動態 365 天 + 類型 + 國防/航太相關部會 slug 過濾
probe(
    "5. 最近 365 天 + 類型 + 核心機關過濾 (DoD / NASA / FAA)",
    {
        "conditions[term]": SEARCH_TERM,
        "conditions[publication_date][gte]": date_365d_ago,
        "conditions[type][]": ["NOTICE", "RULE", "PRESDOCU"],
        "conditions[agencies][]": [
            "defense-department",
            "national-aeronautics-and-space-administration",
            "federal-aviation-administration",
        ],
        "per_page": 5,
        "order": "newest",
    },
)

print("\n" + "=" * 70)
print("🏁 診斷結束")
print("=" * 70)
