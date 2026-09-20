# adapters/base.py
import abc
import hashlib
from typing import Any, Dict, List


class BaseAdapter(abc.ABC):
    """所有情報數據來源必須繼承的基類"""

    @property
    @abc.abstractmethod
    def source_name(self) -> str:
        """回傳來源識別名稱，如 'federal_register'"""
        pass

    @abc.abstractmethod
    def fetch_records(self) -> List[Dict[str, Any]]:
        """執行抓取並回傳標準化後的紀錄清單"""
        pass

    @staticmethod
    def calculate_sha256(content: str) -> str:
        """計算字串的 SHA256 指紋"""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
