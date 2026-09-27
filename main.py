import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import csv
from student import StudentPortal
from admin import AdminPortal
from utils import ensure_data_files

BASE = Path(__file__).resolve().parent

class CampusBiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CampusBite - Campus Food Ordering System")
        self.root.geometry("1050x680")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f5f7fb")
        ensure_data_files()
        self.setup_style()
        self.show_home()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass
        style.configure("TButton", font=("Segoe UI", 11), padding=10)
        style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"), padding=11)
        style.configure("TEntry", padding=8, font=("Segoe UI", 11))
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def header(self, title, subtitle=""):
        frame = tk.Frame(self.root, bg="#172554", height=105)
        frame.pack(fill="x")
        frame.pack_propagate(False)
        tk.Label(frame, text="🍔 CampusBite", font=("Segoe UI", 25, "bold"),
                 fg="white", bg="#172554").pack(anchor="w", padx=35, pady=(17,0))
        tk.Label(frame, text=title + (f"  •  {subtitle}" if subtitle else ""),
                 font=("Segoe UI", 11), fg="#bfdbfe", bg="#172554").pack(anchor="w", padx=37)

    def show_home(self):
        self.clear()
        self.header("Food Ordering System", "Fast, simple and made for campus")
        body = tk.Frame(self.root, bg="#f5f7fb")
        body.pack(expand=True, fill="both")
        tk.Label(body, text="Welcome to CampusBite!", font=("Segoe UI", 30, "bold"),
                 bg="#f5f7fb", fg="#172554").pack(pady=(75,8))
        tk.Label(body, text="Order your favourite campus food from one place.",
                 font=("Segoe UI", 14), bg="#f5f7fb", fg="#475569").pack(pady=(0,40))
        cards = tk.Frame(body, bg="#f5f7fb")
        cards.pack()
        self.home_card(cards, "👨‍🎓", "Student Portal",
                       "Browse menu, manage cart,\nplace orders and view history.",
                       self.show_student_login)
        self.home_card(cards, "👨‍💼", "Admin Portal",
                       "Manage menu, students\nand campus orders.",
                       self.show_admin_login)
        tk.Label(body, text="Python • Tkinter • CSV", font=("Segoe UI", 10),
                 bg="#f5f7fb", fg="#94a3b8").pack(side="bottom", pady=20)

    def home_card(self, parent, icon, title, desc, command):
        card = tk.Frame(parent, bg="white", highlightbackground="#e2e8f0",
                        highlightthickness=1, width=340, height=245)
        card.pack(side="left", padx=18)
        card.pack_propagate(False)
        tk.Label(card, text=icon, font=("Segoe UI Emoji", 40), bg="white").pack(pady=(22,4))
        tk.Label(card, text=title, font=("Segoe UI", 17, "bold"),
                 bg="white", fg="#172554").pack()
        tk.Label(card, text=desc, font=("Segoe UI", 10), bg="white",
                 fg="#64748b", justify="center").pack(pady=10)
        ttk.Button(card, text="Open Portal", command=command,
                   style="Primary.TButton").pack()

    def show_student_login(self):
        self.clear()
        self.header("Student Login", "Sign in to order food")
        box = tk.Frame(self.root, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        box.place(relx=.5, rely=.53, anchor="center", width=430, height=370)
        tk.Label(box, text="🎓 Student Login", font=("Segoe UI", 20, "bold"),
                 bg="white", fg="#172554").pack(pady=(30,25))
        tk.Label(box, text="Email", bg="white", fg="#475569").pack(anchor="w", padx=45)
        email = ttk.Entry(box, width=35)
        email.pack(padx=45, pady=(5,15))
        tk.Label(box, text="Password", bg="white", fg="#475569").pack(anchor="w", padx=45)
        password = ttk.Entry(box, show="•", width=35)
        password.pack(padx=45, pady=(5,18))
        def login():
            from utils import find_row
            row = find_row("students.csv", "email", email.get().strip())
            if not row or row["password"] != password.get():
                messagebox.showerror("Login Failed", "Invalid email or password.")
                return
            StudentPortal(self.root, row, self.show_home)
        ttk.Button(box, text="Login", command=login, style="Primary.TButton").pack(fill="x", padx=45)
        ttk.Button(box, text="Create new account", command=self.show_student_register).pack(pady=8)
        ttk.Button(box, text="← Back", command=self.show_home).pack()

    def show_student_register(self):
        self.clear()
        self.header("Student Registration", "Create your CampusBite account")
        box = tk.Frame(self.root, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        box.place(relx=.5, rely=.53, anchor="center", width=470, height=470)
        tk.Label(box, text="Create Student Account", font=("Segoe UI", 20, "bold"),
                 bg="white", fg="#172554").pack(pady=22)
        entries = {}
        for label, key, show in [("Full Name","name",None),("Email","email",None),
                                 ("College/Department","department",None),("Password","password","•")]:
            tk.Label(box, text=label, bg="white", fg="#475569").pack(anchor="w", padx=45)
            e = ttk.Entry(box, show=show or "", width=38)
            e.pack(padx=45, pady=(4,11))
            entries[key] = e
        def register():
            vals = {k:v.get().strip() for k,v in entries.items()}
            if not all(vals.values()):
                messagebox.showwarning("Missing Details", "Please fill all fields.")
                return
            from utils import append_row, find_row
            if find_row("students.csv","email",vals["email"]):
                messagebox.showerror("Already Registered","This email is already registered.")
                return
            append_row("students.csv", {
                "id": "S" + __import__("utils").next_id("students.csv","id", "S"),
                **vals
            })
            messagebox.showinfo("Success","Account created. You can now log in.")
            self.show_student_login()
        ttk.Button(box, text="Register", command=register, style="Primary.TButton").pack(fill="x", padx=45, pady=5)
        ttk.Button(box, text="← Back to Login", command=self.show_student_login).pack()

    def show_admin_login(self):
        self.clear()
        self.header("Admin Login", "Manage CampusBite")
        box = tk.Frame(self.root, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        box.place(relx=.5, rely=.53, anchor="center", width=430, height=350)
        tk.Label(box, text="🔐 Admin Login", font=("Segoe UI", 20, "bold"),
                 bg="white", fg="#172554").pack(pady=(35,25))
        tk.Label(box, text="Username", bg="white", fg="#475569").pack(anchor="w", padx=45)
        user = ttk.Entry(box, width=35); user.pack(padx=45,pady=(5,15))
        tk.Label(box, text="Password", bg="white", fg="#475569").pack(anchor="w", padx=45)
        pw = ttk.Entry(box, show="•", width=35); pw.pack(padx=45,pady=(5,20))
        def login():
            from utils import find_row
            row = find_row("admins.csv","username",user.get().strip())
            if not row or row["password"] != pw.get():
                messagebox.showerror("Login Failed","Invalid admin credentials.")
                return
            AdminPortal(self.root, self.show_home)
        ttk.Button(box,text="Login",command=login,style="Primary.TButton").pack(fill="x",padx=45)
        ttk.Button(box,text="← Back",command=self.show_home).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    CampusBiteApp(root)
    root.mainloop()
