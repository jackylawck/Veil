# The Veil | 揭帷
> **Global Sovereign UAP Disclosure & Official Declassification Ledger**  
> 全球主權防衛與 UAP 官方解密總帳（審計級開源情報生態系）

[![Pages Deployment](https://github.com/jackylawck/veil/actions/workflows/static.yml/badge.svg)](https://github.com/jackylawck/veil/actions/workflows/static.yml)
[![Daily Automated Ingestion](https://github.com/jackylawck/veil/actions/workflows/ingest.yml/badge.svg)](https://github.com/jackylawck/veil/actions/workflows/ingest.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Schema Version](https://img.shields.io/badge/Schema-v2.0.0-emerald.svg)](schemas/record.schema.json)

---

## 🌐 線上端點與站點 (Live Endpoints & Site)

- **審計儀表板 (Live Dashboard)**: [https://jackylawck.github.io/veil/](https://jackylawck.github.io/veil/)
- **主帳資料端點 (Primary JSON Ledger)**: [https://jackylawck.github.io/veil/api/records-latest.json](https://jackylawck.github.io/veil/api/records-latest.json)
- **數位存證雜湊 (SHA-256 Checksum)**: [https://jackylawck.github.io/veil/api/records-latest.json.sha256](https://jackylawck.github.io/veil/api/records-latest.json.sha256)

---

## 📖 專案宗旨 (Mission Statement)

### 繁體中文
**「揭帷 (The Veil)」** 是一個專注於國家主權層級與法定解密情報的審計級開源情報（OSINT）追蹤庫。  
面對社群網絡上的匿名傳聞、未經確證的目擊片段與深偽合成干擾，本專案嚴格遵循**第一級官方可審計標準（Tier-1 Audit Grade）**，僅收錄經由主權政府公告、國會宣誓聽證、法定解密公報（如美國聯邦公報、國家檔案館 NARA、國會圖書館 GovInfo、法國 CNES/GEIPAN）背書之第一手原檔，並提供密碼學 SHA-256 存證，確保所有披露脈絡均可獨立追溯。

### English
**The Veil** is an audit-grade OSINT intelligence ledger tracking sovereign disclosure milestones and official declassified archives regarding Unidentified Anomalous Phenomena (UAP).  
Amidst widespread speculative claims and synthetic media, The Veil enforces strict **Tier-1 Sovereign Evidentiary Standards**. We index solely primary sources—enacted statutes, sworn congressional testimonies, official military gazettes, and national archives (e.g., Federal Register, GovInfo, Congress.gov, NARA, CNES/GEIPAN). Each entry features cryptographic SHA-256 verification to ensure uncompromised auditability.

---

## 🏛️ 架構與核心特徵 (Key Architectural Features)

1. **三維動態採集管道 (Tri-Adapter Dynamic Ingestion)**:
   - `FederalRegisterAdapter`: 每日自動採集聯邦公報最新公告、國防部命令與跨部會 SORN 存檔。
   - `GovInfoAdapter`: 追蹤美國政府出版局（GPO）發布之法定聽證出版物與國會法規 PDF。
   - `CongressAdapter`: 監控眾議院與參議院法案狀態推進（如 NDAA、UAPDA 修正案）。
2. **靜態歷史典藏庫 (Curated Historical Baseline)**:
   - 經版本控制的權威歷史案卷（`data/curated_historical.json`），內建真實二進位 PDF 特徵校驗（Magic Number `%PDF-` 審核）。
3. **內容級別冪等性與自癒簽章 (Idempotent Pipeline & Self-Healing SHA)**:
   - 全內容語意比對，若資料無實質更新則自動跳過寫入，杜絕空 PR 洗版；同時具備 SHA 檔案校正與原子性磁碟寫入（Atomic Disk Writes）。
4. **雙語原生無障礙前端 (Bilingual Modern Frontend)**:
   - 具備 XSS 消毒防護、URL 協議白名單、瀏覽器語系自動偵測（支援香港 `zh-HK` 及 `yue`）、LocalStorage 偏好持久化及時間線過濾。

---

## 🗂️ 專案目錄結構 (Repository Structure)

```text
veil/
├── .github/workflows/
│   ├── static.yml            # GitHub Pages 自動建置、部署與可用性冒煙測試 (Smoke Test)
│   └── ingest.yml            # 每日定時動態採集、去重排序與自動 PR 提交流程
├── adapters/                 # 官方資料源介面模組
│   ├── base.py               # 抽象適配器基礎類別
│   ├── federal_register.py   # 聯邦公報適配器
│   ├── govinfo.py            # GPO 官方文件適配器
│   └── congress.py           # 美國國會 API 適配器
├── data/
│   └── curated_historical.json # 歷史里程碑核心基準庫 (含官方真 Hash)
├── public/
│   ├── index.html            # 繁英雙語互動儀表板前端
│   └── api/
│       ├── records-latest.json        # 全量合併總帳端點
│       └── records-latest.json.sha256 # 總帳 SHA-256 數位簽章
├── schemas/
│   └── record.schema.json    # JSON Schema v2.0.0 規格驗證標準
├── scripts/
│   ├── ingest.py             # 核心採集、整合與輸出主腳本
│   ├── probe_fr.py           # 聯邦公報階梯式診斷與健康探針 (含陽性對照組)
│   └── compute_hashes.py     # 靜態文件與官方原始文本真 Hash 計算工具
├── requirements.txt          # Python 核心依賴
└── README.md                 # 專案雙語文檔

```

---

## 🛠️ 本地開發與手動執行 (Local Setup & Development)

### 1. 安裝環境需求 (Prerequisites)

* Python 3.10+
* Git

```bash
# 複製專案庫
git clone [https://github.com/jackylawck/veil.git](https://github.com/jackylawck/veil.git)
cd veil

# 建立並啟用虛擬環境
python3 -m venv venv
source venv/bin/activate  # Windows 請執行: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

```

### 2. 執行情報採集管線 (Run Pipeline Ingestion)

```bash
# 預設回溯 30 天動態增量並與歷史庫合併生成
python scripts/ingest.py 30

# 若具備 Congress.gov API Key，可注入執行：
CONGRESS_API_KEY="your_api_key" python scripts/ingest.py 30

```

### 3. 執行聯邦公報階梯式診斷 (Run Diagnostic Probe)

```bash
# 執行具備陽性對照（Positive Control）之 API 健康檢查
python scripts/probe_fr.py

```

### 4. 歷史案卷真實 SHA 雜湊審計 (Audit & Verify Hashes)

```bash
# 審計測試模式 (Dry Run)
python scripts/compute_hashes.py

# 正式回寫模式 (原子寫入真雜湊)
python scripts/compute_hashes.py --write

```

---

## 🔒 數據治理與審計標準 (Data Governance & Audit Standards)

| 屬性 (Attribute) | 規範說明 (Specification) |
| --- | --- |
| **證詞與記錄分級** | `evidence_level` 限制為 `official_document`, `testimony_sworn`, `unsworn_claim`, `circumstantial` |
| **案卷類型** | `type` 限制為 `hearing`, `bill`, `report`, `statement`, `foia`, `media` |
| **真實性雜湊** | 實體二進位檔案計算 SHA-256 並標識 `sha256_verified: true`；動態 HTML 頁面嚴格維持 `sha256: null` |
| **管線健全度** | 任一 Adapter 失敗將發送 Telegram / Issue 警報；全動態 Adapter 崩潰立即觸發 Exit 1 阻斷空發布 |

---

## ⚖️ 授權條款 (License)

本專案採用 [MIT License](https://www.google.com/search?q=LICENSE&utm_source=gemini) 開源授權，歡迎各界開源情報研究員、學術機構與資料審計員共同維護與使用。
