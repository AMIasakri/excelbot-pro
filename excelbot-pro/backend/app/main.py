"""
🚀 Main Application - نقطه ورود اصلی برنامه
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat
from .services.rag_service import RAGService
import os

# ساخت اپلیکیشن FastAPI
app = FastAPI(
    title="ExcelBot Pro",
    description="چت‌بات پشتیبانی هوشمند با استفاده از RAG و FAISS",
    version="1.0.0"
)

# تنظیم CORS (برای ارتباط با ویجت چت)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در محیط تولید، دامنه خودت رو بذار
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ثبت روت‌ها
app.include_router(chat.router, prefix="/api", tags=["Chat"])

# راه‌اندازی اولیه RAG (در صورت وجود اکسل)
@app.on_event("startup")
async def startup_event():
    """اجرا در زمان شروع سرور"""
    print("🚀 سرور در حال راه‌اندازی...")
    
    # بررسی وجود فایل اکسل و بارگذاری اولیه
    excel_path = "data/data.xlsx"
    if os.path.exists(excel_path):
        print(f"📂 بارگذاری اکسل از {excel_path}...")
        try:
            rag = RAGService()
            rag.initialize_from_excel(excel_path)
            print("✅ داده‌ها با موفقیت بارگذاری شدند")
        except Exception as e:
            print(f"⚠️ خطا در بارگذاری اکسل: {e}")
    else:
        print(f"ℹ️ فایل اکسل در {excel_path} یافت نشد")
        print("ℹ️ لطفاً فایل data.xlsx را در پوشه data/ قرار دهید")

@app.get("/")
async def root():
    """صفحه اصلی"""
    return {
        "message": "ExcelBot Pro API",
        "docs": "/docs",
        "health": "/api/health"
    }

# برای اجرای مستقیم
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )