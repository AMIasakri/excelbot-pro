from app.services.rag_service import RAGService

# راه‌اندازی RAG
rag = RAGService()

# داده‌های نمونه
sample_texts = [
    "نحوه ثبت سفارش در فروشگاه اینترنتی",
    "روش بازگشت کالا تا ۷ روز کاری",
    "ساعت کاری پشتیبانی از ۹ صبح تا ۶ عصر",
    "روش پرداخت آنلاین با کارت بانکی"
]
sample_metadatas = [
    {"question": "ثبت سفارش", "answer": "به بخش خرید بروید و محصول را انتخاب کنید", "category": "راهنما"},
    {"question": "بازگشت کالا", "answer": "تا ۷ روز کاری امکان بازگشت وجود دارد", "category": "پشتیبانی"},
    {"question": "ساعت کاری", "answer": "پشتیبانی از ۹ صبح تا ۶ عصر فعال است", "category": "پشتیبانی"},
    {"question": "پرداخت", "answer": "پرداخت از طریق درگاه بانکی انجام میشود", "category": "راهنما"}
]

# ساخت ایندکس
print("=" * 50)
print("🔄 ساخت ایندکس با داده‌های نمونه...")
rag.vector_store.create_index(sample_texts, sample_metadatas)

# پرسش‌ها
queries = [
    "چطور سفارش ثبت کنم؟",
    "چند روز وقت دارم کالا رو برگردونم؟",
    "ساعت کارتون چنده؟"
]

print("\n" + "=" * 50)
print("💬 شروع پرسش و پاسخ...")
print("=" * 50)

for query in queries:
    print(f"\n❓ سوال: {query}")
    result = rag.ask(query)
    print(f"🤖 پاسخ: {result['answer']}")
    print(f"📊 منابع: {len(result['sources'])} مورد پیدا شد")
    print("-" * 50)

print("\n✅ تست RAG کامل شد!")