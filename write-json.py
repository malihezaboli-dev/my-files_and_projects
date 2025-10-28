import json  # ماژول مخصوص کار با JSON

# 1️⃣ داده‌ها (لیست از دیکشنری‌ها)
students = [
    {"name": "Ali", "age": 15, "city": "Tehran"},
    {"name": "Sara", "age": 16, "city": "Shiraz"},
    {"name": "Reza", "age": 14, "city": "Mashhad"}
]

# 2️⃣ ذخیره داده‌ها در فایل JSON
with open("students.json", "w", encoding="utf-8") as file:
    json.dump(students, file, ensure_ascii=False, indent=4)

print("✅ فایل students.json ساخته شد!")
