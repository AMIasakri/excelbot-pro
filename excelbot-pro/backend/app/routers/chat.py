"""
🛤️ Chat Router - مسیرهای مربوط به چت
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..models.schemas import ChatRequest, ChatResponse, HealthResponse
from ..services.rag_service import RAGService

# ایجاد router
router = APIRouter()

# ایجاد نمونه از RAG Service (یکبار در طول اجرا)
rag_service = RAGService()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    دریافت سوال کاربر و بازگرداندن پاسخ
    
    Args:
        request: درخواست شامل سوال و تاریخچه
    
    Returns:
        پاسخ تولید شده با منابع
    """
    try:
        # بررسی اینکه ایندکس ساخته شده یا نه
        if rag_service.vector_store.get_total_count() == 0:
            raise HTTPException(
                status_code=503,
                detail="پایگاه داده هنوز مقداردهی نشده است. لطفاً ابتدا اکسل را بارگذاری کنید."
            )
        
        # دریافت پاسخ از RAG
        result = rag_service.ask(
            query=request.query,
            top_k=request.top_k or 5,
            history=request.history
        )
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"]
        )
        
    except Exception as e:
        print(f"❌ خطا در پردازش درخواست: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    بررسی سلامت سیستم
    """
    total = rag_service.vector_store.get_total_count()
    dim = rag_service.embedding_service.embedding_dim
    
    return HealthResponse(
        status="healthy" if total > 0 else "no_data",
        total_records=total,
        embedding_dim=dim
    )

@router.post("/reload")
async def reload_data():
    """
    بارگذاری مجدد داده‌ها از اکسل (برای به‌روزرسانی)
    """
    try:
        # اینجا باید مسیر فایل اکسل رو مشخص کنی
        file_path = "data/data.xlsx"
        rag_service.initialize_from_excel(file_path)
        return {"status": "success", "message": "داده‌ها با موفقیت بارگذاری شدند"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))