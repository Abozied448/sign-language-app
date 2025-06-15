import os
import json

# ✅ مسار مجلد الداتا (عدله حسب مكان الداتا)
dataset_path = r'D:\project\text_dataset'

# ✅ قراءة أسماء الفولدرات فقط (تجاهل الملفات)
class_names = sorted([
    folder for folder in os.listdir(dataset_path)
    if os.path.isdir(os.path.join(dataset_path, folder))
])

# ✅ حفظهم في ملف JSON
with open("class_names.json", "w", encoding='utf-8') as f:
    json.dump(class_names, f, ensure_ascii=False)

print("✅ تم حفظ أسماء الكلاسات في class_names.json")
print("📁 الكلمات:", class_names)
