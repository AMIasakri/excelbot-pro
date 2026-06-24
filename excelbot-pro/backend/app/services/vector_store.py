"""
📚 Vector Store - ذخیره‌سازی و جستجوی بردارها با FAISS
"""

import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any, Tuple
from .embedding_service import EmbeddingService

class VectorStore:
    """
    کلاس مدیریت پایگاه داده برداری با FAISS
    """
    
    def __init__(self, embedding_service: EmbeddingService, index_path: str = "chroma_db/faiss_index"):
        """
        مقداردهی اولیه
        
        Args:
            embedding_service: نمونه از سرویس Embedding
            index_path: مسیر ذخیره فایل‌های FAISS
        """
        self.embedding_service = embedding_service
        self.index_path = index_path
        self.index = None
        self.metadata = []  # ذخیره اطلاعات هر رکورد
        self.dimension = embedding_service.embedding_dim
        
        # ساخت پوشه اگر وجود ندارد
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        # بارگذاری ایندکس موجود (اگر وجود داشته باشد)
        self.load()
    
    def create_index(self, texts: List[str], metadatas: List[Dict[str, Any]]):
        """
        ساخت ایندکس جدید از لیست متن‌ها
        
        Args:
            texts: لیست متن‌ها برای Embedding
            metadatas: لیست متادیتا (دسته‌بندی، پاسخ و...)
        """
        print(f"🔄 در حال ساخت {len(texts)} بردار...")
        
        # ساخت Embedding برای همه متن‌ها
        embeddings = self.embedding_service.embed_texts(texts)
        
        # ساخت ایندکس FAISS
        self.index = faiss.IndexFlatL2(self.dimension)  # L2 = فاصله اقلیدسی
        
        # اضافه کردن بردارها به ایندکس
        self.index.add(embeddings.astype('float32'))
        
        # ذخیره متادیتا
        self.metadata = metadatas
        
        print(f"✅ {len(texts)} رکورد ذخیره شد")
        print(f"✅ ابعاد ایندکس: {self.index.ntotal}")
        
        # ذخیره روی دیسک
        self.save()
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """
        جستجوی بردارهای مشابه با سوال کاربر
        
        Args:
            query: سوال کاربر
            top_k: تعداد نتایج برتر
        
        Returns:
            لیستی از (متادیتا, فاصله) که نزدیک‌ترین‌ها هستند
        """
        if self.index is None or self.index.ntotal == 0:
            print("⚠️ ایندکس خالی است!")
            return []
        
        # تبدیل سوال به بردار
        query_embedding = self.embedding_service.embed_query(query)
        
        # جستجو در FAISS
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1).astype('float32'), 
            min(top_k, self.index.ntotal)
        )
        
        # ساخت نتایج
        results = []
        for i, idx in enumerate(indices[0]):
            if idx >= 0 and idx < len(self.metadata):
                results.append((self.metadata[idx], distances[0][i]))
        
        return results
    
    def save(self):
        """ذخیره ایندکس و متادیتا روی دیسک"""
        if self.index is None:
            print("⚠️ چیزی برای ذخیره وجود ندارد")
            return
        
        # ذخیره ایندکس FAISS
        faiss.write_index(self.index, f"{self.index_path}.index")
        
        # ذخیره متادیتا با pickle
        with open(f"{self.index_path}.meta", 'wb') as f:
            pickle.dump(self.metadata, f)
        
        print(f"✅ ایندکس در {self.index_path} ذخیره شد")
    
    def load(self):
        """بارگذاری ایندکس و متادیتا از دیسک"""
        index_file = f"{self.index_path}.index"
        meta_file = f"{self.index_path}.meta"
        
        if os.path.exists(index_file) and os.path.exists(meta_file):
            try:
                self.index = faiss.read_index(index_file)
                with open(meta_file, 'rb') as f:
                    self.metadata = pickle.load(f)
                print(f"✅ ایندکس از {self.index_path} بارگذاری شد ({self.index.ntotal} رکورد)")
                return True
            except Exception as e:
                print(f"⚠️ خطا در بارگذاری ایندکس: {e}")
                return False
        else:
            print("ℹ️ ایندکسی برای بارگذاری وجود ندارد")
            return False
    
    def get_total_count(self) -> int:
        """تعداد رکوردهای موجود در ایندکس"""
        if self.index is None:
            return 0
        return self.index.ntotal

# نمونه برای تست
if __name__ == "__main__":
    # تست سرویس
    embedding_service = EmbeddingService()
    vector_store = VectorStore(embedding_service)
    
    # داده‌های نمونه
    sample_texts = [
        "نحوه ثبت سفارش در فروشگاه",
        "روش بازگشت کالا",
        "ساعت کاری پشتیبانی"
    ]
    sample_metadatas = [
        {"title": "ثبت سفارش", "answer": "به بخش خرید بروید", "category": "راهنما"},
        {"title": "بازگشت کالا", "answer": "تا ۷ روز کاری", "category": "پشتیبانی"},
        {"title": "ساعت کاری", "answer": "۹ صبح تا ۶ عصر", "category": "پشتیبانی"}
    ]
    
    # ساخت ایندکس
    vector_store.create_index(sample_texts, sample_metadatas)
    
    # جستجو
    results = vector_store.search("چطور سفارش ثبت کنم؟", top_k=2)
    print("\n📊 نتایج جستجو:")
    for meta, dist in results:
        print(f"  - {meta['title']} (فاصله: {dist:.4f})")