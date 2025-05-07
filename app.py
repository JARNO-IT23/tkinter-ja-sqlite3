import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Ühendus
conn = sqlite3.connect("jarno16-18.db")
cur = conn.cursor()

# Loome tabeli, kui see puudub
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    image TEXT
)
""")
conn.commit()

# Funktsioonid
def kuva_andmed():
    for row in tree.get_children():
        tree.delete(row)
    cur.execute("SELECT * FROM users")
    for r in cur.fetchall():
        tree.insert("", tk.END, values=r)

def lisa():
    if not (e1.get() and e2.get() and e3.get() and e4.get()):
        messagebox.showwarning("Tühjad väljad", "Kõik väljad peale pildi peavad olema täidetud.")
        return
    try:
        cur.execute("INSERT INTO users (first_name, last_name, email, phone, image) VALUES (?, ?, ?, ?, ?)",
                    (e1.get(), e2.get(), e3.get(), e4.get(), e5.get()))
        conn.commit()
        messagebox.showinfo("OK", "Lisatud!")
        kuva_andmed()
    except:
        messagebox.showerror("Viga", "Lisamine ebaõnnestus.")

def kustuta():
    valik = tree.selection()
    if not valik:
        messagebox.showwarning("Vali", "Vali rida.")
        return
    id = tree.item(valik)["values"][0]
    cur.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    messagebox.showinfo("OK", "Kustutatud.")
    kuva_andmed()

def uuenda():
    valik = tree.selection()
    if not valik:
        messagebox.showwarning("Vali", "Vali rida.")
        return
    id = tree.item(valik)["values"][0]
    try:
        cur.execute("""
        UPDATE users SET first_name=?, last_name=?, email=?, phone=?, image=? WHERE id=?
        """, (e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), id))
        conn.commit()
        messagebox.showinfo("OK", "Muudetud.")
        kuva_andmed()
    except:
        messagebox.showerror("Viga", "Muutmine ebaõnnestus.")

def otsi():
    query = otsing.get()
    for row in tree.get_children():
        tree.delete(row)
    cur.execute("SELECT * FROM users WHERE first_name LIKE ? OR last_name LIKE ?", 
                (f"%{query}%", f"%{query}%"))
    for r in cur.fetchall():
        tree.insert("", tk.END, values=r)

# GUI
root = tk.Tk()
root.title("SQLite GUI (Ülesanded 19–22)")
root.geometry("850x600")

tk.Label(root, text="Eesnimi").grid(row=0, column=0)
tk.Label(root, text="Perekonnanimi").grid(row=1, column=0)
tk.Label(root, text="Email").grid(row=2, column=0)
tk.Label(root, text="Telefon").grid(row=3, column=0)
tk.Label(root, text="Pilt").grid(row=4, column=0)

e1 = tk.Entry(root)
e2 = tk.Entry(root)
e3 = tk.Entry(root)
e4 = tk.Entry(root)
e5 = tk.Entry(root)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)

tk.Button(root, text="Lisa", command=lisa).grid(row=5, column=0, pady=5)
tk.Button(root, text="Uuenda", command=uuenda).grid(row=5, column=1, pady=5)
tk.Button(root, text="Kustuta", command=kustuta).grid(row=5, column=2, pady=5)

tk.Label(root, text="Otsi").grid(row=6, column=0)
otsing = tk.Entry(root)
otsing.grid(row=6, column=1)
tk.Button(root, text="Otsi", command=otsi).grid(row=6, column=2)

cols = ("ID", "Eesnimi", "Perenimi", "Email", "Telefon", "Pilt")
tree = ttk.Treeview(root, columns=cols, show="headings", height=15)
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=130)

tree.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

scroll = tk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
scroll.grid(row=7, column=3, sticky="ns")

kuva_andmed()
root.mainloop()

