"""
📂 Excel Loader - خواندن و پردازش فایل اکسل
"""

import pandas as pd
import os
from typing import List, Dict, Any

def load_excel_data(file_path: str) -> List[Dict[str, Any]]:
    """
    خواندن فایل اکسل و تبدیل به لیست دیکشنری
    
    Args:
        file_path: مسیر فایل اکسل
    
    Returns:
        لیستی از دیکشنری‌ها با داده‌های تمیز شده
    """
    # بررسی وجود فایل
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ فایل {file_path} پیدا نشد!")
    
    # خواندن فایل اکسل
    df = pd.read_excel(file_path)
    
    # نمایش اطلاعات اولیه
    print(f"✅ تعداد ردیف‌ها: {len(df)}")
    print(f"✅ ستون‌ها: {list(df.columns)}")
    
    # حذف ردیف‌های خالی
    df = df.dropna(how='all')
    
    # پر کردن مقادیر NaN با رشته خالی
    df = df.fillna('')
    
    # تبدیل به لیست دیکشنری
    records = df.to_dict('records')
    
    # اضافه کردن یک فیلد ترکیبی برای جستجوی بهتر
    for record in records:
        # همه مقادیر غیر خالی را ترکیب می‌کنیم برای جستجو
        text_parts = [str(v) for v in record.values() if str(v).strip()]
        record['_combined_text'] = ' '.join(text_parts)
    
    print(f"✅ {len(records)} رکورد آماده شد")
    return records

# تابع تست (برای اینکه خودمون تست کنیم)
if __name__ == "__main__":
    # مسیر فایل اکسل رو به‌روز کن
    test_path = "../data/data.xlsx"
    
    try:
        data = load_excel_data(test_path)
        print("\n📊 نمونه اولین رکورد:")
        print(data[0])
        print(f"\n✅ مجموعاً {len(data)} رکورد بارگذاری شد")
    except Exception as e:
        print(f"❌ خطا: {e}")
        print("⚠️ لطفاً یک فایل اکسل در پوشه backend/data/ قرار دهید")