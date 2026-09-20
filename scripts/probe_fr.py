# scripts/probe_fr.py
import requests
import json

BASE = "https://www.federalregister.gov/api/v1/documents.json"

def probe(label, params):
    try:
        r = requests.get(BASE, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        count = data.get('count', 0)
        results = data.get('results', [])
        print(f"\n[{label}] -> 總數 count: {count} | 本頁回傳: {len(results)}")
        if results:
            first = results[0]
            print(f"   最新一筆日期: {first.get('publication_date')} | 標題: {first.get('title')[:60]}...")
            print(f"   文件類型: {first.get('type')} | 機關: {[a.get('raw_name') for a in first.get('agencies', [])]}")
        return count
    except Exception as e:
        print(f"\n[{label}] -> 請求錯誤: {e}")
        return None

print("=" * 60)
print("🔍 Federal Register 搜尋條件階梯式診斷開始...")
print("=" * 60)

# 測試 1：精確短語全歷史（看歷史上到底有沒有收錄這些詞）
probe("1. 精確短語 (全歷史)", {
    "conditions[term]": '"unidentified anomalous phenomena" OR "All-domain Anomaly Resolution Office" OR "AARO"',
    "per_page": 5,
    "order": "newest"
})

# 測試 2：精確短語 + 最近 365 天
probe("2. 精確短語 + 最近 365 天", {
    "conditions[term]": '"unidentified anomalous phenomena" OR "All-domain Anomaly Resolution Office" OR "AARO"',
    "conditions[publication_date][gte]": "2025-09-20",
    "per_page": 5,
    "order": "newest"
})

# 測試 3：精確短語 + 最近 365 天 + 類型過濾 (NOTICE, RULE, PRESDOCU)
probe("3. 測試 2 + 類型過濾", {
    "conditions[term]": '"unidentified anomalous phenomena" OR "All-domain Anomaly Resolution Office" OR "AARO"',
    "conditions[publication_date][gte]": "2025-09-20",
    "conditions[type][]": ["NOTICE", "RULE", "PRESDOCU"],
    "per_page": 5,
    "order": "newest"
})

# 測試 4：精確短語 + 最近 365 天 + 類型 + 機關過濾
probe("4. 測試 3 + 機關過濾 (DoD / NASA / FAA)", {
    "conditions[term]": '"unidentified anomalous phenomena" OR "All-domain Anomaly Resolution Office" OR "AARO"',
    "conditions[publication_date][gte]": "2025-09-20",
    "conditions[type][]": ["NOTICE", "RULE", "PRESDOCU"],
    "conditions[agencies][]": [
        "defense-department",
        "national-aeronautics-and-space-administration",
        "federal-aviation-administration",
    ],
    "per_page": 5,
    "order": "newest"
})

print("\n" + "=" * 60)
print("🏁 診斷結束")
print("=" * 60)
