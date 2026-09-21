# scripts/probe_fr.py
import json
import os
from pathlib import Path
import sys
import time
import traceback
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List
import requests

BASE = "https://www.federalregister.gov/api/v1/documents.json"
HEADERS = {
    "User-Agent": "TheVeil-OSINT-Auditor/2.0 (+https://github.com/jackylawck/veil; audit-probe)",
    "Accept": "application/json"
}


def probe(label: str, params: Dict[str, Any], retries: int = 2) -> int:
    """向 Federal Register API 發送階梯探針請求，具備重試、指數退避與安全防禦。"""
    for attempt in range(retries + 1):
        try:
            r = requests.get(BASE, params=params, headers=HEADERS, timeout=15)
            r.raise_for_status()
            data = r.json()
            count = data.get("count", 0)
            results = data.get("results", [])

            print(f"\n[{label}]")
            print(f"   🔗 實際請求 URL : {r.url}")
            print(f"   📊 總數 count: {count:<4} | 本頁回傳: {len(results)}")

            if results:
                for idx, item in enumerate(results[:3], start=1):
                    agencies_raw = item.get("agencies") or []
                    agencies = [
                        a.get("raw_name")
                        for a in agencies_raw
                        if isinstance(a, dict) and a.get("raw_name")
                    ]
                    
                    pub_date = item.get("publication_date") or "UNKNOWN-DATE"
                    doc_type = item.get("type") or "UNKNOWN"
                    raw_title = item.get("title") or "Untitled Document"
                    doc_num = item.get("document_number") or "N/A"

                    print(f"   └─ #{idx} [{pub_date}] [{doc_type:<8}] {raw_title[:60]}...")
                    print(f"      機關: {agencies[:2]} | Doc#: {doc_num}")
            else:
                print("   ⚠️  本查詢條件下查無符合公報")

            return count

        except (requests.exceptions.RequestException, json.JSONDecodeError) as exc:
            if attempt < retries:
                wait_sec = 2 ** attempt
                print(f"   ⚠️  請求異常 ({exc})，{wait_sec} 秒後進行第 {attempt + 1} 次重試...")
                time.sleep(wait_sec)
                continue
            print(f"\n[{label}] -> ❌ 請求徹底失敗（已重試 {retries} 次）: {exc}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return -1
        except Exception as exc:
            print(f"\n[{label}] -> ❌ 解析過程拋出未預期例外: {exc}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return -1

    return -1


def main() -> int:
    env_days = os.getenv("PROBE_DAYS_BACK", "365").strip()
    try:
        days_back_int = int(env_days)
    except ValueError:
        days_back_int = 365

    days_back_int = max(1, min(days_back_int, 36500))

    today = datetime.now(timezone.utc)
    cutoff_date = (today - timedelta(days=days_back_int)).strftime("%Y-%m-%d")

    # 檢索語句優化：同時相容自訂語句與最精確的聯邦公報關鍵詞集
    custom_term = os.getenv("PROBE_CUSTOM_TERM", "").strip()
    if custom_term:
        search_term = custom_term
    else:
        # Federal Register 官方最能命中的短語與詞條
        search_term = 'unidentified aerial OR "All-Domain Anomaly Resolution Office" OR "AARO"'

    print("=" * 75)
    print("🔍 Federal Register 階梯式審計診斷開始")
    print(f"   基準時間 : {today.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"   回溯窗口 : {days_back_int} 日 (截斷點: >= {cutoff_date})")
    print(f"   檢索語句 : {search_term}")
    print("=" * 75)

    results: Dict[str, int] = {}

    # 測試 0：陽性對照組（驗證 API 端點在線狀態）
    results["test_0_positive_control"] = probe(
        "0. 陽性對照組 (搜尋 'NASA'，驗證端點連線與解析完整性)",
        {"conditions[term]": "NASA", "per_page": 3, "order": "newest"},
    )
    time.sleep(1)

    # 測試 1：全歷史寬鬆搜尋
    results["test_1_all_history"] = probe(
        "1. 全歷史寬鬆檢索 (無時間/類型限制)",
        {"conditions[term]": search_term, "per_page": 5, "order": "newest"},
    )
    time.sleep(1)

    # 測試 2：專項法規短語精確命中 (AARO 專項)
    results["test_2_specific_phrase"] = probe(
        "2. 全歷史專項短語 (鎖定 'All-Domain Anomaly Resolution Office')",
        {
            "conditions[term]": '"All-Domain Anomaly Resolution Office"',
            "per_page": 5,
            "order": "newest",
        },
    )
    time.sleep(1)

    # 測試 3：動態回溯時間窗口過濾
    results["test_3_with_window"] = probe(
        f"3. 動態窗口過濾 (>= {cutoff_date})",
        {
            "conditions[term]": search_term,
            "conditions[publication_date][gte]": cutoff_date,
            "per_page": 5,
            "order": "newest",
        },
    )
    time.sleep(1)

    # 測試 4：動態窗口 + 公報類型過濾
    results["test_4_with_type"] = probe(
        "4. 動態窗口 + 類型過濾 (NOTICE, RULE, PRESDOCU)",
        {
            "conditions[term]": search_term,
            "conditions[publication_date][gte]": cutoff_date,
            "conditions[type][]": ["NOTICE", "RULE", "PRESDOCU"],
            "per_page": 5,
            "order": "newest",
        },
    )
    time.sleep(1)

    # 測試 5：動態窗口 + 核心防衛機關過濾 (國防部、NASA、FAA)
    results["test_5_with_agencies"] = probe(
        "5. 動態窗口 + 類型 + 核心防衛機關過濾 (DoD / NASA / FAA)",
        {
            "conditions[term]": search_term,
            "conditions[publication_date][gte]": cutoff_date,
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

    # ==========================================
    # 📊 診斷匯總與智能結論生成
    # ==========================================
    print("\n" + "=" * 75)
    print("📊 Federal Register 診斷匯總報告")
    print("=" * 75)
    
    for test_key, count in results.items():
        if count == -1:
            status = "❌ 請求失敗 (API 錯誤或網路中斷)"
        elif count == 0:
            status = "⚠️ 0 筆命中"
        else:
            status = f"✅ 命中 {count} 筆"
        print(f"  • {test_key:<32} : {status}")

    print("-" * 75)
    print("💡 智能適配器診斷結論 (Diagnostic Conclusion):")
    
    if results.get("test_0_positive_control", -1) <= 0:
        conclusion = "❌ [致命] 陽性對照組失敗！探針本身或遠端 Federal Register API 嚴重故障，無法進行有效診斷。"
    elif results.get("test_1_all_history", 0) == 0:
        conclusion = "⚠️ [警報] 全歷史檢索無任何結果，請檢視關鍵詞拼寫或是否包含特殊未轉義字元。"
    elif results.get("test_5_with_agencies", 0) == 0 and results.get("test_4_with_type", 0) > 0:
        conclusion = "💡 [建議] 加上 agency slug 過濾後筆數歸零，但放寬機關後有結果。建議 adapter 移除特定 agency 過濾條件，改由全域檢索確保不漏接跨部會公報。"
    elif results.get("test_5_with_agencies", 0) > 0:
        conclusion = "✅ [通過] 目前聯邦公報的 Agency 與類型過濾條件運行正常，轉入 Adapter 生產無虞。"
    else:
        conclusion = "❓ [注意] 探針順利完成，但查詢結果分佈異常，請結合上方各階梯明細進行判定。"
        
    print(f"   {conclusion}")
    print("=" * 75)

    # 輸出結構化結果到 GitHub Actions Step Summary（若環境支援）
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path and Path(summary_path).exists():
        with open(summary_path, "a", encoding="utf-8") as sf:
            sf.write("### 🔍 Federal Register API 診斷摘要\n\n")
            sf.write(f"- **診斷結論**: {conclusion}\n")
            sf.write(f"- **回溯窗口**: {days_back_int} 天 (`>= {cutoff_date}`)\n\n")
            sf.write("| 測試階梯項目 | 探測狀態 |\n|---|---|\n")
            for k, v in results.items():
                v_str = f"命中 {v} 筆" if v > 0 else ("0 筆" if v == 0 else "請求失敗")
                sf.write(f"| `{k}` | {v_str} |\n")

    # 退出碼策略
    if results.get("test_0_positive_control", -1) == -1:
        print("❌ 診斷終止：陽性對照探針請求失敗，回傳退出碼 1", file=sys.stderr)
        return 1
        
    if all(c == -1 for c in results.values()):
        print("❌ 診斷終止：所有階梯探針全數請求失敗，回傳退出碼 1", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
