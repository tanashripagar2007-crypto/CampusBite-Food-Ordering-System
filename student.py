import tkinter as tk
from tkinter import ttk, messagebox
from utils import read_csv, append_row, next_id, money, timestamp

class StudentPortal:
    def __init__(self, root, student, logout):
        self.root=root; self.student=student; self.logout=logout; self.cart={}
        self.show_dashboard()

    def clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def header(self,title):
        f=tk.Frame(self.root,bg="#172554",height=88); f.pack(fill="x"); f.pack_propagate(False)
        tk.Label(f,text="🍔 CampusBite",font=("Segoe UI",23,"bold"),fg="white",bg="#172554").pack(side="left",padx=30)
        tk.Label(f,text=title,font=("Segoe UI",13),fg="#bfdbfe",bg="#172554").pack(side="left")
        ttk.Button(f,text="Logout",command=self.logout).pack(side="right",padx=25)

    def show_dashboard(self):
        self.clear(); self.header(f"Welcome, {self.student['name']}")
        nav=tk.Frame(self.root,bg="#e2e8f0",height=52); nav.pack(fill="x")
        ttk.Button(nav,text="🍴 Menu",command=self.show_menu).pack(side="left",padx=12,pady=8)
        ttk.Button(nav,text="🛒 Cart",command=self.show_cart).pack(side="left",pady=8)
        ttk.Button(nav,text="📦 My Orders",command=self.show_orders).pack(side="left",padx=12,pady=8)
        self.show_menu_body()

    def show_menu(self): self.show_dashboard()
    def show_menu_body(self):
        body=tk.Frame(self.root,bg="#f5f7fb"); body.pack(fill="both",expand=True)
        top=tk.Frame(body,bg="#f5f7fb"); top.pack(fill="x",padx=28,pady=18)
        tk.Label(top,text="Campus Menu",font=("Segoe UI",22,"bold"),bg="#f5f7fb",fg="#172554").pack(side="left")
        search=ttk.Entry(top,width=30); search.pack(side="right",ipady=4)
        search.insert(0,"Search food...")
        def filter_items(*_):
            q=search.get().lower()
            for c in cards.winfo_children(): c.destroy()
            rows=[r for r in read_csv("menu.csv") if r["availability"].lower()=="yes" and (q in r["name"].lower() or q in r["category"].lower())]
            for r in rows: self.food_card(cards,r)
        search.bind("<KeyRelease>",filter_items)
        cards=tk.Frame(body,bg="#f5f7fb"); cards.pack(fill="both",expand=True,padx=25,pady=5)
        self.cards=cards
        for r in read_csv("menu.csv"):
            if r["availability"].lower()=="yes": self.food_card(cards,r)

    def food_card(self,parent,r):
        c=tk.Frame(parent,bg="white",highlightbackground="#e2e8f0",highlightthickness=1,width=220,height=175)
        c.pack(side="left",padx=8,pady=8); c.pack_propagate(False)
        tk.Label(c,text="🍽️",font=("Segoe UI Emoji",28),bg="white").pack(pady=(12,0))
        tk.Label(c,text=r["name"],font=("Segoe UI",13,"bold"),bg="white",fg="#172554").pack()
        tk.Label(c,text=r["category"],font=("Segoe UI",9),bg="white",fg="#64748b").pack()
        tk.Label(c,text=money(r["price"]),font=("Segoe UI",12,"bold"),bg="white",fg="#15803d").pack(pady=4)
        ttk.Button(c,text="Add to Cart",command=lambda x=r:self.add_cart(x)).pack()

    def add_cart(self,r):
        fid=r["id"]
        if fid not in self.cart: self.cart[fid]={"item":r,"qty":0}
        self.cart[fid]["qty"]+=1
        messagebox.showinfo("Cart","Added to cart.")

    def show_cart(self):
        self.clear(); self.header("Shopping Cart")
        body=tk.Frame(self.root,bg="#f5f7fb"); body.pack(fill="both",expand=True,padx=35,pady=25)
        tk.Label(body,text="Your Cart",font=("Segoe UI",23,"bold"),bg="#f5f7fb",fg="#172554").pack(anchor="w")
        tree=ttk.Treeview(body,columns=("item","price","qty","subtotal"),show="headings")
        for col,title in zip(("item","price","qty","subtotal"),("Food Item","Price","Quantity","Subtotal")):
            tree.heading(col,text=title); tree.column(col,anchor="center")
        tree.pack(fill="both",expand=True,pady=15)
        total=0
        for fid,data in self.cart.items():
            r=data["item"]; sub=float(r["price"])*data["qty"]; total+=sub
            tree.insert("", "end", iid=fid, values=(r["name"],money(r["price"]),data["qty"],money(sub)))
        bottom=tk.Frame(body,bg="#f5f7fb"); bottom.pack(fill="x")
        tk.Label(bottom,text=f"Total: {money(total)}",font=("Segoe UI",17,"bold"),bg="#f5f7fb",fg="#172554").pack(side="right",padx=15)
        def remove():
            sel=tree.selection()
            if sel:
                del self.cart[sel[0]]; self.show_cart()
        ttk.Button(bottom,text="Remove Selected",command=remove).pack(side="left")
        ttk.Button(bottom,text="← Continue Shopping",command=self.show_dashboard).pack(side="left",padx=8)
        ttk.Button(bottom,text="Checkout",command=lambda:self.checkout(total),
                   style="Primary.TButton").pack(side="right")
        if not self.cart:
            tk.Label(body,text="Your cart is empty.",font=("Segoe UI",13),bg="#f5f7fb",fg="#64748b").pack(pady=30)

    def checkout(self,total):
        if not self.cart: messagebox.showwarning("Empty Cart","Add food items first."); return
        if not messagebox.askyesno("Confirm Order",f"Place order for {money(total)}?"): return
        items="; ".join(f"{d['item']['name']} x{d['qty']}" for d in self.cart.values())
        oid="ORD"+next_id("orders.csv","order_id","ORD")
        append_row("orders.csv",{"order_id":oid,"student_id":self.student["id"],"student_name":self.student["name"],
                                 "items":items,"total":f"{total:.2f}","status":"Placed","date":timestamp()})
        self.cart.clear()
        messagebox.showinfo("Order Placed",f"Order {oid} placed successfully!\nTotal: {money(total)}")
        self.show_orders()

    def show_orders(self):
        self.clear(); self.header("My Orders")
        body=tk.Frame(self.root,bg="#f5f7fb"); body.pack(fill="both",expand=True,padx=30,pady=25)
        tk.Label(body,text="Order History",font=("Segoe UI",23,"bold"),bg="#f5f7fb",fg="#172554").pack(anchor="w",pady=(0,15))
        tree=ttk.Treeview(body,columns=("id","items","total","status","date"),show="headings")
        for c,t,w in [("id","Order ID",100),("items","Items",360),("total","Total",100),("status","Status",110),("date","Date",170)]:
            tree.heading(c,text=t); tree.column(c,width=w,anchor="center")
        tree.pack(fill="both",expand=True)
        for r in read_csv("orders.csv"):
            if r["student_id"]==self.student["id"]:
                tree.insert("","end",values=(r["order_id"],r["items"],money(r["total"]),r["status"],r["date"]))
