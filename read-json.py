import json

# باز کردن و خوندن فایل
with open("students.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# چاپ داده‌ها
print("📘 لیست دانش‌آموزان:")
for student in data:
    print(f"نام: {student['name']}, سن: {student['age']}, شهر: {student['city']}")

