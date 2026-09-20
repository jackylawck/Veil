# scripts/ingest.py
import os
import sys
import json
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any

# 加入專案根目錄至 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 匯入全部 65 個官方與權威適配器
from adapters.federal_register import FederalRegisterAdapter
from adapters.congress import CongressAdapter
from adapters.govinfo import GovInfoAdapter
from adapters.nara import NaraAdapter
from adapters.dvids import DvidsAdapter
from adapters.nasa import NasaAdapter
from adapters.odni import OdniAdapter
from adapters.tna import TnaAdapter
from adapters.lac import LacAdapter
from adapters.naa import NaaAdapter
from adapters.nzdf import NzdfAdapter
from adapters.norad import NoradAdapter
from adapters.un import UnAdapter
from adapters.icao import IcaoAdapter
from adapters.geipan import GeipanAdapter
from adapters.ejercito_aire import EjercitoAireAdapter
from adapters.aeronautica_militare import AeronauticaMilitareAdapter
from adapters.belgian_air_component import BelgianAirComponentAdapter
from adapters.nas_ukraine import NasUkraineAdapter
from adapters.finnish_defence import FinnishDefenceAdapter
from adapters.sweden_ghost_rockets import SwedenGhostRocketsAdapter
from adapters.fap_portugal import FapPortugalAdapter
from adapters.irish_df import IrishDfAdapter
from adapters.rnlaf_netherlands import RnlafNetherlandsAdapter
from adapters.hessdalen_ffi import HessdalenFfiAdapter
from adapters.an_brazil import AnBrazilAdapter
from adapters.cefaa import CefaaAdapter
from adapters.cridovni import CridovniAdapter
from adapters.ciaa_argentina import CiaaArgentinaAdapter
from adapters.difaa_peru import DifaaPeruAdapter
from adapters.ceifo_ecuador import CeifoEcuadorAdapter
from adapters.aerocivil_colombia import AerocivilColombiaAdapter
from adapters.sedena_mexico import SedenaMexicoAdapter
from adapters.antarctica_decepcion import AntarcticaDecepcionAdapter
from adapters.antarctica_nsf import AntarcticaNsfAdapter
from adapters.mod_japan import ModJapanAdapter
from adapters.pla_air_situation import PlaAirSituationAdapter
from adapters.cangzhou_intercept import CangzhouInterceptAdapter
from adapters.russia_grid import RussiaGridAdapter
from adapters.iriaf_tehran import IriafTehranAdapter
from adapters.saaf_south_africa import SaafSouthAfricaAdapter
from adapters.rendlesham_halt import RendleshamHaltAdapter
from adapters.af3532_sepra import Af3532SepraAdapter
from adapters.malmstrom_nuclear import MalmstromNuclearAdapter
from adapters.cometa_france import CometaFranceAdapter
from adapters.canada_hellyer import CanadaHellyerAdapter
from adapters.church_committee import ChurchCommitteeAdapter
from adapters.house_uap_nov2024 import HouseUapNov2024Adapter
from adapters.immaculate_constellation import ImmaculateConstellationAdapter
from adapters.dod_oig_eval import DodOigEvalAdapter
from adapters.senate_sasc_uap import SenateSascUapAdapter
from adapters.senate_uapda import SenateUapdaAdapter
from adapters.aaro_historical_report import AaroHistoricalReportAdapter
from adapters.dhs_kona_blue import DhsKonaBlueAdapter
from adapters.sol_karl_nell import SolKarlNellAdapter
from adapters.aaro_historical_vol2 import AaroHistoricalVol2Adapter
from adapters.odni_annual_update import OdniAnnualUpdateAdapter
from adapters.nara_records_collection import NaraRecordsCollectionAdapter
from adapters.aaro_secure_portal import AaroSecurePortalAdapter
from adapters.icig_whistleblower import IcigWhistleblowerAdapter
from adapters.gao_defense_sap import GaoDefenseSapAdapter
from adapters.aaro_annual_report import AaroAnnualReportAdapter
from adapters.doe_nuclear_labs import DoeNuclearLabsAdapter
from adapters.faa_atc_mandatory import FaaAtcMandatoryAdapter
from adapters.nasa_uap_science import NasaUapScienceAdapter
from adapters.cas_fast_seti import CasFastSetiAdapter
from adapters.un_iaa_post_detection import UnIaaPostDetectionAdapter

# 註冊所有適配器清單 (共 67 個模組實例，全主權覆蓋)
ALL_ADAPTERS = [
    FederalRegisterAdapter, CongressAdapter, GovInfoAdapter, NaraAdapter,
    DvidsAdapter, NasaAdapter, OdniAdapter, TnaAdapter, LacAdapter, NaaAdapter,
    NzdfAdapter, NoradAdapter, UnAdapter, IcaoAdapter, GeipanAdapter,
    EjercitoAireAdapter, AeronauticaMilitareAdapter, BelgianAirComponentAdapter,
    NasUkraineAdapter, FinnishDefenceAdapter, SwedenGhostRocketsAdapter,
    FapPortugalAdapter, IrishDfAdapter, RnlafNetherlandsAdapter, HessdalenFfiAdapter,
    AnBrazilAdapter, CefaaAdapter, CridovniAdapter, CiaaArgentinaAdapter,
    DifaaPeruAdapter, CeifoEcuadorAdapter, AerocivilColombiaAdapter, SedenaMexicoAdapter,
    AntarcticaDecepcionAdapter, AntarcticaNsfAdapter, ModJapanAdapter,
    PlaAirSituationAdapter, CangzhouInterceptAdapter, RussiaGridAdapter,
    IriafTehranAdapter, SaafSouthAfricaAdapter, RendleshamHaltAdapter, Af3532SepraAdapter,
    MalmstromNuclearAdapter, CometaFranceAdapter, CanadaHellyerAdapter,
    ChurchCommitteeAdapter, HouseUapNov2024Adapter, ImmaculateConstellationAdapter,
    DodOigEvalAdapter, SenateSascUapAdapter, SenateUapdaAdapter,
    AaroHistoricalReportAdapter, DhsKonaBlueAdapter, SolKarlNellAdapter,
    AaroHistoricalVol2Adapter, OdniAnnualUpdateAdapter, NaraRecordsCollectionAdapter,
    AaroSecurePortalAdapter, IcigWhistleblowerAdapter, GaoDefenseSapAdapter,
    AaroAnnualReportAdapter, DoeNuclearLabsAdapter, FaaAtcMandatoryAdapter,
    NasaUapScienceAdapter, CasFastSetiAdapter, UnIaaPostDetectionAdapter
]

def run_ingestion(days_back: int = 36500) -> None:
    """
    執行全量資料攝入
    預設 days_back=36500 (100 年)，徹底解除 365 天的時間截斷限制，
    確保冷戰以降至當代所有里程碑與解密案卷全數完整保留入庫。
    """
    print(f"[{datetime.now(timezone.utc).isoformat()}] 啟動全量情報攝入 (時間窗口: {days_back} 日 / 全歷史覆蓋)...")
    
    all_records: List[Dict[str, Any]] = []
    seen_ids = set()
    adapter_stats = {}

    for adapter_cls in ALL_ADAPTERS:
        try:
            adapter = adapter_cls()
            # 傳入 36500 天，保證歷史文件不被遺漏
            records = adapter.fetch_records(days_back=days_back)
            added_count = 0
            for r in records:
                r_id = r.get("id")
                if r_id and r_id not in seen_ids:
                    seen_ids.add(r_id)
                    all_records.append(r)
                    added_count += 1
            adapter_stats[adapter.source_name] = added_count
            print(f"  ✔ [{adapter.source_name:<28}] 成功載入 {added_count} 筆記錄")
        except Exception as e:
            print(f"  ✖ [{adapter_cls.__name__:<28}] 執行失敗: {e}", file=sys.stderr)

    # 依照事件日期降序排序 (最新在最前，歷史在後)
    all_records.sort(
        key=lambda x: x.get("date", {}).get("val", "1900-01-01"),
        reverse=True
    )

    # 構建 Ledger 主輸出結構
    output_data = {
        "metadata": {
            "title": "The Veil - Global Declassified & Sovereign UAP Intelligence Ledger",
            "zh_title": "揭帷 - 全球主權防衛與官方解密情報總帳",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_records": len(all_records),
            "adapters_active": len(ALL_ADAPTERS),
            "ingestion_policy": "full_historical_retention_unrestricted",
            "retention_window_days": days_back
        },
        "records": all_records
    }

    # 確保輸出路徑存在
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public", "api"))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "records-latest.json")
    sha_file = os.path.join(out_dir, "records-latest.json.sha256")

    # 寫入 JSON 主檔
    json_bytes = json.dumps(output_data, ensure_ascii=False, indent=2).encode("utf-8")
    with open(out_file, "wb") as f:
        f.write(json_bytes)

    # 計算並寫入 SHA-256 審計校驗碼
    sha256_hash = hashlib.sha256(json_bytes).hexdigest()
    with open(sha_file, "w", encoding="utf-8") as f:
        f.write(f"{sha256_hash}  records-latest.json\n")

    print("\n" + "=" * 60)
    print(f" 數據入庫完成！總記錄數: {len(all_records)} 筆")
    print(f" 主端點生成: {out_file}")
    print(f" SHA-256 驗證: {sha256_hash}")
    print("=" * 60)

if __name__ == "__main__":
    # 支援命令列指定天數，預設 36500 (100 年) 全歷史載入
    days = 36500
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            pass
    run_ingestion(days_back=days)
