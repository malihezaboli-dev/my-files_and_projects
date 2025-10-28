import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ---------- کلاس پایگاه داده ----------
class ContactDatabase:
    def __init__(self, db_name="contacts.db"):
        self.db_name = db_name
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL
                )
            """)
            conn.commit()

    def insert_contact(self, name, phone):
        with self.connect() as conn:
            conn.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
            conn.commit()

    def update_contact(self, contact_id, name, phone):
        with self.connect() as conn:
            conn.execute("UPDATE contacts SET name=?, phone=? WHERE id=?", (name, phone, contact_id))
            conn.commit()

    def delete_contact(self, contact_id):
        with self.connect() as conn:
            conn.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
            conn.commit()

    def fetch_all(self):
        with self.connect() as conn:
            return conn.execute("SELECT * FROM contacts").fetchall()

    def search_contacts(self, keyword):
        with self.connect() as conn:
            return conn.execute(
                "SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?",
                (f"%{keyword}%", f"%{keyword}%")
            ).fetchall()


# ---------- کلاس اصلی اپ ----------
class ContactManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("مدیریت مخاطبین")
        self.geometry("550x450")
        self.resizable(False, False)

        self.db = ContactDatabase()

        # دیکشنری برای صفحات
        self.frames = {}

        # ایجاد صفحات
        for F in (HomePage, AddContactPage, EditContactPage):
            frame = F(self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        # نمایش صفحه اصلی
        self.show_frame(HomePage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()
        if hasattr(frame, "refresh"):
            frame.refresh()


# ---------- صفحه‌ی اصلی (نمایش لیست مخاطبین) ----------
class HomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db = master.db

        tk.Label(self, text="📞 لیست مخاطبین", font=("B Nazanin", 16, "bold")).pack(pady=10)

        # جستجو
        search_frame = tk.Frame(self)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="جستجو:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT)
        tk.Button(search_frame, text="🔍", command=self.search_contacts).pack(side=tk.LEFT)
        tk.Button(search_frame, text="نمایش همه", command=self.refresh).pack(side=tk.LEFT, padx=5)

        # جدول
        self.tree = ttk.Treeview(self, columns=("id", "name", "phone"), show="headings")
        self.tree.heading("id", text="کد")
        self.tree.heading("name", text="نام")
        self.tree.heading("phone", text="شماره تلفن")
        self.tree.column("id", width=50)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # دکمه‌ها
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="➕ افزودن مخاطب", command=lambda: master.show_frame(AddContactPage)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ ویرایش", command=self.go_to_edit).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑 حذف", command=self.delete_contact).pack(side=tk.LEFT, padx=5)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for contact in self.db.fetch_all():
            self.tree.insert("", tk.END, values=contact)

    def search_contacts(self):
        keyword = self.search_entry.get().strip()
        results = self.db.search_contacts(keyword)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for contact in results:
            self.tree.insert("", tk.END, values=contact)

    def delete_contact(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("خطا", "لطفاً یک مخاطب را انتخاب کنید.")
            return

        contact_id = self.tree.item(selected)["values"][0]
        confirm = messagebox.askyesno("تأیید حذف", "آیا از حذف این مخاطب مطمئن هستید؟")
        if confirm:
            self.db.delete_contact(contact_id)
            self.refresh()

    def go_to_edit(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("خطا", "لطفاً یک مخاطب را انتخاب کنید.")
            return

        contact_id, name, phone = self.tree.item(selected)["values"]
        edit_page = self.master.frames[EditContactPage]
        edit_page.load_contact(contact_id, name, phone)
        self.master.show_frame(EditContactPage)


# ---------- صفحه افزودن مخاطب ----------
class AddContactPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db = master.db

        tk.Label(self, text="➕ افزودن مخاطب جدید", font=("B Nazanin", 16, "bold")).pack(pady=15)

        form = tk.Frame(self)
        form.pack(pady=20)

        tk.Label(form, text="نام:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form)
        self.name_entry.grid(row=0, column=1)

        tk.Label(form, text="شماره تلفن:").grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(form)
        self.phone_entry.grid(row=1, column=1)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="ذخیره", command=self.add_contact).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="بازگشت", command=lambda: master.show_frame(HomePage)).pack(side=tk.LEFT, padx=5)

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning("خطا", "لطفاً نام و شماره تلفن را وارد کنید.")
            return

        self.db.insert_contact(name, phone)
        messagebox.showinfo("موفقیت", "مخاطب با موفقیت افزوده شد.")
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.master.show_frame(HomePage)


# ---------- صفحه ویرایش مخاطب ----------
class EditContactPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db = master.db
        self.contact_id = None

        tk.Label(self, text="✏️ ویرایش مخاطب", font=("B Nazanin", 16, "bold")).pack(pady=15)

        form = tk.Frame(self)
        form.pack(pady=20)

        tk.Label(form, text="نام:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form)
        self.name_entry.grid(row=0, column=1)

        tk.Label(form, text="شماره تلفن:").grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(form)
        self.phone_entry.grid(row=1, column=1)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="ذخیره تغییرات", command=self.save_changes).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="بازگشت", command=lambda: master.show_frame(HomePage)).pack(side=tk.LEFT, padx=5)

    def load_contact(self, contact_id, name, phone):
        self.contact_id = contact_id
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
        self.phone_entry.insert(0, phone)

    def save_changes(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning("خطا", "لطفاً نام و شماره تلفن را وارد کنید.")
            return

        self.db.update_contact(self.contact_id, name, phone)
        messagebox.showinfo("موفقیت", "تغییرات ذخیره شد.")
        self.master.show_frame(HomePage)


# ---------- اجرای برنامه ----------
if __name__ == "__main__":
    app = ContactManagerApp()
    app.mainloop()
