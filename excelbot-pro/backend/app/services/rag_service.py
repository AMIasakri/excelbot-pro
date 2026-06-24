"""
🧠 RAG Service - ترکیب جستجو و تولید پاسخ
"""

from typing import List, Dict, Any, Optional
from .embedding_service import EmbeddingService
from .vector_store import VectorStore
from .llm_service import LLMService

class RAGService:
    """
    سرویس RAG (Retrieval-Augmented Generation)
    """
    
    def __init__(self):
        """مقداردهی اولیه همه سرویس‌ها"""
        print("🚀 در حال راه‌اندازی RAG Service...")
        
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore(self.embedding_service)
        self.llm_service = LLMService()
        
        print("✅ RAG Service آماده شد!")
    
    def initialize_from_excel(self, file_path: str):
        """
        مقداردهی اولیه از فایل اکسل
        
        Args:
            file_path: مسیر فایل اکسل
        """
        from ..utils.excel_loader import load_excel_data
        
        print(f"📂 در حال خواندن اکسل از {file_path}...")
        data = load_excel_data(file_path)
        
        if not data:
            print("⚠️ داده‌ای برای بارگذاری وجود ندارد")
            return
        
        # استخراج متن‌ها و متادیتا
        texts = []
        metadatas = []
        
        for record in data:
            # از فیلد _combined_text استفاده کن (که قبلاً ساختیم)
            text = record.get('_combined_text', '')
            
            # متادیتا (همه ستون‌های اصلی)
            metadata = {k: v for k, v in record.items() if not k.startswith('_')}
            
            texts.append(text)
            metadatas.append(metadata)
        
        print(f"📊 {len(texts)} رکورد برای ساخت ایندکس آماده شد")
        
        # ساخت ایندکس
        self.vector_store.create_index(texts, metadatas)
        print("✅ ایندکس ساخته شد!")
    
    def ask(self, query: str, top_k: int = 5, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        پرسش از سیستم RAG
        
        Args:
            query: سوال کاربر
            top_k: تعداد نتایج جستجو
            history: تاریخچه مکالمه
        
        Returns:
            دیکشنری شامل پاسخ و اطلاعات جانبی
        """
        # ۱. جستجوی بردارهای مشابه
        print(f"🔍 جستجو برای: {query}")
        results = self.vector_store.search(query, top_k=top_k)
        
        if not results:
            return {
                "answer": "متاسفم، اطلاعاتی برای پاسخ به این سوال در دانشنامه ما وجود ندارد.",
                "sources": [],
                "confidence": 0.0
            }
        
        # ۲. استخراج متادیتا از نتایج
        context = [meta for meta, _ in results]
        distances = [dist for _, dist in results]
        
        # ۳. تولید پاسخ با LLM
        print(f"🤖 در حال تولید پاسخ...")
        answer = self.llm_service.generate_response(query, context, history)
        
        # ۴. برگرداندن نتیجه
        return {
            "answer": answer,
            "sources": context[:3],  # فقط ۳ منبع برتر
            "confidence": 1.0 - min(distances) / 10  # تبدیل فاصله به درصد (تقریبی)
        }
    
    def reload_from_excel(self, file_path: str):
        """
        بارگذاری مجدد از اکسل (برای به‌روزرسانی)
        """
        self.initialize_from_excel(file_path)


# ============================================================
# 🔧 مهمترین تغییر: تابع شبیه‌سازی با کلیدهای فارسی
# ============================================================

def _simulate_response(self, query: str, context: List[Dict[str, Any]]) -> str:
    """
    حالت شبیه‌سازی (وقتی کلید OpenAI موجود نیست)
    """
    if not context:
        return "متاسفم، اطلاعاتی برای پاسخ به این سوال در دانشنامه ما وجود ندارد."
    
    # ✅ استفاده از کلیدهای فارسی (همون چیزی که تو اکسل داری)
    best_match = context[0]
    
    # اول سعی کن از 'پاسخ' بگیر
    answer = best_match.get('پاسخ', '')
    
    # اگه 'پاسخ' نبود، از 'answer' بگیر (برای سازگاری با داده‌های نمونه)
    if not answer:
        answer = best_match.get('answer', '')
    
    if answer:
        return answer
    
    # اگه هیچ پاسخی نبود، از سوال استفاده کن
    question = best_match.get('سوال', '') or best_match.get('question', '')
    return f"بر اساس اطلاعات موجود: {question} - {answer}"


# ============================================================
# پچ کردن کلاس (اضافه کردن تابع به کلاس)
# ============================================================
RAGService._simulate_response = _simulate_response


# ============================================================
# بخش تست
# ============================================================
if __name__ == "__main__":
    # تست RAG
    rag = RAGService()
    
    # از داده‌های نمونه استفاده کن
    sample_texts = [
        "نحوه ثبت سفارش در فروشگاه اینترنتی",
        "روش بازگشت کالا تا ۷ روز کاری",
        "ساعت کاری پشتیبانی از ۹ صبح تا ۶ عصر",
        "روش پرداخت آنلاین با کارت بانکی"
    ]
    sample_metadatas = [
        {"سوال": "ثبت سفارش", "پاسخ": "به بخش خرید بروید و محصول را انتخاب کنید", "دسته\u200cبندی": "راهنما"},
        {"سوال": "بازگشت کالا", "پاسخ": "تا ۷ روز کاری امکان بازگشت وجود دارد", "دسته\u200cبندی": "پشتیبانی"},
        {"سوال": "ساعت کاری", "پاسخ": "پشتیبانی از ۹ صبح تا ۶ عصر فعال است", "دسته\u200cبندی": "پشتیبانی"},
        {"سوال": "پرداخت", "پاسخ": "پرداخت از طریق درگاه بانکی انجام میشود", "دسته\u200cبندی": "راهنما"}
    ]
    
    # ساخت ایندکس با داده‌های نمونه
    rag.vector_store.create_index(sample_texts, sample_metadatas)
    
    # پرسش
    result = rag.ask("چطور می‌تونم سفارش ثبت کنم؟")
    print(f"\n📝 پاسخ: {result['answer']}")
    print(f"📊 منابع: {result['sources']}")