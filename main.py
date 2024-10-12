import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

# Data file
DATA_FILE = 'finance_data.csv'

# Create the main window
root = tk.Tk()
root.title("Kişisel Bitcoin Asistanı")
root.geometry("400x400")

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=['islem', 'Miktar', 'Kredi Kartı']).to_csv(DATA_FILE, index=False)

# Function to add a financial record
def add_record():
    record_type = record_type_var.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if not amount:
        messagebox.showwarning("Uyarı", "Lütfen bir miktar girin.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Uyarı", "Miktar geçerli bir sayı olmalıdır.")
        return

    # Add to the dataframe
    new_record = pd.DataFrame([[record_type, amount, description]], columns=['islem', 'Miktar', 'Kredi Kartı'])
    new_record.to_csv(DATA_FILE, mode='a', header=False, index=False)

    messagebox.showinfo("Başarılı", "Kayıt eklendi.")
    clear_entries()
    load_data()

# Function to load and display data
def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
        for row in tree.get_children():
            tree.delete(row)
        for index, record in df.iterrows():
            tree.insert("", "end", values=(record['islem'], record['Miktar'], record['Kredi Kartı']))
    except Exception as e:
        messagebox.showerror("Hata", f"Veri yüklenirken hata oluştu: {e}")

# Function to clear input fields
def clear_entries():
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

# UI Elements
record_type_var = tk.StringVar(value='Alım')

record_type_label = tk.Label(root, text="Kayıt Türü:")
record_type_label.pack(pady=5)

record_type_frame = tk.Frame(root)
record_type_frame.pack(pady=5)

income_radio = ttk.Radiobutton(record_type_frame, text='Alım', variable=record_type_var, value='Alım')
expense_radio = ttk.Radiobutton(record_type_frame, text='Satım', variable=record_type_var, value='Satım')
income_radio.pack(side='left')
expense_radio.pack(side='left')

amount_label = tk.Label(root, text="Miktar")
amount_label.pack(pady=5)

amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)

description_label = tk.Label(root, text="Kredi Kartı")
description_label.pack(pady=5)

description_entry = tk.Entry(root)
description_entry.pack(pady=5)

add_button = ttk.Button(root, text="Kaydet", command=add_record)
add_button.pack(pady=10)

# Treeview for displaying records
tree = ttk.Treeview(root, columns=('Type', 'Amount', 'Description'), show='headings')
tree.heading('Type', text='Alım-Satım')
tree.heading('Amount', text='Bitcoin Miktarı')
tree.heading('Description', text='Kredi Kartı Numarası')
tree.pack(pady=10)

load_data()

# Run the application
root.mainloop()
