# Privacy & Personal Data Protection Policy
# 個人資料保護與隱私權合規聲明

**Document Identifier / 文件編號**: PRIV-VEIL-2026-V1  
**Legal Jurisdictions / 適用法域**: Hong Kong PDPO (Cap. 486), EU GDPR (Regulation (EU) 2016/679), PRC PIPL  
**Standard Alignment / 對標標準**: ISO/IEC 27701:2019 (PIMS)

---

## 1. Regulatory Scope & Basis / 法規範疇與法律依據

### [English]
**The Veil** does not collect, process, or sell personal consumer data. Data present in this repository is strictly restricted to sovereign declassification records, congressional testimonies, and official administrative publications.

1. **Hong Kong Personal Data (Privacy) Ordinance (Cap. 486) - PDPO**:
   - *Public Domain Exclusion*: Personal names appearing in this ledger (e.g., government witnesses, military pilots, public officials) are derived exclusively from declassified government registers, official gazettes, and public legislative proceedings.
   - *Data Protection Principle 3 (Use)*: Publication is consistent with the statutory and public purpose for which the information was made available by sovereign authorities.
2. **European Union General Data Protection Regulation (GDPR - Regulation (EU) 2016/679)**:
   - *Lawful Basis (Article 6(1)(f))*: The processing of names and public titles is based on the legitimate interest of sovereign transparency, academic archiving, and freedom of information.
   - *Article 17 (Right to Erasure)*: Public record archives maintained for historical research purposes and public accountability are protected under Article 17(3)(d).

### [繁體中文]
**「揭帷 (The Veil)」** 不主動收集、分析或販售任何個人用戶資料。本系統收錄之所有內容僅限於各國主權解密公報、國會宣誓證詞及法定公開行政紀錄。

1. **香港《個人資料（私隱）條例》（第 486 章 - PDPO）**：
   - **公共領域豁免**：卷宗中所提及之人員姓名與職稱（如宣誓證人、軍方飛行員、政府官員）均完整取材自主權機關已解密之憲報、司法或立法公開聽證紀錄。
   - **保障資料原則第 3 原則**：本專案之索引與研究用途，與各國主管當局最初依法公開該等資訊之法定目的一致。
2. **歐盟《通用數據保護條例》（GDPR - Regulation (EU) 2016/679）**：
   - **合法處理基礎（第 6(1)(f) 條）**：系統收錄公開公職人員與聽證名冊之行為，基於維護歷史情報真實性、公共知情權及學術研究之「合法利益」。
   - **被遺忘權之例外（第 17(3)(d) 條）**：為公共利益或歷史研究目的建立之檔案，不受一般被遺忘權請求之刪除限制。

---

## 2. ISO/IEC 27701:2019 Privacy Information Management System (PIMS) / 隱私資訊管理架構

### [English]
- **Data Minimization**: Personal identifiable information (PII) of private citizens unintentionally contained in unredacted third-party reports is excluded or anonymized at the ingestion layer.
- **Client-Side Storage**: The web dashboard stores only the user's localized interface language preferences (`veil_lang`) within the user's local browser storage (`localStorage`). No tracking pixels, cookies, or telemetry analytics are deployed.
- **Zero Third-Party Data Transmission**: Ingestion and build pipelines execute in ephemeral, hardened runner environments without transmitting personal data to third-party ad networks or tracking servers.

### [繁體中文]
- **資料最小化原則**：若第三方未妥善遮蔽之非公眾人物敏感個人資料，採集層一律主動進行去識別化或排除收錄。
- **純本地客戶端暫存**：前端儀表板僅在使用者瀏覽器本地（`localStorage`）暫存語言介面偏好（`veil_lang`），全站無任何第三方追蹤 Cookie、行銷代碼或行為分析 SDK。
- **零第三方數據外洩**：自動化建構管線於隔離之虛擬環境中運行，絕不向任何外部廣告或數據代理商傳輸資訊。

---

## 3. Data Subject Rights & Notice / 當事人權利行使與通報管道

### [English]
If any declassified material inadvertently contains non-public personal information or violates statutory privacy safeguards, affected parties may submit a formal redaction request via GitHub Issues with the label `privacy-redaction`. Verified requests will be processed promptly in compliance with international data privacy standards.

### [繁體中文]
若任何已解密原檔非故意包含未公開之平民個人私隱資訊，當事人或其法定代表可透過 GitHub Issues 提交標註為 `privacy-redaction` 之審查請求。經核實後，本專案將依照國際隱私保護標準迅速實施遮蔽或移除。
