
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database
conn = sqlite3.connect("Marie_Depalubos.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Marie_Depalubos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    city TEXT NOT NULL,
    age INTEGER NOT NULL,
    occupation TEXT NOT NULL
)
""")
conn.commit()


# Add Data
def add_data():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    city = city_entry.get()
    age = age_entry.get()
    occupation = occupation_entry.get()

    if not all([name, email, phone, city, age, occupation]):
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        age = int(age)
        if age <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid age.")
        return

    cursor.execute("""
        INSERT INTO Marie_Depalubos
        (full_name, email, phone, city, age, occupation)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, phone, city, age, occupation))

    conn.commit()
    display_data()
    clear_fields()
    messagebox.showinfo("Success", "Data added successfully!")


# Display Data
def display_data():
    for item in table.get_children():
        table.delete(item)

    cursor.execute("SELECT * FROM Marie_Depalubos")
    records = cursor.fetchall()

    for record in records:
        table.insert("", tk.END, values=record)

    count_records()


# Select Data
def select_data(event):
    selected = table.selection()

    if selected:
        record = table.item(selected[0], "values")
        clear_fields()

        name_entry.insert(0, record[1])
        email_entry.insert(0, record[2])
        phone_entry.insert(0, record[3])
        city_entry.insert(0, record[4])
        age_entry.insert(0, record[5])
        occupation_entry.insert(0, record[6])


# Update Data
def update_data():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a record.")
        return

    record_id = table.item(selected[0], "values")[0]

    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    city = city_entry.get()
    age = age_entry.get()
    occupation = occupation_entry.get()

    if not all([name, email, phone, city, age, occupation]):
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        age = int(age)
        if age <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid age.")
        return

    cursor.execute("""
        UPDATE Marie_Depalubos
        SET full_name=?, email=?, phone=?, city=?, age=?, occupation=?
        WHERE id=?
    """, (name, email, phone, city, age, occupation, record_id))

    conn.commit()
    display_data()
    clear_fields()
    messagebox.showinfo("Success", "Data updated successfully!")


# Delete Data
def delete_data():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a record.")
        return

    confirm = messagebox.askyesno(
        "Confirm",
        "Do you want to delete this record?"
    )

    if confirm:
        record_id = table.item(selected[0], "values")[0]

        cursor.execute(
            "DELETE FROM Marie_Depalubos WHERE id=?",
            (record_id,)
        )
        conn.commit()

        display_data()
        clear_fields()
        messagebox.showinfo("Success", "Data deleted successfully!")


# Search Data
def search_data():
    keyword = search_entry.get().strip()

    for item in table.get_children():
        table.delete(item)

    cursor.execute("""
        SELECT * FROM Marie_Depalubos
        WHERE full_name LIKE ?
        OR email LIKE ?
        OR phone LIKE ?
        OR city LIKE ?
        OR CAST(age AS TEXT) LIKE ?
        OR occupation LIKE ?
    """, tuple(["%" + keyword + "%"] * 6))

    records = cursor.fetchall()

    for record in records:
        table.insert("", tk.END, values=record)

    if not records:
        messagebox.showinfo("Search", "No records found.")


# Clear Fields
def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    occupation_entry.delete(0, tk.END)

    for item in table.selection():
        table.selection_remove(item)


# Count Records
def count_records():
    cursor.execute("SELECT COUNT(*) FROM Marie_Depalubos")
    total = cursor.fetchone()[0]
    total_label.config(text="Total Records: " + str(total))


# Main Window
root = tk.Tk()
root.title("Marie Depalubos Information System")
root.geometry("1100x650")
root.configure(bg="lightgray")

title = tk.Label(
    root,
    text="MARIE DEPALUBOS INFORMATION SYSTEM",
    font=("Arial", 18, "bold"),
    bg="lightblue",
    pady=15
)
title.pack(fill="x")

# Input Form
form = tk.LabelFrame(
    root,
    text="Personal Information",
    padx=10,
    pady=10,
    bg="lightgray"
)
form.pack(fill="x", padx=15, pady=10)

tk.Label(form, text="Full Name:", bg="lightgray").grid(
    row=0, column=0, padx=5, pady=5
)
name_entry = tk.Entry(form, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form, text="Email:", bg="lightgray").grid(
    row=1, column=0, padx=5, pady=5
)
email_entry = tk.Entry(form, width=30)
email_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form, text="Phone:", bg="lightgray").grid(
    row=2, column=0, padx=5, pady=5
)
phone_entry = tk.Entry(form, width=30)
phone_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(form, text="City:", bg="lightgray").grid(
    row=0, column=2, padx=5, pady=5
)
city_entry = tk.Entry(form, width=30)
city_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(form, text="Age:", bg="lightgray").grid(
    row=1, column=2, padx=5, pady=5
)
age_entry = tk.Entry(form, width=30)
age_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Label(form, text="Occupation:", bg="lightgray").grid(
    row=2, column=2, padx=5, pady=5
)
occupation_entry = tk.Entry(form, width=30)
occupation_entry.grid(row=2, column=3, padx=5, pady=5)

# Buttons
buttons = tk.Frame(root, bg="lightgray")
buttons.pack(pady=5)

tk.Button(buttons, text="ADD", width=12, command=add_data).grid(
    row=0, column=0, padx=5
)
tk.Button(buttons, text="UPDATE", width=12, command=update_data).grid(
    row=0, column=1, padx=5
)
tk.Button(buttons, text="DELETE", width=12, command=delete_data).grid(
    row=0, column=2, padx=5
)
tk.Button(buttons, text="CLEAR", width=12, command=clear_fields).grid(
    row=0, column=3, padx=5
)
tk.Button(buttons, text="DISPLAY ALL", width=12, command=display_data).grid(
    row=0, column=4, padx=5
)

# Search
search_frame = tk.Frame(root, bg="lightgray")
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search:", bg="lightgray").pack(side="left")

search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=5)

tk.Button(search_frame, text="SEARCH", command=search_data).pack(
    side="left", padx=5
)
tk.Button(search_frame, text="SHOW ALL", command=display_data).pack(
    side="left", padx=5
)

# Table
columns = (
    "ID", "Full Name", "Email", "Phone",
    "City", "Age", "Occupation"
)

table = ttk.Treeview(root, columns=columns, show="headings")

for column in columns:
    table.heading(column, text=column)
    table.column(column, width=140)

table.pack(fill="both", expand=True, padx=15, pady=10)
table.bind("<<TreeviewSelect>>", select_data)

# Total Records
total_label = tk.Label(
    root,
    text="Total Records: 0",
    font=("Arial", 11, "bold"),
    bg="lightgray"
)
total_label.pack(pady=5)

# Run Program
display_data()

def close_program():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_program)
root.mainloop()
