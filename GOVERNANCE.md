# Comprehensive Governance, Compliance & Export Control Statement
# 全球法規遵從、出口管制與系統治理框架聲明

**Document Identifier / 文件編號**: GOV-VEIL-2026-V1  
**Classification / 安全分級**: Public / Audit-Grade Open Information (一級公開審計資訊)  
**Effective Date / 生效日期**: 2026-09-21  
**Framework Alignment / 對標框架**: ISO/IEC 42001:2023, ISO/IEC 27001:2022, ISO/IEC 27701:2019, US EAR/ITAR, HK Cap. 60

---

## 1. Executive Summary & Project Nature / 項目本質與架構定位

### [English]
**The Veil (揭帷)** is an audit-grade, deterministic Open Source Intelligence (OSINT) indexer and sovereign declassification ledger. The system aggregates, validates cryptographic checksums (SHA-256), and indexes publicly released, declassified government records, statutory gazettes, and legislative hearing artifacts. 

- **Autonomous Determinism**: The core architecture relies strictly on automated retrieval scripts (Python standard libraries, deterministic REST API consumers) and cryptographic hashing algorithms.
- **Exclusion of Proprietary AI Models**: The project does not train, fine-tune, deploy, or host proprietary Machine Learning (ML), Deep Learning (DL), or autonomous generative models. 

### [繁體中文]
**「揭帷 (The Veil)」** 為一審計級確定性開源情報（OSINT）索引與主權解密公報總帳系統。本專案僅針對主權政府法定解密之公開紀錄、國會議事筆錄及憲報公報進行元數據彙總與密碼學 SHA-256 數位簽章存證。

- **確定性架構**：本系統完全基於確定性之 Python 自動化擷取腳本與標準雜湊演算法。
- **排除專有 AI 模型**：本專案不涉及任何專有機器學習（ML）、深度學習（DL）或自主生成式 AI 模型之訓練、微調、託管或部署。

---

## 2. Artificial Intelligence Governance (ISO/IEC 42001 & EU AI Act) / AI 治理與監管適用性

### [English]
1. **EU Artificial Intelligence Act (Regulation (EU) 2024/1689)**:
   - *Inapplicability*: The Veil is neither a "high-risk AI system" under Annex III nor a "General Purpose AI (GPAI) Model" under Chapter V. It does not perform profiling, biometric identification, critical infrastructure management, or automated decision-making.
   - *Transparency (Art. 50)*: Even where external automated discovery is deployed, all outputs consist solely of raw sovereign metadata accompanied by original source URLs and cryptographic hashes.
2. **ISO/IEC 42001:2023 (Artificial Intelligence Management System - AIMS)**:
   - *Scope Limitation*: Because no predictive or synthetic models operate within this repository, AIMS controls regarding algorithmic drift, bias training, and model explainability are declared **Out of Scope (不適用 / 免除審計)**. Data integrity controls are aligned under ISO/IEC 27001:2022.

### [繁體中文]
1. **歐盟《人工智慧法案》(EU AI Act - Regulation (EU) 2024/1689)**：
   - **不適用性判定**：本系統非 Annex III 界定之高風險 AI 系統，亦非第五章所指之通用 AI（GPAI）模型。系統不執行特徵畫像、生物辨識、關鍵基礎設施調度或具法律效力之自動化決策。
   - **透明度聲明**：系統所輸出之所有卷宗均完整附帶原始主權來源鏈接與 SHA-256 驗證指紋，確保原始溯源透明度。
2. **ISO/IEC 42001:2023（人工智慧管理體系）**：
   - **範疇界定**：本專案無自主預測或合成算法，ISO 42001 中關於模型偏差、特徵工程與算法漂移之控制項列為**「不適用（Out of Scope）」**；其餘數據完整性控制對標 ISO 27001 實施。

---

## 3. Strategic Export Controls & Dual-Use Compliance (EAR, ITAR, HK Cap. 60) / 戰略物資、軍民兩用與出口管制

### [English]
1. **United States Export Administration Regulations (EAR) - 15 CFR § 734.7**:
   - All materials indexed herein are "Published" and available to the public without restrictions upon its further dissemination. Pursuant to 15 CFR § 734.7(a)(1)-(4), these declassified publications are **not subject to the EAR**.
2. **International Traffic in Arms Regulations (ITAR) - 22 CFR § 120.34**:
   - Information cataloged in this ledger is strictly limited to records in the "Public Domain" (22 CFR § 120.34(a)), including official government publications, open-access congressional archives, and sovereign gazettes. No defense services or technical data subject to ITAR are generated or transferred.
3. **Hong Kong Strategic Commodities Regulations (Import and Export Ordinance, Cap. 60)**:
   - The ledger does not export, import, or re-export articles specified in Schedule 1 to the Import and Export (Strategic Commodities) Regulations. Information made available is purely open-source scholarly and public legal metadata.

### [繁體中文]
1. **美國出口管制條例 (EAR - 15 CFR § 734.7)**：
   - 本總帳所索引之資料均屬已由法定機關「公開發布（Published）」之文檔。依據 15 CFR § 734.7 之規定，向公眾無限制傳播之解密公開出版物**不受 EAR 限制**。
2. **國際武器貿易條例 (ITAR - 22 CFR § 120.34)**：
   - 本專案收錄之所有紀錄均嚴格屬於「公共領域（Public Domain）」（22 CFR § 120.34(a)），包括官方出版物、各國國會公開筆錄及國家解密檔案。本專案不製造、持有或轉讓任何受 ITAR 監管之國防物資或技術數據。
3. **香港《進出口（戰略物品）規例》（香港法例第 60 章）**：
   - 本總帳不涉及香港附表 1 所列之任何戰略物品、雙重用途物資或敏感科技軟體之實體或未授權電子轉移。本專案發布之內容僅限公共學術與法定開源情資。

---

## 4. Information Security & Cryptographic Verifiability (ISO/IEC 27001:2022) / 資訊安全與密碼學驗證

### [English]
The platform enforces ISO/IEC 27001:2022 Controls (A.8.7, A.8.9, A.8.15):
- **Cryptographic Evidence Baseline**: Declassified PDFs and static artifacts are fingerprinted with SHA-256. Dynamic web representations are explicitly marked with `"sha256": null` and `"sha256_verified": false` to prevent falsification of cryptographically non-reproducible states.
- **Tamper Evident Auditability**: Pipeline execution, state updates, and schema migrations are tracked under immutable Git commit histories with signed automated pull requests.
- **CI/CD Hardening**: Workflows enforce `set -euo pipefail`, sandbox dynamic module discovery, eliminate secret leaks into static distributions (`public/`), and run automated smoke tests.

### [繁體中文]
本系統落實 ISO/IEC 27001:2022 安全控制措施（A.8.7、A.8.9、A.8.15）：
- **密碼學存證基準**：靜態解密原檔採用 SHA-256 進行唯一指紋校驗。動態 HTML 頁面嚴格標記為 `"sha256": null` 與 `"sha256_verified": false`，杜絕任何偽造雜湊之審計瑕疵。
- **防篡改審計性**：所有增量、歷史變更與 Schema 演進皆記錄於 Git 不可變提交日誌中，並透過 PR 機制進行人工簽核。
- **CI/CD 安全防護**：自動化工作流全面啟用嚴格錯誤阻斷、動態模組沙盒隔離，防止憑證洩露至靜態發布端點，並具備自動化站點探測（Smoke Test）。

---

## 5. Sovereign & Legal Disclaimers / 主權免責與法律聲明

### [English]
- **No Official Endorsement**: The compilation of records does not constitute official endorsement by the sovereign entities referenced (e.g., US DoD, AARO, NASA, GEIPAN, MOD Japan).
- **Secondary Research Use**: The ledger is provided strictly for academic, research, journalistic, and public accountability purposes on an "AS IS" and "AS AVAILABLE" basis without warranties of merchantability or fitness for a particular purpose.

### [繁體中文]
- **無官方代表性**：本專案對官方解密文檔之索引，不代表各主權機關（如美國國防部、AARO、NASA、法國 GEIPAN、日本防衛省等）之官方背書或隸屬關係。
- **研究與公共目的**：本總帳嚴格依據「現狀（AS IS）」與「現有（AS AVAILABLE）」基礎提供，僅供學術研究、公開情報校驗與公共資訊檢索之用。
