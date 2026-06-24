from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore

# ۱. ساخت سرویس Embedding
print("=" * 50)
print("🔄 در حال تست Embedding Service...")
embedding_service = EmbeddingService()

# ۲. ساخت Vector Store
print("\n" + "=" * 50)
print("🔄 در حال تست Vector Store...")
vector_store = VectorStore(embedding_service)

# ۳. داده‌های نمونه
texts = [
    "نحوه ثبت سفارش در فروشگاه اینترنتی",
    "روش بازگشت کالا تا ۷ روز کاری",
    "ساعت کاری پشتیبانی از ۹ صبح تا ۶ عصر",
    "روش پرداخت آنلاین با کارت بانکی"
]
metadatas = [
    {"question": "ثبت سفارش", "answer": "به بخش خرید بروید و محصول را انتخاب کنید", "category": "راهنما"},
    {"question": "بازگشت کالا", "answer": "تا ۷ روز کاری امکان بازگشت وجود دارد", "category": "پشتیبانی"},
    {"question": "ساعت کاری", "answer": "پشتیبانی از ۹ صبح تا ۶ عصر فعال است", "category": "پشتیبانی"},
    {"question": "پرداخت", "answer": "پرداخت از طریق درگاه بانکی انجام میشود", "category": "راهنما"}
]

# ۴. ساخت ایندکس
print("\n" + "=" * 50)
print("🔄 در حال ساخت ایندکس...")
vector_store.create_index(texts, metadatas)

# ۵. تست جستجو
print("\n" + "=" * 50)
print("🔍 تست جستجو:")
queries = [
    "چطور سفارش ثبت کنم؟",
    "چند روز وقت دارم کالا رو برگردونم؟"
]

for query in queries:
    print(f"\n📝 سوال: {query}")
    results = vector_store.search(query, top_k=2)
    for meta, dist in results:
        print(f"  - {meta['question']} (فاصله: {dist:.4f})")
        print(f"    پاسخ: {meta['answer']}")

print("\n" + "=" * 50)
print("✅ همه تست‌ها با موفقیت انجام شد!")