"""
📋 Schemas - مدل‌های داده برای API
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ChatRequest(BaseModel):
    """
    مدل درخواست چت
    """
    query: str  # سوال کاربر
    history: Optional[List[Dict[str, str]]] = None  # تاریخچه مکالمه
    top_k: Optional[int] = 5  # تعداد نتایج جستجو

class ChatResponse(BaseModel):
    """
    مدل پاسخ چت
    """
    answer: str  # پاسخ تولید شده
    sources: List[Dict[str, Any]]  # منابع استفاده شده
    confidence: float  # درصد اطمینان

class HealthResponse(BaseModel):
    """
    مدل پاسخ سلامت سیستم
    """
    status: str
    total_records: int
    embedding_dim: int