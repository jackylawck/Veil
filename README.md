# The Veil | 揭帷
> **Global Sovereign UAP Disclosure & Official Declassification Ledger**  
> 全球主權防衛與 UAP 官方解密總帳（審計級開源情報生態系）

[![Pages Deployment](https://github.com/jackylawck/veil/actions/workflows/static.yml/badge.svg)](https://github.com/jackylawck/veil/actions/workflows/static.yml)
[![Daily Automated Ingestion](https://github.com/jackylawck/veil/actions/workflows/ingest.yml/badge.svg)](https://github.com/jackylawck/veil/actions/workflows/ingest.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Schema Version](https://img.shields.io/badge/Schema-v2.0.0-emerald.svg)](schemas/record.schema.json)
[![Compliance: EAR & ITAR](https://img.shields.io/badge/Export%20Control-EAR%20%7C%20ITAR%20Exempt-blue.svg)](GOVERNANCE.md)
[![Privacy: PDPO & GDPR](https://img.shields.io/badge/Privacy-PDPO%20%7C%20GDPR%20Aligned-success.svg)](PRIVACY.md)
[![Security: ISO 27001](https://img.shields.io/badge/Security-ISO%2027001%20Controls-green.svg)](GOVERNANCE.md)

---

## 🌐 線上端點與站點 (Live Endpoints & Site)

- **審計儀表板 (Live Dashboard)**: [https://jackylawck.github.io/veil/](https://jackylawck.github.io/veil/)
- **主帳資料端點 (Primary JSON Ledger)**: [https://jackylawck.github.io/veil/api/records-latest.json](https://jackylawck.github.io/veil/api/records-latest.json)
- **數位存證雜湊 (SHA-256 Checksum)**: [https://jackylawck.github.io/veil/api/records-latest.json.sha256](https://jackylawck.github.io/veil/api/records-latest.json.sha256)

---

## 📖 專案宗旨 (Mission Statement)

### 繁體中文
**「揭帷 (The Veil)」** 是一個專注於國家主權層級與法定解密情報的審計級開源情報（OSINT）追蹤庫。  
面對社群網絡上的匿名傳聞、未經確證的目擊片段與深偽合成干擾，本專案嚴格遵循**第一級官方可審計標準（Tier-1 Audit Grade）**，僅收錄經由主權政府公告、國會宣誓聽證、法定解密公報（如美國聯邦公報、國家檔案館 NARA、國會圖書館 GovInfo、法國 CNES/GEIPAN、英國國家檔案館 TNA 等）背書之第一手原檔，並提供密碼學 SHA-256 存證，確保所有披露脈絡均可獨立追溯。

### English
**The Veil** is an audit-grade OSINT intelligence ledger tracking sovereign disclosure milestones and official declassified archives regarding Unidentified Anomalous Phenomena (UAP).  
Amidst widespread speculative claims and synthetic media, The Veil enforces strict **Tier-1 Sovereign Evidentiary Standards**. We index solely primary sources—enacted statutes, sworn congressional testimonies, official military gazettes, and national archives (e.g., Federal Register, GovInfo, Congress.gov, NARA, CNES/GEIPAN, UK TNA). Each entry features cryptographic SHA-256 verification to ensure uncompromised auditability.

---

## 🏛️ 架構與核心特徵 (Key Architectural Features)

1. **動態發現採集引擎 (Dynamic Discovery Ingestion Engine)**:
   - 具備自動模組反射發現機制（`discover_all_adapters`），動態裝載 `adapters/` 目錄下 60 餘個跨國國防、航天與情資來源。
   - 內建**沙盒錯誤隔離（Sandbox Isolation）**，單一境外機構連線異常或 API 降級時自動記錄警報，確保核心總帳管線零中斷。
2. **密碼學完整性與原子寫入 (Cryptographic Integrity & Atomic Writes)**:
   - 對已下載之靜態二進位 PDF 嚴格校驗 SHA-256（`sha256_verified: true`）；動態網頁嚴格標註為 `null`，杜絕任何偽造雜湊。
   - 採用暫存檔替換與磁碟同步機制（Atomic `os.replace`），杜絕建置中斷造成的 JSON 損毀。
3. **內容級別冪等性 (Semantic Idempotency)**:
   - 全內容語意深層比對，僅在檢測到實質新資料時開啟審查 PR，杜絕無效 PR 干擾審計。
4. **雙語防禦型前端 (Hardened Bilingual Frontend)**:
   - 部署嚴格 Content Security Policy (CSP)、XSS 消毒、URL 協議白名單，支援香港繁體（`zh-HK`/`yue`）與英文動態切換，自適應類型正規化（Normalization）。
5. **企業級合規與治理 (Enterprise Governance Framework)**:
   - 明確主張美國 EAR 15 CFR § 734.7 與 ITAR 22 CFR § 120.34 公開領域豁免，對標 ISO/IEC 42001（無專有模型部署聲明）、ISO/IEC 27001 及香港 PDPO / 歐盟 GDPR。

---

## 🗂️ 專案目錄結構 (Repository Structure)

```text
veil/
├── .github/workflows/
│   ├── static.yml            # GitHub Pages 自動建置、部署與原生 Python 冒煙測試 (Smoke Test)
│   ├── ingest.yml            # 每日定時全適配器動態巡檢、去重排序與自動 PR 提交流程
│   └── probe.yml             # 聯邦公報與核心 API 階梯式診斷巡檢工作流
├── adapters/                 # 全球官方情報適配器模組庫 (60+ Adapters)
│   ├── __init__.py           # 套件識別標識
│   ├── base.py               # 抽象適配器基礎規範 (BaseAdapter)
│   ├── federal_register.py   # 美國聯邦公報適配器
│   ├── congress.py           # 美國國會法案 API 適配器 (Schema v2)
│   ├── govinfo.py            # GPO 聽證出版物適配器
│   ├── geipan.py             # 法國國家太空研究中心 GEIPAN 適配器
│   └── ...                   # 60+ 國防司令部、歷史調查與主權情報來源適配器
├── data/
│   └── curated_historical.json # 歷史里程碑核心基準庫 (含官方真 Hash)
├── public/
│   ├── index.html            # 繁英雙語互動儀表板前端 (含類型正規化引擎)
│   ├── site.webmanifest      # PWA 應用程式清單
│   └── api/
│       ├── records-latest.json        # 全量合併總帳端點 (Schema v2)
│       └── records-latest.json.sha256 # 總帳 SHA-256 數位簽章
├── schemas/
│   └── record.schema.json    # JSON Schema v2.0.0 規格驗證標準
├── scripts/
│   ├── ingest.py             # 核心採集、動態適配器反射裝載與輸出主腳本
│   ├── probe_fr.py           # 聯邦公報階梯式診斷與健康探針
│   └── compute_hashes.py     # 靜態文件與官方原始文本真 Hash 計算工具
├── GOVERNANCE.md             # 全球法規遵從、出口管制與 AI 治理框架聲明
├── PRIVACY.md                # 個人資料保護、去識別化與隱私權合規政策
├── requirements.txt          # Python 核心依賴
└── README.md                 # 專案主文檔

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
# 動態掃描載入全數適配器並生成最新總帳
python scripts/ingest.py 30

# 若具備 Congress.gov API Key，可注入執行以抓取深層法案動態：
CONGRESS_API_KEY="your_api_key" python scripts/ingest.py 30

```

### 3. 執行聯邦公報健康探針 (Run Diagnostic Probe)

```bash
# 執行 API 探針檢測
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
| **證據位階 (Evidence Level)** | 限制為 `official_document`, `testimony_sworn`, `unsworn_claim`, `circumstantial` |
| **卷宗類型 (Record Types)** | 對齊 Schema v2.0.0：`hearing`, `bill`, `report`, `statement`, `foia`, `media` |
| **密碼學存證 (Verification)** | 實體二進位原檔強制校驗 SHA-256；動態 HTML 維持 `sha256: null` 杜絕偽造 |
| **出口管制 (Export Controls)** | 符合美國 EAR 15 CFR § 734.7 及 ITAR 22 CFR § 120.34 公開出版物豁免 |
| **管線健全度 (Resilience)** | 單一適配器失敗採沙盒降級隔離；全部適配器異常則觸發 Exit 1 阻斷發布 |

---

## 📜 治理文檔索引 (Governance Documentation)

* **綜合治理與出口管制框架**: 參見 [`GOVERNANCE.md`](https://www.google.com/search?q=GOVERNANCE.md&utm_source=gemini)
* **個人資料與隱私保護政策**: 參見 [`PRIVACY.md`](PRIVACY.md)

---

## ⚖️ 授權條款 (License)

本專案採用 [MIT License](https://github.com/jackylawck/veil/blob/main/LICENSE) 開源授權，歡迎各界開源情報研究員、學術機構與資料審計員共同維護與使用。

