# scripts/ingest.py
import hashlib
import importlib
import inspect
import json
import os
from pathlib import Path
import pkgutil
import sys
import tempfile
import traceback
from datetime import datetime, timezone
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import adapters
from adapters.base import BaseAdapter


def parse_date_safe(date_str: str) -> datetime:
    """健全解析多元日期格式（含 ISO 8601 / 時區），供時間軸嚴格排序。"""
    if not date_str or not isinstance(date_str, str):
        return datetime(1900, 1, 1, tzinfo=timezone.utc)
    
    try:
        clean_str = date_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_str)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        pass

    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
            
    return datetime(1900, 1, 1, tzinfo=timezone.utc)


def load_curated_historical_records() -> List[Dict[str, Any]]:
    """載入歷史典藏底庫 (data/curated_historical.json)。"""
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
    for item_a, item_b in zip(a, b):
        if not isinstance(item_a, dict) or not isinstance(item_b, dict):
            return False
        if json.dumps(item_a, sort_keys=True) != json.dumps(item_b, sort_keys=True):
            return False
    return True


def discover_all_adapters() -> List[BaseAdapter]:
    """
    動態自動發現並實例化 adapters/ 目錄下的所有可用適配器。
    具備沙盒錯誤隔離：任一檔案語法錯誤或缺少依賴均不中斷整體管線。
    """
    discovered: List[BaseAdapter] = []
    adapters_path = Path(adapters.__file__).parent

    print("🔍 啟動動態適配器反射掃描 (Dynamic Discovery)...")

    for _, module_name, _ in pkgutil.iter_modules([str(adapters_path)]):
        if module_name == "base":
            continue

        full_module_name = f"adapters.{module_name}"
        try:
            mod = importlib.import_module(full_module_name)
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                # 必須是 class，繼承自 BaseAdapter，且非 BaseAdapter 本身
                if inspect.isclass(attr) and issubclass(attr, BaseAdapter) and attr is not BaseAdapter:
                    try:
                        # 嘗試無參數或環境變數實例化
                        instance = attr()
                        discovered.append(instance)
                        break  # 一個模組通常註冊一個主 class
                    except TypeError:
                        # 若建構子需特定參數（如 api_key），依序注入環境變數重試
                        try:
                            key = os.environ.get("CONGRESS_API_KEY")
                            instance = attr(api_key=key)
                            discovered.append(instance)
                            break
                        except Exception:
                            continue
        except Exception as exc:
            print(f"  ⚠️ [模組跳過] 無法載入適配器 {module_name}: {exc}", file=sys.stderr)

    print(f"✔ 適配器動態裝載完成，共啟動 {len(discovered)} 個情報適配器。\n")
    return discovered


def atomic_write(target_path: Path, content: bytes) -> None:
    """以暫存檔 + 實體磁碟同步 (fsync) + os.replace 實現安全原子性寫入。"""
    target_dir = target_path.parent
    target_dir.mkdir(parents=True, exist_ok=True)
    fd, tmp_file = tempfile.mkstemp(dir=target_dir, prefix=".tmp_", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_file, target_path)
    except Exception:
        if os.path.exists(tmp_file):
            os.unlink(tmp_file)
        raise


def run_ingestion(days_back: int = 30) -> None:
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

    # 2. 自動掃描裝載所有適配器
    active_adapters = discover_all_adapters()
    api_metrics: Dict[str, Dict[str, Any]] = {}

    # 3. 逐一採集動態增量
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
            print(f"  ✔ [API: {name:<25}] 抓取 {len(fetched)} 筆，新增入庫 {added} 筆")
        except Exception as exc:
            print(f"  ✖ [API: {name:<25}] 採集失敗: {exc}", file=sys.stderr)
            api_metrics[name] = {
                "status": "failed",
                "error": str(exc),
            }

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
                print("\n✔ [冪等生效] 卷宗內容無任何實質異動，跳過覆寫。")
                existing_bytes = out_file.read_bytes()
                correct_hash = hashlib.sha256(existing_bytes).hexdigest()
                sha_file.write_text(f"{correct_hash}  records-latest.json\n", encoding="utf-8")
                return
        except Exception:
            print("⚠️ 既有檔案解析異常，重新全量生成。", file=sys.stderr)

    # 6. 生成新總帳並以原子操作寫入
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
    atomic_write(out_file, json_bytes)

    # 簽署 SHA-256
    sha256_hash = hashlib.sha256(json_bytes).hexdigest()
    atomic_write(sha_file, f"{sha256_hash}  records-latest.json\n".encode("utf-8"))

    print("\n" + "=" * 60)
    print(f"✨ 總帳生成完畢！總卷宗數: {len(all_records)} 筆 (耗時: {duration}s)")
    print(f"📁 主端點: {out_file}")
    print(f"🔐 SHA-256: {sha256_hash}")
    print("=" * 60)


if __name__ == "__main__":
    days = 30
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            print(f"⚠️ 無效天數: '{sys.argv[1]}'，使用預設值 30 天", file=sys.stderr)
    run_ingestion(days_back=days)
