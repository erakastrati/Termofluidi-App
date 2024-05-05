
import os
import sys
import shutil

import tkinter
from tkinter import *
from tkinter.ttk import Treeview, Combobox
from datetime import date, datetime
import sqlite3
from docxtpl import DocxTemplate
from num2words import num2words
from tkinter import OptionMenu, messagebox
from tkcalendar import DateEntry


def table_has_data(table_name):
    conn = sqlite3.connect('client_list.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def create_shitjet_table():
    conn = sqlite3.connect('client_list.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shitjet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategoria TEXT,
            data_shpenzimit TEXT,
            pershkrimi TEXT,
            cmimi REAL
        )
    ''')
    
    if not table_has_data("shitjet"):
        cursor.execute("INSERT INTO shitjet (kategoria, data_shpenzimit, pershkrimi, cmimi) VALUES (?, ?, ?, ?)", ("Initial Category", "2024-04-26", "Initial Description", 0.0))
        conn.commit()
    
    conn.close()

create_shitjet_table()

def create_borxhet_table():
    conn = sqlite3.connect('client_list.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borxhet (
            client_name TEXT,
            phone_number TEXT,
            borxh_description TEXT,
            borxh_amount REAL
        )
    ''')

    if not table_has_data("borxhet"):
        cursor.execute("INSERT INTO borxhet (client_name, phone_number, borxh_description, borxh_amount) VALUES (?, ?, ?, ?)", ("Initial Client", "Initial Phone", "Initial Description", 0.0))
        conn.commit()
    
    conn.close()

create_borxhet_table()

def create_clients_table():
    conn = sqlite3.connect('client_list.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            name TEXT,
            code TEXT,
            pvm TEXT,
            address TEXT
        )
    ''')

    if not table_has_data("clients"):
        cursor.execute("INSERT INTO clients (name, code, pvm, address) VALUES (?, ?, ?, ?)", ("Initial Name", "Initial Code", "Initial PVM", "Initial Address"))
        conn.commit()
    
    conn.close()

create_clients_table()


def update_list():
    try:
        conn = sqlite3.connect('client_list.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM clients")
        global client_list
        client_list = [row[0] for row in cursor.fetchall()]
        conn.commit()
    except sqlite3.Error as e:
        print("Error executing SQL query:", e)
    finally:
        conn.close()

update_list()


today = date.today()
no = 0

window = Tk()
window.title("TERMOFLUIDI")
frame = Frame(window)
frame.pack(padx=20, pady=10)


def clients_window():
    def add_client():
        name = name_entry.get()
        code = code_entry.get()
        pvm = pvm_entry.get()
        address = address_entry.get()

        conn = sqlite3.connect('client_list.db')
        c = conn.cursor()
        c.execute('INSERT INTO clients (name, code, pvm, address) VALUES (?, ?, ?, ?)',
                  (name, code, pvm, address))
        conn.commit()
        conn.close()

        tree.insert("", "end", values=(name, code, pvm, address))
        name_entry.delete(0, END)
        code_entry.delete(0, END)
        pvm_entry.delete(0, END)
        address_entry.delete(0, END)

    def load_clients_from_db():
        conn = sqlite3.connect('client_list.db')
        c = conn.cursor()
        c.execute('SELECT name, code, pvm, address FROM clients')
        records = c.fetchall()

        for i in tree.get_children():
            tree.delete(i)

        for record in records:
            tree.insert("", "end", values=record)

    def delete_client():
        try:
            selected_item = tree.selection()[0]  # Get selected item
            values = tree.item(selected_item, "values")
            name, code, pvm, address = values

            conn = sqlite3.connect('client_list.db')
            c = conn.cursor()
            c.execute('DELETE FROM clients WHERE name=? AND code=? AND pvm=? AND address=?',
                      (name, code, pvm, address))
            conn.commit()
            conn.close()

            tree.delete(selected_item)
            tkinter.messagebox.showinfo("Success", "Klient u fshi me sukses.")
        except IndexError:
            tkinter.messagebox.showerror("Error", "Please select a client to delete.")

    new_window = tkinter.Toplevel(window)
    new_window.title("Menaxhimi i klientëve")

    frame_clients = Frame(new_window)
    frame_clients.pack(padx=20, pady=10)

    name_label = Label(frame_clients, text="Klienti")
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry = Entry(frame_clients, width=20)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    code_label = Label(frame_clients, text="Numri i telefonit")
    code_label.grid(row=1, column=0, padx=10, pady=10)
    code_entry = Entry(frame_clients, width=20)
    code_entry.grid(row=1, column=1, padx=10, pady=10)

    pvm_label = Label(frame_clients, text="Adresa")
    pvm_label.grid(row=2, column=0, padx=10, pady=10)
    pvm_entry = Entry(frame_clients, width=20)
    pvm_entry.grid(row=2, column=1, padx=10, pady=10)

    address_label = Label(frame_clients, text="Shenim")
    address_label.grid(row=3, column=0, padx=10, pady=10)
    address_entry = Entry(frame_clients, width=20)
    address_entry.grid(row=3, column=1, padx=10, pady=10)

    add_client_button = Button(frame_clients, text="Shto Klient", command=add_client)
    add_client_button.grid(row=4, column=0, columnspan=2, pady=10)

    delete_client_button = Button(frame_clients, text="Fshij Klient", command=delete_client)
    delete_client_button.grid(row=4, column=1, columnspan=2, pady=10)

    columns_clients = ("Klienti", "Numri i telefonit", "Adresa", "Shenim")
    tree = Treeview(frame_clients, columns=columns_clients, show="headings")

    tree.column("Klienti", width=100)
    tree.column("Numri i telefonit", width=100)
    tree.column("Adresa", width=100)
    tree.column("Shenim", width=200)

    tree.heading("Klienti", text="Name")
    tree.heading("Numri i telefonit", text="Code")
    tree.heading("Adresa", text="PVM")
    tree.heading("Shenim", text="Address")

    tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    load_clients_from_db()

clients_button = tkinter.Button(frame, text="KLIENTET", command=clients_window)
clients_button.grid(row=0, column=1)

def clear_item():
    description.delete(0, tkinter.END)
    qty.delete(0, tkinter.END)
    qty.insert(0, "1")
    price.delete(0, tkinter.END)
    price.insert(0, "0.0")


folder_path_invoices = "Faturat"

if not os.path.exists(folder_path_invoices):
    try:
        os.makedirs(folder_path_invoices)
    except OSError as e:
        print(f"Error creating directory '{folder_path_invoices}': {e}")


def get_next_invoice_id():
    try:
        files = os.listdir(folder_path_invoices)
        highest_id = 0

        for file in files:
            if file.startswith("fatura_") and file.endswith(".docx"):
                file_id = int(file.split("_")[1].split(".")[0])
                if file_id > highest_id:
                    highest_id = file_id

        if highest_id == 0:
            return "00001"

        next_id = highest_id + 1

        return str(next_id).zfill(5)
    except OSError as e:
        print(f"Error accessing directory: {e}")
        return "00001"
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def translate_month(month):
    translations = {
        "January": "Janar",
        "February": "Shkurt",
        "March": "Mars",
        "April": "Prill",
        "May": "Maj",
        "June": "Qershor",
        "July": "Korrik",
        "August": "Gusht",
        "September": "Shtator",
        "October": "Tetor",
        "November": "Nëntor",
        "December": "Dhjetor"
    }
    return translations.get(month, month)

def translate_date(date_str):
    parts = date_str.split()
    if len(parts) == 3:
        day, month, year = parts
        translated_month = translate_month(month)
        return f"{day} {translated_month} {year}"
    return date_str


def generate_invoice():
    invoice_template_path = resource_path("invoice_template.docx")
    doc = DocxTemplate(invoice_template_path)

    invoice_year2 = date_entry.get()
    car2 = car_entry.get()
    
    # Calculate sum
    sum2 = sum(float(item[5]) for item in invoice_list)
    
    # Calculate TVSH (pvm)
    pvm2 = sum2 * 0.09
    
    # Calculate sum without TVSH
    sum_without_tvsh = sum2 - pvm2
    
    # Calculate total
    total = sum2
    
    # Convert total to words
    numbers2words = num2words(total, to='currency', lang='lt')
    client_name = client.get()

    date_str = translate_date(date.today().strftime("%d %B %Y"))
    invoice_id = get_next_invoice_id()

    doc.render({
        "invoice_year": invoice_year2[2:4],
        "date": date_str,
        "invoice_id": invoice_id,
        "car": car2,
        "invoice_list": invoice_list,
        "sum_without_tvsh": "{:.2f}".format(sum_without_tvsh),  # Display sum without TVSH
        "pvm": "{:.2f}".format(pvm2),
        "total": "{:.2f}".format(total),
        "company_name": client_name,
        "sum_in_words": numbers2words
    })

    client_name_for_filename = client_name.replace(" ", "_")
    
    file_name = f"fatura_{invoice_id}_{client_name_for_filename}.docx"
    file_path = os.path.join(folder_path_invoices, file_name)
    
    doc.save(file_path)
    messagebox.showinfo("Informata", f"Fatura {client_name}-{invoice_id}.docx u krijua")


invoice_list = []

def add_item():
    global no
    description2 = description.get()
    qty2 = int(qty.get())
    price2 = float(price.get())
    sum = "{:.2f}".format(qty2 * price2)
    no += 1
    invoice_item = [no, description2, car_entry.get(), "cope", qty2, price2, sum]

    tree.insert('', tkinter.END, values=invoice_item)
    clear_item()
    invoice_list.append(invoice_item)

def new_invoice():
    car_entry.delete(0, tkinter.END)
    clear_item()
    tree.delete(*tree.get_children())
    invoice_list.clear()

description_label = Label(frame, text="Artikulli")
description_label.grid(row=4, column=2)
description = Entry(frame, width=27)
description.grid(row=5,column=2)

faturaid_label = Label(frame, text="Fatura ID")
faturaid_label.grid(row=4, column=1)
faturaid = Entry(frame, width=32)
faturaid.grid(row=5, column=1)
faturaid.insert(0, get_next_invoice_id()) 

qty_label = Label(frame, text="Sasia")
qty_label.grid(row=6, column=1)
qty = Spinbox(frame, from_=1, to=2000, increment=1)
qty.grid(row=7,column=1, padx=30)

price_label = Label(frame, text="Çmimi €")
price_label.grid(row=6, column=2)
price = Spinbox(frame, from_=0.0, to=15000, increment=1, format='%1.2f')
price.grid(row=7,column=2)

add_button = Button(frame, text="Shto artikull", command=add_item, bg="light green")
add_button.grid(row=9, column=3)

date_label = Label(frame, text="Data")
date_label.grid(row=4, column=0)
date_entry = Entry(frame)
date_entry.insert(0, today)
date_entry.grid(row=5,column=0)

client_label = Label(frame, text="Klienti")
client_label.grid(row=2, column=0, columnspan=3)


client = StringVar()
client.set(" ")
update_list()
if client_list:
    client.set(client_list[0])
else:
    client.set(" ")

try:
    client_drop = OptionMenu(frame, client, *client_list)
    client_drop.grid(row=3, column=0, columnspan=3, padx=30)
    client_drop.config(width=50)
except Exception as e:
    print("Error initializing OptionMenu:", e)

print("Client Value:", client.get())


print("Client Value:", client.get())
spacer_frame = Frame(frame, height=20, width=2)
spacer_frame.grid(row=3, column=0)

car_label = Label(frame, text="Përshkrimi i produktit")
car_label.grid(row=6, column=0)
car_entry = Entry(frame, width=20)
car_entry.grid(row=7, column=0)


spacer_frame = Frame(frame, height=20, width=2)
spacer_frame.grid(row=1, column=1)

columns = ('ID', 'Artikulli', 'Përshkrimi', 'Sasia', 'Çmimi', 'Shuma')
tree = Treeview(frame, columns=columns, show="headings")
tree.column("ID", width=60)
tree.column("Artikulli", width=300)
tree.column("Përshkrimi", width=150)  # Adjust width as needed
tree.column("Sasia", width=100)
tree.column("Çmimi", width=100)
tree.column("Shuma", width=100)
tree.heading('ID', text='ID')
tree.heading('Artikulli', text='Artikulli')
tree.heading('Përshkrimi', text='Përshkrimi')
tree.heading('Sasia', text="Sasia")
tree.heading('Çmimi', text="Çmimi")
tree.heading('Shuma', text="Shuma")
tree.grid(row=10, column=0, columnspan=4, padx=20, pady=10)

save_invoice_button = Button(frame, text="RUAJ FATURËN", command=generate_invoice)
save_invoice_button.grid(row=11, column=0, columnspan=4, sticky="news", padx=20, pady=5)
new_invoice_button = Button(frame, text="PASTRO", command=new_invoice)
new_invoice_button.grid(row=12, column=0, columnspan=4, sticky="news", padx=20, pady=5)

folder_path_fletpagesat = "Fletepagesat"

if not os.path.exists(folder_path_fletpagesat):
    os.makedirs(folder_path_fletpagesat)

def get_next_fletepagesa_id():
    files = os.listdir(folder_path_fletpagesat)
    highest_id = 0

    for file in files:
        if file.startswith("fletepagesa_") and file.endswith(".docx"):
            file_id = int(file.split("_")[1].split(".")[0])
            if file_id > highest_id:
                highest_id = file_id

    next_id = highest_id + 1

    return str(next_id).zfill(5)


def fletepagesa_window():
    new_window = Toplevel(window)
    new_window.title("FLETËPAGESA")

    frame_fp = Frame(new_window)
    frame_fp.pack(padx=30, pady=30)

    fletepagesa_id_label = Label(frame_fp, text="Fletepagesa ID")
    fletepagesa_id_label.grid(row=0, column=0, padx=10, pady=10)
    fletepagesa_id = get_next_fletepagesa_id()
    fletepagesa_id_entry = Entry(frame_fp, width=20)
    fletepagesa_id_entry.grid(row=0, column=1, padx=10, pady=10)
    fletepagesa_id_entry.insert(0, fletepagesa_id)
    fletepagesa_id_entry.config(state="readonly")

    client_label = Label(frame_fp, text="Zgjedhni klientin")
    client_label.grid(row=1, column=0, padx=10, pady=10)

    client_dropdown = OptionMenu(frame_fp, client, *client_list)
    client_dropdown.grid(row=1, column=1, padx=10, pady=10)
    client_dropdown.config(width=30)

    adresa_label = Label(frame_fp, text="Adresa")
    adresa_label.grid(row=2, column=0, padx=10, pady=10)

    adresa_entry = Entry(frame_fp, width=20)
    adresa_entry.grid(row=2, column=1, padx=10, pady=10)

    phone_label = Label(frame_fp, text="Numri i telefonit")
    phone_label.grid(row=3, column=0, padx=10, pady=10)

    phone_entry = Entry(frame_fp, width=20)
    phone_entry.grid(row=3, column=1, padx=10, pady=10)

    cmimi_label = Label(frame_fp, text="Çmimi")
    cmimi_label.grid(row=4, column=0, padx=10, pady=10)

    cmimi_entry = Entry(frame_fp, width=10)
    cmimi_entry.grid(row=4, column=1, padx=10, pady=10)

    generate_fletepagesa_button = Button(frame_fp, text="RUAJ FLETEPAGESEN", command=lambda: generate_fletepagesa(adresa_entry.get(), phone_entry.get(), cmimi_entry.get(), client.get(), client.get(), adresa_entry.get(), fletepagesa_id))

    generate_fletepagesa_button.grid(row=5, column=0, columnspan=2, pady=10)

    fletepagesa_id_entry.insert(0, fletepagesa_id)

add_fletepagesa_button = Button(frame, text="FLETËPAGESA", command=fletepagesa_window)
add_fletepagesa_button.grid(row=0, column=2)


folder_path_fletpagesat = "Fletepagesat"

if not os.path.exists(folder_path_fletpagesat):
    os.makedirs(folder_path_fletpagesat)

def generate_fletepagesa(adresa, phone_number, cmimi, client_name, client_code, client_address, fletepagesa_id):
    print("Inside generate_fletepagesa function")
    
    fletepagesa_template_path = resource_path("fletepagesa_template.docx")

    doc = DocxTemplate(fletepagesa_template_path)

    client_name_for_filename = client_name.replace(" ", "_")
    cmimi = "{:.2f}".format(float(cmimi))

    doc.render({
        "adresa": adresa,
        "phone_number": phone_number,
        "cmimi": cmimi,
        "client_name": client_name,
        "client_code": client_code,
        "client_address": client_address,
        "fletepagesa_id": fletepagesa_id.zfill(5),
        "date": date.today().strftime("%Y-%m-%d")
    })

    file_name = f"fletepagesa_{fletepagesa_id}_{client_name_for_filename}.docx"
    file_path = os.path.join(folder_path_fletpagesat, file_name)  
    doc.save(file_path)
    messagebox.showinfo("Informata", f"Fletepagesa {client_name}-{fletepagesa_id}.docx u krijua")



def shitjet_window():
    def add_shitje():
        
        kategoria = kategoria_combobox.get()
        data = data_calendar.get()
        pershkrimi = pershkrimi_entry.get()
        cmimi = cmimi_entry.get()

        conn = sqlite3.connect('client_list.db')
        c = conn.cursor()

        c.execute('INSERT INTO shitjet (kategoria, data_shpenzimit, pershkrimi, cmimi) VALUES (?, ?, ?, ?)',
                (kategoria, data, pershkrimi, cmimi))

        conn.commit()
        conn.close()
        tree.insert("", "end", values=(kategoria, data, pershkrimi, cmimi))
        cmimi_entry.delete(0, END)
        kategoria_combobox.set("Zgjidhni një kategori")
        pershkrimi_entry.delete(0, END)

    def load_shitjet_from_db():
        conn = sqlite3.connect('client_list.db')
        c = conn.cursor()
        c.execute('SELECT kategoria, data_shpenzimit, pershkrimi, cmimi FROM shitjet')
        records = c.fetchall()

        for i in tree.get_children():
            tree.delete(i) 

        for record in records:
            formatted_cmimi = "{:.2f}".format(record[3])
            tree.insert("", "end", values=(record[0], record[1], record[2], formatted_cmimi))

    def delete_shitje():
        try:
            selected_item = tree.selection()[0]  # Get selected item
            values = tree.item(selected_item, "values")
            kategoria, data, pershkrimi, cmimi = values

            conn = sqlite3.connect('client_list.db')
            c = conn.cursor()
            c.execute('DELETE FROM shitjet WHERE kategoria=? AND data_shpenzimit=? AND pershkrimi=? AND cmimi=?',
                      (kategoria, data, pershkrimi, cmimi))
            conn.commit()
            conn.close()

            tree.delete(selected_item)
            tkinter.messagebox.showinfo("Success", "Shpenzimi u fshi me sukses.")
        except IndexError:
            tkinter.messagebox.showerror("Error", "Ju lutem zgjidhni një shpenzim për të fshirë.")

    new_window = tkinter.Toplevel(window)
    new_window.title("SHPENZIMET")

    frame_shitjet = Frame(new_window)
    frame_shitjet.pack(padx=20, pady=10)


    cmimi_label = Label(frame_shitjet, text="Cmimi")
    cmimi_label.grid(row=3, column=0, padx=10, pady=10)
    cmimi_entry = Entry(frame_shitjet, width=20)
    cmimi_entry.grid(row=3, column=1, padx=10, pady=10)


    kategoria_label = Label(frame_shitjet, text="Kategoria")
    kategoria_label.grid(row=0, column=0, padx=10, pady=10)
    kategoria_options = ["Pagesa e punetoreve", "Nafta", "Ushqim", "Mjet pune", "Tjeter"]
    kategoria_combobox = Combobox(frame_shitjet, values=kategoria_options, width=17)
    kategoria_combobox.grid(row=0, column=1, padx=10, pady=10)
    kategoria_combobox.set("Zgjidhni një kategori")


    data_label = Label(frame_shitjet, text="Data e shpenzimit")
    data_label.grid(row=2, column=0, padx=10, pady=10)
    data_calendar = DateEntry(frame_shitjet, width=18, background='darkblue', foreground='white', borderwidth=2)
    data_calendar.grid(row=2, column=1, padx=10, pady=10)


    pershkrimi_label = Label(frame_shitjet, text="Pershkrimi")
    pershkrimi_label.grid(row=1, column=0, padx=10, pady=10)
    pershkrimi_entry = Entry(frame_shitjet, width=20)
    pershkrimi_entry.grid(row=1, column=1, padx=10, pady=10)

    delete_shitje_button = Button(frame_shitjet, text="Fshij", command=delete_shitje)
    delete_shitje_button.grid(row=4, column=1, columnspan=2, pady=10)

    add_shitje_button = Button(frame_shitjet, text="Shto Shpenzim", command=add_shitje)
    add_shitje_button.grid(row=4, column=0, columnspan=2, pady=10)


    columns_shitje = ("Kategoria", "Pershkrimi", "Data", "Cmimi")

    tree = Treeview(frame_shitjet, columns=columns_shitje, show="headings")

    tree.column("Kategoria", width=100)
    tree.column("Pershkrimi", width=200)
    tree.column("Data", width=100)
    tree.column("Cmimi", width=100)

    tree.heading("Kategoria", text="Kategoria")
    tree.heading("Pershkrimi", text="Pershkrimi")
    tree.heading("Data", text="Data")
    tree.heading("Cmimi", text="Cmimi")

    tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    load_shitjet_from_db()




add_shitjet_button = tkinter.Button(frame, text="SHPENZIMET", command=shitjet_window)
add_shitjet_button.grid(row=0, column=3)

def ballina_window():
    def apply_date_filters():
        from_date = from_date_entry.get()
        to_date = to_date_entry.get()

        if not (from_date and to_date):
            messagebox.showerror("Error", "Please select both 'From' and 'To' dates.")
            return

        def get_cmimi_for_category_with_date_filter(category, from_date, to_date):
            conn = sqlite3.connect('client_list.db')
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(cmimi) FROM shitjet WHERE kategoria = ? AND data_shpenzimit BETWEEN ? AND ?",
                           (category, from_date, to_date))
            total_cmimi = cursor.fetchone()[0] or 0
            conn.close()
            return total_cmimi

        for widget in frame_ballina.winfo_children():
            widget.destroy()

        total_clients_label = Label(frame_ballina, text=f"Numri i klientëve: {get_total_clients()}")
        total_clients_label.pack(pady=10)

        total_cmimi_label = Label(frame_ballina, text=f"Shuma totale e shpenzimeve: {get_total_cmimi():,.2f} €")
        total_cmimi_label.pack(pady=10)

        date_range_label = Label(frame_ballina, text=f"Data prej: {from_date}   Data deri: {to_date}")
        date_range_label.pack()

        categories = ["Pagesa e punetoreve", "Nafta", "Ushqim", "Mjet pune", "Tjeter"]

        for category in categories:
            category_cmimi = get_cmimi_for_category_with_date_filter(category, from_date, to_date)
            formatted_cmimi = "{:.2f}".format(category_cmimi)
            cmimi_label = Label(frame_ballina, text=f"{category}: {formatted_cmimi} €")
            cmimi_label.pack()

    new_window = tkinter.Toplevel(window)
    new_window.title("BALLINA")

    frame_ballina = Frame(new_window)
    frame_ballina.pack(padx=20, pady=10)

    def get_total_clients():
        conn = sqlite3.connect('client_list.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clients")
        total_clients = cursor.fetchone()[0]
        conn.close()
        return total_clients

    def get_total_cmimi():
        conn = sqlite3.connect('client_list.db')
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(cmimi) FROM shitjet")
        total_cmimi = cursor.fetchone()[0]
        conn.close()
        return total_cmimi

    total_clients_label = Label(frame_ballina, text=f"Numri i klientëve: {get_total_clients()}")
    total_clients_label.pack(pady=10)

    total_cmimi_label = Label(frame_ballina, text=f"Shuma totale e shpenzimeve: {get_total_cmimi():,.2f} €")
    total_cmimi_label.pack(pady=10)

    from_date_label = Label(frame_ballina, text="Data prej:")
    from_date_label.pack()

    from_date_entry = DateEntry(frame_ballina, width=12, background='darkblue', foreground='white', borderwidth=2)
    from_date_entry.pack()

    to_date_label = Label(frame_ballina, text="Data deri:")
    to_date_label.pack()

    to_date_entry = DateEntry(frame_ballina, width=12, background='darkblue', foreground='white', borderwidth=2)
    to_date_entry.pack()

    apply_filters_button = Button(frame_ballina, text="Filtro", command=apply_date_filters)
    apply_filters_button.pack(pady=10)

ballina_button = tkinter.Button(frame, text="BALLINA", command=ballina_window)
ballina_button.grid(row=0, column=0)


def borxhet_window():
    new_window = tkinter.Toplevel(window)
    new_window.title("BORXHET")
    
    frame_borxhet = Frame(new_window)
    frame_borxhet.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    frame_input = Frame(new_window)
    frame_input.pack(side=tkinter.RIGHT, padx=20, pady=10)
    
    update_list()
    
    klienti_label = tkinter.Label(frame_input, text="Klienti:")
    klienti_label.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.E)
    
    client_var = tkinter.StringVar()
    client_dropdown = tkinter.OptionMenu(frame_input, client_var, *client_list)
    client_dropdown.config(width=25)
    client_dropdown.grid(row=0, column=1, padx=10, pady=10)

    phone_label = tkinter.Label(frame_input, text="Numri i telefonit:")
    phone_label.grid(row=1, column=0, padx=10, pady=10, sticky=tkinter.E)
    phone_entry = tkinter.Entry(frame_input, width=30)
    phone_entry.grid(row=1, column=1, padx=10, pady=10)

    borxh_description_label = tkinter.Label(frame_input, text="Pershkrimi i borxhit:")
    borxh_description_label.grid(row=2, column=0, padx=10, pady=10, sticky=tkinter.E)
    borxh_description_entry = tkinter.Entry(frame_input, width=30)
    borxh_description_entry.grid(row=2, column=1, padx=10, pady=10)

    borxh_amount_label = tkinter.Label(frame_input, text="Shuma e borxhit:")
    borxh_amount_label.grid(row=3, column=0, padx=10, pady=10, sticky=tkinter.E)
    borxh_amount_entry = tkinter.Entry(frame_input, width=30)
    borxh_amount_entry.grid(row=3, column=1, padx=10, pady=10)

    def add_debt():
        client = client_var.get()
        phone = phone_entry.get()
        borxh_description = borxh_description_entry.get()
        borxh_amount = borxh_amount_entry.get()

        conn = sqlite3.connect('client_list.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO borxhet (client_name, phone_number, borxh_description, borxh_amount) VALUES (?, ?, ?, ?)",
                       (client, phone, borxh_description, float(borxh_amount)))
        conn.commit()
        conn.close()

        update_debts_table()

        client_var.set('')
        phone_entry.delete(0, tkinter.END)
        borxh_description_entry.delete(0, tkinter.END)
        borxh_amount_entry.delete(0, tkinter.END)

    add_button = tkinter.Button(frame_input, text="Shto", command=add_debt)
    add_button.grid(row=4, column=1, pady=10)

    columns = ('Klienti', 'Numri i telefonit', 'Pershkrimi', 'Shuma e borxhit')
    debts_table = tkinter.ttk.Treeview(frame_borxhet, columns=columns, show="headings")
    for col in columns:
        debts_table.heading(col, text=col.title())
    debts_table.pack(fill=tkinter.BOTH, expand=True)

    def update_debts_table():
        for row in debts_table.get_children():
            debts_table.delete(row)

        conn = sqlite3.connect('client_list.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM borxhet")
        for row in cursor.fetchall():
            formatted_row = list(row)
            formatted_row[-1] = "{:.2f}".format(formatted_row[-1])
            debts_table.insert('', 'end', values=formatted_row)
        conn.close()

    update_debts_table()


    def delete_debt():
        selected_item = debts_table.selection()[0]
        item_values = debts_table.item(selected_item, 'values')
        conn = sqlite3.connect('client_list.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM borxhet WHERE client_name=? AND phone_number=? AND borxh_description=? AND borxh_amount=?", item_values)
        conn.commit()
        conn.close()
        debts_table.delete(selected_item)

    delete_button = tkinter.Button(frame_input, text="Fshij", command=delete_debt)
    delete_button.grid(row=4, column=0, pady=10)

borxhet_button = tkinter.Button(frame, text="BORXHET", command=borxhet_window)
borxhet_button.grid(row=0, column=4)

window.mainloop()
