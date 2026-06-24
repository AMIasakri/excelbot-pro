"""
🧠 Embedding Service - ساخت بردار (Embedding) از متن‌ها با استفاده از Sentence-Transformers
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union

class EmbeddingService:
    """
    کلاس سرویس Embedding
    تبدیل متن به بردار عددی برای جستجوی معنایی
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        مقداردهی اولیه مدل
        
        Args:
            model_name: نام مدل از HuggingFace
            گزینه‌های سبک و مناسب:
            - 'all-MiniLM-L6-v2' (سریع و سبک، 384 بعدی)
            - 'all-mpnet-base-v2' (دقیق‌تر ولی سنگین‌تر، 768 بعدی)
        """
        print(f"🔄 در حال بارگذاری مدل {model_name}...")
        self.model = SentenceTransformer(model_name)
        print(f"✅ مدل {model_name} بارگذاری شد")
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"✅ ابعاد بردارها: {self.embedding_dim}")
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        تبدیل یک متن به بردار
        
        Args:
            text: متن ورودی
        
        Returns:
            بردار عددی (numpy array)
        """
        if not text or not text.strip():
            text = "متنی موجود نیست"
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        تبدیل لیستی از متن‌ها به بردار
        
        Args:
            texts: لیست متن‌ها
        
        Returns:
            آرایه‌ای از بردارها
        """
        # فیلتر کردن متن‌های خالی
        valid_texts = [t if t and t.strip() else "متنی موجود نیست" for t in texts]
        embeddings = self.model.encode(valid_texts, convert_to_numpy=True)
        return embeddings
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        تبدیل سوال کاربر به بردار (مخصوص جستجو)
        
        Args:
            query: سوال کاربر
        
        Returns:
            بردار عددی
        """
        return self.embed_text(query)

# نمونه برای تست
if __name__ == "__main__":
    # تست سرویس
    service = EmbeddingService()
    
    # تست با یک متن نمونه
    sample_text = "نحوه ثبت سفارش در فروشگاه"
    embedding = service.embed_text(sample_text)
    
    print(f"✅ متن: {sample_text}")
    print(f"✅ ابعاد بردار: {embedding.shape}")
    print(f"✅ ۱۰ عدد اول بردار: {embedding[:10]}")