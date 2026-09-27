import tkinter as tk
from tkinter import ttk, messagebox
from utils import read_csv, write_csv, append_row, next_id, money, timestamp

class AdminPortal:
    def __init__(self,root,logout):
        self.root=root; self.logout=logout; self.show_dashboard()

    def clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def header(self,title):
        f=tk.Frame(self.root,bg="#172554",height=88); f.pack(fill="x"); f.pack_propagate(False)
        tk.Label(f,text="🍔 CampusBite",font=("Segoe UI",23,"bold"),fg="white",bg="#172554").pack(side="left",padx=30)
        tk.Label(f,text=title,font=("Segoe UI",13),fg="#bfdbfe",bg="#172554").pack(side="left")
        ttk.Button(f,text="Logout",command=self.logout).pack(side="right",padx=25)

    def nav(self):
        n=tk.Frame(self.root,bg="#e2e8f0",height=52); n.pack(fill="x")
        for txt,cmd in [("📊 Dashboard",self.show_dashboard),("🍔 Menu",self.show_menu),
                        ("📦 Orders",self.show_orders),("👨‍🎓 Students",self.show_students)]:
            ttk.Button(n,text=txt,command=cmd).pack(side="left",padx=8,pady=8)

    def show_dashboard(self):
        self.clear(); self.header("Admin Dashboard"); self.nav()
        body=tk.Frame(self.root,bg="#f5f7fb"); body.pack(fill="both",expand=True,padx=35,pady=30)
        menu=read_csv("menu.csv"); orders=read_csv("orders.csv"); students=read_csv("students.csv")
        cards=tk.Frame(body,bg="#f5f7fb"); cards.pack(fill="x")
        for title,value,icon in [("Food Items",len(menu),"🍔"),("Total Orders",len(orders),"📦"),
                                ("Students",len(students),"👨‍🎓"),
                                ("Revenue",money(sum(float(x["total"]) for x in orders)),"₹")]:
            c=tk.Frame(cards,bg="white",highlightbackground="#e2e8f0",highlightthickness=1,width=205,height=125)
            c.pack(side="left",padx=7); c.pack_propagate(False)
            tk.Label(c,text=icon,font=("Segoe UI Emoji",22),bg="white").pack(pady=(14,0))
            tk.Label(c,text=str(value),font=("Segoe UI",19,"bold"),bg="white",fg="#172554").pack()
            tk.Label(c,text=title,font=("Segoe UI",10),bg="white",fg="#64748b").pack()
        tk.Label(body,text="Quick Actions",font=("Segoe UI",19,"bold"),bg="#f5f7fb",fg="#172554").pack(anchor="w",pady=(35,12))
        ttk.Button(body,text="➕ Add New Food Item",command=self.add_food,style="Primary.TButton").pack(anchor="w")

    def show_menu(self):
        self.clear(); self.header("Menu Management"); self.nav()
        body=tk.Frame(self.root,bg="#f5f7fb"); body.pack(fill="both",expand=True,padx=30,pady=20)
        top=tk.Frame(body,bg="#f5f7fb"); top.pack(fill="x")
        tk.Label(top,text="Food Menu",font=("Segoe UI",22,"bold"),bg="#f5f7fb",fg="#172554").pack(side="left")
        ttk.Button(top,text="➕ Add Food",command=self.add_food).pack(side="right")
        tree=ttk.Treeview(body,columns=("id","name","cat","price","avail"),show="headings")
        for c,t in zip(("id","name","cat","price","avail"),("ID","Name","Category","Price","Availability")):
            tree.heading(c,text=t); tree.column(c,anchor="center")
        tree.pack(fill="both",expand=True,pady=15)
        for r in read_csv("menu.csv"): tree.insert("","end",iid=r["id"],values=(r["id"],r["name"],r["category"],money(r["price"]),r["availability"]))
        actions=tk.Frame(body,bg="#f5f7fb"); actions.pack(fill="x")
        ttk.Button(actions,text="Edit Selected",command=lambda:self.edit_food(tree)).pack(side="left")
        ttk.Button(actions,text="Delete Selected",command=lambda:self.delete_food(tree)).pack(side="left",padx=8)

    def add_food(self):
        self.food_form()

    def edit_food(self,tree):
        sel=tree.selection()
        if not sel: messagebox.showwarning("Select Item","Select a food item first."); return
        row=next(r for r in read_csv("menu.csv") if r["id"]==sel[0])
        self.food_form(row)

    def food_form(self,row=None):
        win=tk.Toplevel(self.root); win.title("Food Item"); win.geometry("400x430"); win.transient(self.root); win.grab_set()
        tk.Label(win,text="Food Item",font=("Segoe UI",20,"bold")).pack(pady=20)
        fields={}
        for label,key in [("Food Name","name"),("Category","category"),("Price (₹)","price"),("Availability (Yes/No)","availability")]:
            tk.Label(win,text=label).pack(anchor="w",padx=40)
            e=ttk.Entry(win); e.pack(fill="x",padx=40,pady=(3,12))
            if row: e.insert(0,row[key])
            fields[key]=e
        def save():
            vals={k:v.get().strip() for k,v in fields.items()}
            try: float(vals["price"])
            except: messagebox.showerror("Invalid Price","Enter a valid price."); return
            if not vals["name"] or not vals["category"]: messagebox.showwarning("Missing","Fill all fields."); return
            rows=read_csv("menu.csv")
            if row:
                for r in rows:
                    if r["id"]==row["id"]: r.update(vals)
                write_csv("menu.csv",rows)
            else:
                vals["id"]="F"+next_id("menu.csv","id","F"); append_row("menu.csv",vals)
            win.destroy(); self.show_menu()
        ttk.Button(win,text="Save",command=save,style="Primary.TButton").pack(fill="x",padx=40,pady=10)

    def delete_food(self,tree):
        sel=tree.selection()
        if not sel: messagebox.showwarning("Select Item","Select an item."); return
        if not messagebox.askyesno("Delete","Delete selected food item?"): return
        rows=[r for r in read_csv("menu.csv") if r["id"]!=sel[0]]
        write_csv("menu.csv",rows); self.show_menu()

    def show_orders(self):
        self.clear(); self.header("Order Management"); self.nav()
        body=tk.Frame(self.root,bg="#f5f7fb"); body.pack(fill="both",expand=True,padx=25,pady=20)
        tree=ttk.Treeview(body,columns=("id","student","items","total","status","date"),show="headings")
        for c,t,w in [("id","Order ID",90),("student","Student",130),("items","Items",330),("total","Total",90),("status","Status",110),("date","Date",170)]:
            tree.heading(c,text=t); tree.column(c,width=w,anchor="center")
        tree.pack(fill="both",expand=True)
        for r in read_csv("orders.csv"):
            tree.insert("","end",iid=r["order_id"],values=(r["order_id"],r["student_name"],r["items"],money(r["total"]),r["status"],r["date"]))
        def update_status():
            sel=tree.selection()
            if not sel: messagebox.showwarning("Select","Select an order."); return
            win=tk.Toplevel(self.root); win.title("Update Status"); win.geometry("330x190")
            tk.Label(win,text="Order Status",font=("Segoe UI",14,"bold")).pack(pady=20)
            combo=ttk.Combobox(win,values=["Placed","Preparing","Ready","Completed","Cancelled"],state="readonly")
            combo.pack(); combo.set("Preparing")
            def save():
                rows=read_csv("orders.csv")
                for r in rows:
                    if r["order_id"]==sel[0]: r["status"]=combo.get()
                write_csv("orders.csv",rows); win.destroy(); self.show_orders()
            ttk.Button(win,text="Update",command=save).pack(pady=20)
        ttk.Button(body,text="Update Selected Status",command=update_status).pack(anchor="w",pady=10)

    def show_students(self):
        self.clear(); self.header("Student Management"); self.nav()
        body=tk.Frame(self.root,bg="#f5f7fb"); body.pack(fill="both",expand=True,padx=30,pady=25)
        tree=ttk.Treeview(body,columns=("id","name","email","department"),show="headings")
        for c,t in zip(("id","name","email","department"),("ID","Name","Email","Department")):
            tree.heading(c,text=t); tree.column(c,anchor="center")
        tree.pack(fill="both",expand=True)
        for r in read_csv("students.csv"): tree.insert("","end",values=(r["id"],r["name"],r["email"],r["department"]))
