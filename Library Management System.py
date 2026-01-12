import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Library Management System")
        self.root.geometry("1200x700+100+50")
        self.root.resizable(False, False)

        # --- Title ---
        title = tk.Label(self.root, text="Library Management System",
                         bg="#3b5998", fg="white", font=("Elephant", 36, "bold"),
                         bd=4, relief="raised", pady=10)
        title.pack(side="top", fill="x")

        # --- Option Frame (Left) ---
        optFrame = tk.Frame(self.root, bd=4, relief="ridge", bg="#f0f0f0")
        optFrame.place(width=300, height=550, x=30, y=120)

        buttons = [
            ("Add Book", self.addFrameFun),
            ("Search Book", self.searchFrameFun),
            ("Update Book", self.updateFrameFun),
            ("Show All", self.showAll),
            ("Delete Book", self.deleteFrameFun)
        ]

        for i, (text, cmd) in enumerate(buttons):
            btn = tk.Button(optFrame, text=text, command=cmd,
                            bg="#2196f3", fg="white", bd=3, relief="raised",
                            font=("Arial", 16, "bold"), width=18, height=2)
            btn.grid(row=i, column=0, padx=20, pady=12)
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1976d2"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2196f3"))

        # --- Detail Frame (Right) ---
        self.detFrame = tk.Frame(self.root, bd=4, relief="ridge", bg="#fff9c4")
        self.detFrame.place(width=840, height=550, x=350, y=120)

        tk.Label(self.detFrame, text="Book Records",
                 font=("Arial", 28, "bold"), bg="#fff9c4").pack(side="top", fill="x", pady=10)

        self.tabFun()
        self.currentFrame = None

    # -------------------- DATABASE --------------------
    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="Ram@1234", database="librarydb")
        self.cur = self.con.cursor()

    # -------------------- TABLE --------------------
    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken", bg="#b2ebf2")
        tabFrame.place(width=800, height=420, x=20, y=80)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
        style.configure("Treeview", font=("Arial", 14), rowheight=28)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")
        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,
                                  columns=("id", "title", "author", "genre", "status"))
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("id", text="ID")
        self.table.heading("title", text="Title")
        self.table.heading("author", text="Author")
        self.table.heading("genre", text="Genre")
        self.table.heading("status", text="Status")
        self.table["show"] = "headings"

        for col, width in zip(("id", "title", "author", "genre", "status"), (80, 220, 200, 150, 120)):
            self.table.column(col, width=width, anchor="center")

        self.table.pack(fill="both", expand=1, padx=5, pady=5)

    def close_current_frame(self):
        if self.currentFrame:
            self.currentFrame.destroy()
            self.currentFrame = None

    # -------------------- ADD BOOK --------------------
    def addFrameFun(self):
        self.close_current_frame()
        self.currentFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#aed581")
        self.currentFrame.place(width=450, height=450, x=400, y=140)

        # Text fields
        entries = [("Title:", "title"), ("Author:", "author"), ("Genre:", "genre")]
        self.addVars = {}
        for i, (lbl, var) in enumerate(entries):
            tk.Label(self.currentFrame, text=lbl, font=("arial", 15, "bold"), bg="#aed581").grid(row=i, column=0, padx=20, pady=12, sticky="w")
            ent = tk.Entry(self.currentFrame, width=25, font=("arial", 15, "bold"), bd=3)
            ent.grid(row=i, column=1, padx=10, pady=12)
            self.addVars[var] = ent

        # Dropdown for Status
        tk.Label(self.currentFrame, text="Status:", font=("arial", 15, "bold"), bg="#aed581").grid(row=3, column=0, padx=20, pady=12, sticky="w")
        self.status_var = ttk.Combobox(self.currentFrame, values=("Available", "Borrowed",'Return'),
                                       font=("arial", 15, "bold"), width=22, state="readonly")
        self.status_var.set("Available")
        self.status_var.grid(row=3, column=1, padx=10, pady=12)

        tk.Button(self.currentFrame, text="Add Book", command=self.addFun,
                  bd=3, relief="raised", font=("Arial", 18, "bold"), width=18).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.currentFrame, text="❌ Back", command=self.close_current_frame,
                  bd=3, relief="raised", font=("Arial", 14, "bold"), width=12, bg="red", fg="white").grid(row=5, column=0, columnspan=2, pady=10)

    def addFun(self):
        title = self.addVars["title"].get().strip()
        author = self.addVars["author"].get().strip()
        genre = self.addVars["genre"].get().strip()
        status = self.status_var.get().strip()

        if title and author and genre and status:
            try:
                self.dbFun()
                self.cur.execute("INSERT INTO books (title, author, genre, status) VALUES (%s, %s, %s, %s)",
                                 (title, author, genre, status))
                self.con.commit()
                messagebox.showinfo("Success", f"Book '{title}' added successfully!")
                self.showAll()
                self.close_current_frame()
                self.con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showerror("Error", "All fields are required!")

    # -------------------- SEARCH BOOK --------------------
    def searchFrameFun(self):
        self.close_current_frame()
        self.currentFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#64b5f6")
        self.currentFrame.place(width=450, height=270, x=400, y=140)

        tk.Label(self.currentFrame, text="Search By:", font=("arial", 15, "bold"), bg="#64b5f6").grid(row=0, column=0, padx=20, pady=15, sticky="w")
        self.option = ttk.Combobox(self.currentFrame, width=20, values=("title", "author", "genre", "status"), font=("Arial", 15, "bold"))
        self.option.set("Select Option")
        self.option.grid(row=0, column=1, padx=10, pady=15)

        tk.Label(self.currentFrame, text="Value:", font=("arial", 15, "bold"), bg="#64b5f6").grid(row=1, column=0, padx=20, pady=15, sticky="w")
        self.value = tk.Entry(self.currentFrame, width=22, font=("arial", 15, "bold"), bd=3)
        self.value.grid(row=1, column=1, padx=10, pady=15)

        tk.Button(self.currentFrame, text="Search", command=self.searchFun,
                  bd=3, relief="raised", font=("Arial", 20, "bold"), width=18).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.currentFrame, text="❌ Back", command=self.close_current_frame,
                  bd=3, relief="raised", font=("Arial", 15, "bold"), width=12, bg="red", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

    def searchFun(self):
        opt = self.option.get()
        val = self.value.get().strip()
        if opt != "Select Option" and val:
            try:
                self.dbFun()
                query = f"SELECT * FROM books WHERE {opt} LIKE %s"
                self.cur.execute(query, (f"%{val}%",))
                data = self.cur.fetchall()
                self.table.delete(*self.table.get_children())
                if data:
                    for i in data:
                        self.table.insert('', tk.END, values=i)
                else:
                    messagebox.showinfo("Info", "No records found!")
                self.con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showerror("Error", "Please enter valid search criteria!")

    # -------------------- UPDATE BOOK --------------------
    def updateFrameFun(self):
        self.close_current_frame()
        self.currentFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#ffe082")
        self.currentFrame.place(width=450, height=280, x=400, y=140)

        tk.Label(self.currentFrame, text="Field:", font=("arial", 15, "bold"), bg="#ffe082").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.option = ttk.Combobox(self.currentFrame, width=20, values=("title", "author", "genre", "status"), font=("Arial", 15, "bold"))
        self.option.set("Select Field")
        self.option.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.currentFrame, text="New Value:", font=("arial", 15, "bold"), bg="#ffe082").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.value = tk.Entry(self.currentFrame, width=22, font=("arial", 15, "bold"), bd=3)
        self.value.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.currentFrame, text="Book ID:", font=("arial", 15, "bold"), bg="#ffe082").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.book_id = tk.Entry(self.currentFrame, width=22, font=("arial", 15, "bold"), bd=3)
        self.book_id.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.currentFrame, text="Update", command=self.updateFun,
                  bd=3, relief="raised", font=("Arial", 20, "bold"), width=18).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.currentFrame, text="❌ Back", command=self.close_current_frame,
                  bd=3, relief="raised", font=("Arial", 15, "bold"), width=12, bg="red", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

    def updateFun(self):
        field = self.option.get()
        val = self.value.get().strip()
        book_id = self.book_id.get()
        if field and val and book_id.isdigit():
            try:
                self.dbFun()
                self.cur.execute(f"UPDATE books SET {field}=%s WHERE id=%s", (val, int(book_id)))
                self.con.commit()
                messagebox.showinfo("Success", f"Book ID {book_id} updated!")
                self.showAll()
                self.close_current_frame()
                self.con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showerror("Error", "All fields are required!")

    # -------------------- SHOW ALL --------------------
    def showAll(self):
        try:
            self.dbFun()
            self.cur.execute("SELECT * FROM books")
            data = self.cur.fetchall()
            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('', tk.END, values=i)
            self.con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    # -------------------- DELETE BOOK --------------------
    def deleteFrameFun(self):
        self.close_current_frame()
        self.currentFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#ef9a9a")
        self.currentFrame.place(width=450, height=220, x=400, y=140)

        tk.Label(self.currentFrame, text="Book ID:", font=("arial", 15, "bold"), bg="#ef9a9a").grid(row=0, column=0, padx=20, pady=25, sticky="w")
        self.book_id = tk.Entry(self.currentFrame, width=22, font=("arial", 15, "bold"), bd=3)
        self.book_id.grid(row=0, column=1, padx=10, pady=25)

        tk.Button(self.currentFrame, text="Delete", command=self.deleteFun,
                  bd=3, relief="raised", font=("Arial", 20, "bold"), width=18).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.currentFrame, text="❌ Back", command=self.close_current_frame,
                  bd=3, relief="raised", font=("Arial", 15, "bold"), width=12, bg="red", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

    def deleteFun(self):
        book_id = self.book_id.get()
        if book_id.isdigit():
            try:
                self.dbFun()
                self.cur.execute("DELETE FROM books WHERE id=%s", (int(book_id),))
                self.con.commit()
                messagebox.showinfo("Deleted", f"Book ID {book_id} deleted successfully!")
                self.showAll()
                self.close_current_frame()
                self.con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showerror("Error", "Enter valid Book ID!")


# -------------------- RUN APP --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
