"""
🤖 LLM Service - ارتباط با مدل زبانی (OpenAI / DeepSeek / ...)
"""

import openai
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

class LLMService:
    """
    سرویس ارتباط با APIهای مختلف (OpenAI، DeepSeek، و...)
    """
    
    def __init__(self):
        """مقداردهی اولیه با متغیرهای محیطی"""
        # خواندن تنظیمات از فایل .env
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        self.base_url = os.getenv("OPENAI_BASE_URL")  # آدرس دلخواه برای API
        
        # اگر کلید وجود نداشت یا مقدار پیش‌فرض بود، برو به حالت شبیه‌سازی
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("⚠️ هشدار: OPENAI_API_KEY در فایل .env تنظیم نشده!")
            print("ℹ️ برای تست می‌توانید از حالت simulated استفاده کنید")
            self.simulated = True
        else:
            self.simulated = False
            try:
                # ساخت کلاینت با آدرس base_url (در صورت وجود)
                self.client = openai.OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url if self.base_url else None
                )
                print(f"✅ مدل {self.model} از مسیر {self.base_url or 'OpenAI'} آماده شد")
            except Exception as e:
                print(f"❌ خطا در راه‌اندازی کلاینت: {e}")
                self.simulated = True
    
    def generate_response(
        self, 
        query: str, 
        context: List[Dict[str, Any]], 
        history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        تولید پاسخ بر اساس سوال و زمینه (Context)
        
        Args:
            query: سوال کاربر
            context: لیست نتایج جستجو از پایگاه برداری
            history: تاریخچه مکالمه (اختیاری)
        
        Returns:
            پاسخ تولید شده
        """
        # اگر حالت simulated فعال باشه
        if self.simulated:
            return self._simulate_response(query, context)
        
        # ساخت پرامپت (Prompt)
        prompt = self._build_prompt(query, context, history)
        
        try:
            # ارسال درخواست به API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "شما یک دستیار پشتیبانی هوشمند هستید. فقط بر اساس اطلاعات داده شده پاسخ دهید. اگر اطلاعات کافی ندارید، بگویید 'متاسفم، این سوال در دانشنامه ما موجود نیست'."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ خطا در ارتباط با API: {e}")
            # در صورت خطا، به حالت simulated برگرد
            return self._simulate_response(query, context)
    
    def _build_prompt(
        self, 
        query: str, 
        context: List[Dict[str, Any]], 
        history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        ساخت پرامپت کامل با زمینه و تاریخچه
        """
        # بخش تاریخچه (اگر وجود داشته باشد)
        history_text = ""
        if history:
            history_text = "\nتاریخچه مکالمه:\n"
            for msg in history[-5:]:  # فقط ۵ پیام آخر
                role = "کاربر" if msg.get("role") == "user" else "دستیار"
                history_text += f"{role}: {msg.get('content', '')}\n"
        
        # بخش زمینه (Context) - با پشتیبانی از کلیدهای فارسی و انگلیسی
        context_text = "\nاطلاعات مرتبط از دانشنامه:\n"
        for i, item in enumerate(context, 1):
            # تلاش برای پیدا کردن کلیدهای مختلف
            question = item.get('سوال', '') or item.get('question', '')
            answer = item.get('پاسخ', '') or item.get('answer', '')
            category = item.get('دسته\u200cبندی', '') or item.get('category', '')
            
            context_text += f"{i}. سوال: {question}\n"
            context_text += f"   پاسخ: {answer}\n"
            if category:
                context_text += f"   دسته‌بندی: {category}\n"
            context_text += "\n"
        
        # پرامپت نهایی
        prompt = f"""
سوال کاربر: {query}
{history_text}
{context_text}
لطفاً بر اساس اطلاعات بالا، پاسخی دقیق و مفید به کاربر بدهید.
اگر اطلاعات کافی نیست، صادقانه بگویید.
پاسخ باید مختصر، حرفه‌ای و مفید باشد.
"""
        return prompt
    
    def _simulate_response(self, query: str, context: List[Dict[str, Any]]) -> str:
        """
        حالت شبیه‌سازی (وقتی کلید API موجود نیست یا خطا رخ می‌دهد)
        """
        if not context:
            return "متاسفم، اطلاعاتی برای پاسخ به این سوال در دانشنامه ما وجود ندارد."
        
        # بهترین نتیجه رو پیدا کن (نزدیک‌ترین فاصله)
        best_match = context[0]
        
        # تلاش برای پیدا کردن پاسخ با کلیدهای مختلف
        answer = best_match.get('پاسخ', '') or best_match.get('answer', '')
        
        if answer:
            return answer
        
        # اگه هیچ پاسخی نبود، از سوال استفاده کن
        question = best_match.get('سوال', '') or best_match.get('question', '')
        return f"بر اساس اطلاعات موجود: {question}"


# بخش تست (اختیاری)
if __name__ == "__main__":
    print("🧪 تست LLM Service...")
    service = LLMService()
    
    # داده‌های تست
    test_context = [
        {"سوال": "ساعت کاری", "پاسخ": "۹ صبح تا ۶ عصر", "دسته\u200cبندی": "پشتیبانی"}
    ]
    
    response = service.generate_response(
        query="ساعت کاری چنده؟",
        context=test_context
    )
    
    print(f"📝 پاسخ: {response}")