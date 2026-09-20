# scripts/ingest.py
from datetime import datetime
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List

# 動態將專案根目錄加入 Python 模組搜尋路徑（解決 ModuleNotFoundError）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# 當前啟用的 Adapters 註冊清單
from adapters.federal_register import FederalRegisterAdapter

# 未來逐步新增：
# from adapters.congress import CongressGovAdapter
# from adapters.govinfo import GovInfoAdapter

ACTIVE_ADAPTERS = [
    FederalRegisterAdapter(),
    # CongressGovAdapter(api_key=os.getenv("CONGRESS_API_KEY")),
]


def run_pipeline():
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    os.makedirs("drafts", exist_ok=True)
    draft_path = f"drafts/{today_str}.json"

    # 若今天已有草稿則讀取，以便增量合併
    existing_records: Dict[str, Any] = {}
    if os.path.exists(draft_path):
        with open(draft_path, "r", encoding="utf-8") as f:
            for item in json.load(f):
                existing_records[item["id"]] = item

    new_count = 0
    for adapter in ACTIVE_ADAPTERS:
        print(f"[*] Running adapter: {adapter.source_name}...")
        try:
            records = adapter.fetch_records()
            for r in records:
                if r["id"] not in existing_records:
                    existing_records[r["id"]] = r
                    new_count += 1
        except Exception as e:
            print(f"[!] Error in {adapter.source_name}: {e}")

    # 輸出至今日 Draft
    output_list = list(existing_records.values())
    with open(draft_path, "w", encoding="utf-8") as f:
        json.dump(output_list, f, ensure_ascii=False, indent=2)

    print(f"[✓] Ingest complete. {new_count} new entries written to {draft_path}")

    # 設定輸出環境變數，讓 GitHub Actions 知道是否有新資料以及今天的日期字串
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as env_file:
            env_file.write(f"new_records={new_count}\n")
            env_file.write(f"today_str={today_str}\n")


if __name__ == "__main__":
    run_pipeline()
