
import os
print(os.getcwd())
import sync_to_central
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import threading
import time
import socket

root = tk.Tk()
root.title("Role-Based Healthcare Sync System")
root.geometry("800x700")

# Simulated user credentials (for demo purposes)
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "dr_smith": {"password": "doc123", "role": "Doctor"},
    "nurse_amy": {"password": "nurse123", "role": "Nurse"},
}

unsynced_records = []
online_status = tk.StringVar(value="Checking...")

# Function to check internet connectivity
def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False

# Thread function to monitor internet connection
def monitor_internet():
    while True:
        online_status.set("Online" if check_internet() else "Offline")
        time.sleep(2)

# Function to simulate sync process
def sync_data():
    if check_internet():
        for record in unsynced_records:
            synced_list.insert("", "end", values=record)
        unsynced_records.clear()
        unsynced_list.delete(*unsynced_list.get_children())
        messagebox.showinfo("Sync Complete", "All data has been synced successfully!")
    else:
        messagebox.showwarning("No Internet", "Internet not detected. Data remains unsynced.")
tk.Button(root, text="Sync to Central", command=sync_to_central, bg="#FF9800", fg="white").pack(pady=5)


# Function to save a record
def save_record(fields):
    values = [field.get() for field in fields]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if all(values):
        record = tuple(values + [timestamp])
        unsynced_records.append(record)
        unsynced_list.insert("", "end", values=record)
        for field in fields:
            field.delete(0, tk.END)
        messagebox.showinfo("Record Saved", "Data saved locally for syncing.")
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

# Dynamic form generator
def show_role_ui(role):
    login_frame.destroy()
    tk.Label(root, text=f"Logged in as {role}", font=("Arial", 14)).pack(pady=10)
    
    if role == "Admin":
        labels = ["Prescription", "Billing"]
    elif role == "Doctor":
        labels = ["Doctor Name", "Specialization", "Procedure"]
    elif role == "Nurse":
        labels = ["Patient Name", "Email", "Diagnosis"]
    else:
        labels = []

    frame = tk.Frame(root)
    frame.pack(pady=10)
    entries = []
    for i, label in enumerate(labels):
        tk.Label(frame, text=f"{label}:").grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(frame, width=30)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)

    tk.Button(root, text="Save Record", command=lambda: save_record(entries), bg="#4CAF50", fg="white").pack(pady=10)

    # Sync + Internet Monitor + Data Views
    tk.Label(root, text="Internet Status:", font=("Arial", 12)).pack()
    tk.Label(root, textvariable=online_status, font=("Arial", 12, "bold"), fg="red").pack(pady=5)

    tk.Label(root, text="Unsynced Records", font=("Arial", 12)).pack(pady=5)
    columns = labels + ["Timestamp"]
    global unsynced_list, synced_list
    unsynced_list = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        unsynced_list.heading(col, text=col)
        unsynced_list.column(col, width=150)
    unsynced_list.pack(pady=10, fill="x", padx=10)

    tk.Button(root, text="Sync Data", command=sync_data, bg="#2196F3", fg="white").pack(pady=10)

    tk.Label(root, text="Synced Records", font=("Arial", 12)).pack(pady=5)
    synced_list = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        synced_list.heading(col, text=col)
        synced_list.column(col, width=150)
    synced_list.pack(pady=10, fill="x", padx=10)

    thread = threading.Thread(target=monitor_internet, daemon=True)
    thread.start()

# Login check
def login():
    username = username_entry.get()
    password = password_entry.get()
    user = USERS.get(username)
    if user and user["password"] == password:
        show_role_ui(user["role"])
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Main app


login_frame = tk.Frame(root)
login_frame.pack(pady=100)

tk.Label(login_frame, text="Login", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(login_frame, text="Username:").grid(row=1, column=0, padx=10, pady=5)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Label(login_frame, text="Password:").grid(row=2, column=0, padx=10, pady=5)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Button(login_frame, text="Login", command=login, bg="#2196F3", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
