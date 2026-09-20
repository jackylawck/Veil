# scripts/ingest.py
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback
from datetime import datetime, timezone
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from adapters.base import BaseAdapter
from adapters.federal_register import FederalRegisterAdapter
from adapters.congress import CongressAdapter
from adapters.govinfo import GovInfoAdapter


def parse_date_safe(date_str: str) -> datetime:
    """健全解析多元日期格式（含 ISO 8601 / 時區），供時間軸嚴格排序。"""
    if not date_str or not isinstance(date_str, str):
        return datetime(1900, 1, 1, tzinfo=timezone.utc)
    
    # 優先嘗試 ISO 格式 (例如 2026-09-18T14:30:00Z)
    try:
        clean_str = date_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_str)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        pass

    # 次選常見常規日期格式
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
            
    return datetime(1900, 1, 1, tzinfo=timezone.utc)


def load_curated_historical_records() -> List[Dict[str, Any]]:
    """載入歷史典藏底庫 (data/curated_historical.json)。
    
    嚴格拒絕靜默退化：檔案損毀時拋出例外阻斷管線，防止歷史資料蒸發。
    """
    curated_file = ROOT_DIR / "data" / "curated_historical.json"
    if not curated_file.exists():
        print(f"⚠️ 提示: 歷史典藏庫檔案不存在: {curated_file}", file=sys.stderr)
        return []
        
    try:
        with open(curated_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"❌ 致命錯誤: curated_historical.json JSON 語法損毀: {exc}") from exc
    except OSError as exc:
        raise RuntimeError(f"❌ 致命錯誤: 無法讀取 curated_historical.json: {exc}") from exc

    records = data if isinstance(data, list) else data.get("records", [])
    if not isinstance(records, list):
        raise RuntimeError("❌ 致命錯誤: curated_historical.json 頂層結構必須為清單 (list) 或包含 records 清單")
        
    return records


def records_equal(a: List[Dict[str, Any]], b: List[Dict[str, Any]]) -> bool:
    """深度比對兩份卷宗清單的實質內容（含屬性與排序），偵測內文或狀態更新。"""
    if len(a) != len(b):
        return False
    # 透過 JSON canonical serialization 進行嚴格內容比對
    for item_a, item_b in zip(a, b):
        if not isinstance(item_a, dict) or not isinstance(item_b, dict):
            return False
        if json.dumps(item_a, sort_keys=True) != json.dumps(item_b, sort_keys=True):
            return False
    return True


def run_ingestion(days_back: int = 30) -> None:
    """執行全管線情報採集：
    
    1. 載入靜態歷史底庫
    2. 採集動態 API 增量
    3. 去重與嚴格日期排序
    4. 內容級別冪等比對：內容完全相同時跳過寫入，杜絕無效 PR
    """
    start_time = datetime.now(timezone.utc)
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] 啟動情報採集管線 (動態增量窗口: {days_back} 日)...")

    all_records: List[Dict[str, Any]] = []
    seen_ids = set()

    # 1. 載入靜態歷史底庫
    historical = load_curated_historical_records()
    for r in historical:
        rid = r.get("id")
        if rid and rid not in seen_ids:
            seen_ids.add(rid)
            all_records.append(r)
    print(f"✔ 成功載入歷史里程碑典藏: {len(all_records)} 筆")

    # 2. 註冊動態 API 適配器
    active_adapters: List[BaseAdapter] = [
        FederalRegisterAdapter(),
        GovInfoAdapter(),
    ]
    
    congress_key = os.environ.get("CONGRESS_API_KEY", "").strip()
    if congress_key:
        active_adapters.append(CongressAdapter(api_key=congress_key))
    else:
        print("⚠️ 未檢測到 CONGRESS_API_KEY，略過 Congress.gov 動態採集", file=sys.stderr)

    api_metrics: Dict[str, Dict[str, Any]] = {}

    # 3. 採集動態增量
    for adapter in active_adapters:
        name = getattr(adapter, "source_name", adapter.__class__.__name__)
        try:
            fetched = adapter.fetch_records(days_back=days_back)
            added = 0
            for r in fetched:
                rid = r.get("id")
                if rid and rid not in seen_ids:
                    seen_ids.add(rid)
                    all_records.append(r)
                    added += 1
            api_metrics[name] = {
                "status": "success",
                "fetched": len(fetched),
                "new": added,
            }
            print(f"  ✔ [API: {name:<20}] 抓取 {len(fetched)} 筆，新增入庫 {added} 筆")
        except Exception as exc:
            print(f"  ✖ [API: {name:<20}] 採集失敗: {exc}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            api_metrics[name] = {
                "status": "failed",
                "error": str(exc),
            }

    # 防衛性斷路器：若所有活躍動態 API 全數崩潰，中止管線
    failed_count = sum(1 for m in api_metrics.values() if m.get("status") == "failed")
    if active_adapters and failed_count == len(active_adapters):
        print("❌ 致命錯誤: 所有動態適配器均執行失敗，中止構建以維護端點完整！", file=sys.stderr)
        sys.exit(1)

    # 4. 嚴格日期排序 (最新置頂)
    all_records.sort(
        key=lambda x: parse_date_safe(x.get("date", {}).get("val", "")),
        reverse=True,
    )

    out_dir = ROOT_DIR / "public" / "api"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "records-latest.json"
    sha_file = out_dir / "records-latest.json.sha256"

    # 5. 深度內容級冪等性驗證
    if out_file.exists():
        try:
            with open(out_file, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            
            existing_records = existing_data.get("records", []) if isinstance(existing_data, dict) else existing_data
            
            if isinstance(existing_records, list) and records_equal(existing_records, all_records):
                print("\n✔ [冪等生效] 卷宗內容無任何異動，跳過主檔覆寫。")
                # 確保校驗 SHA 檔案一定與既有檔案對齊，防止手動修改脫節
                existing_bytes = out_file.read_bytes()
                correct_hash = hashlib.sha256(existing_bytes).hexdigest()
                sha_file.write_text(f"{correct_hash}  records-latest.json\n", encoding="utf-8")
                return
        except (json.JSONDecodeError, OSError, ValueError):
            print("⚠️ 既有檔案損毀或解析異常，重新全量生成。", file=sys.stderr)

    # 6. 生成新資料並寫入磁碟
    end_time = datetime.now(timezone.utc)
    duration = round((end_time - start_time).total_seconds(), 2)

    output_data = {
        "metadata": {
            "title": "The Veil - Global UAP Intelligence Ledger",
            "zh_title": "揭帷 - 全球主權防衛與官方解密情報總帳",
            "generated_at": end_time.isoformat(),
            "duration_sec": duration,
            "total_records": len(all_records),
            "curated_historical_records": len(historical),
            "live_adapters_active": len(active_adapters),
            "api_metrics": api_metrics,
        },
        "records": all_records,
    }

    json_bytes = json.dumps(output_data, ensure_ascii=False, indent=2).encode("utf-8")
    out_file.write_bytes(json_bytes)

    # 簽署 SHA-256
    sha256_hash = hashlib.sha256(json_bytes).hexdigest()
    sha_file.write_text(f"{sha256_hash}  records-latest.json\n", encoding="utf-8")

    print("\n" + "=" * 60)
    print(f" 總帳生成完畢！總卷宗數: {len(all_records)} 筆 (耗時: {duration}s)")
    print(f" 主端點: {out_file}")
    print(f" SHA-256: {sha256_hash}")
    print("=" * 60)


if __name__ == "__main__":
    days = 30
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            print(f"⚠️ 無效的天數參數: '{sys.argv[1]}'，自動使用預設值 30 天", file=sys.stderr)
    run_ingestion(days_back=days)
