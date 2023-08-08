import tkinter as tk
import ttkbootstrap as ttk #untuk frame
from tkinter import messagebox
import pymongo
import datetime
from PIL import Image , ImageTk
from ttkbootstrap import Style
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
     FigureCanvasTkAgg)
import numpy as np
import seaborn as sns
from tkinter import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *

# Fungsi untuk menghubungkan ke MongoDB
def connect_to_mongodb():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        return client
    except pymongo.errors.ConnectionFailure:
        messagebox.showerror("Error", "Tidak dapat terhubung ke MongoDB.")
        return None

#buat window
window = ttk.Window()
window.title('FinWiz')
window.geometry('500x800')
window.configure(bg='#fff')
window.resizable(False,False)
window.iconbitmap('FinWiz.ico')
Style(theme="solar")
# l1=ttk.Label(window, text="FinWiz",font=('Century Gothic',30))
# l1.place(relx=0.5, rely=0.2,  anchor=tk.CENTER)
#---------------------------------------------------------------------------------------
# main page
def total():
    client = connect_to_mongodb()
    db = client["finwiz"]
    ttl_income = db["income"]
    ttl_outcome = db['outcome']
    total = [{"$match": {"Id": get_id()}},{"$group": {"_id": None, "total": {"$sum": "$nominal"}}}]
    incomee = ttl_income.aggregate(total)
    outcomee = ttl_outcome.aggregate(total)
    total_income = next(incomee, {}).get("total",0)
    total_outcome = next(outcomee, {}).get("total", 0)
    hasil = total_income-total_outcome
    return hasil
#frame income
def income_fr(window):
    global combo, nomin_entry, tgl_entry,ket_entry
    def on_entry_change(*args):
        try:
            input_number = float(nomin_entry.get().replace(".", "").replace(",", ""))
            formatted_number = format_number(input_number)
            nomin_entry.set(formatted_number)
        except ValueError:
            pass
    # main_fr.pack_forget()
    income_frame = ttk.Frame(window, width = 500, height = 800)
    income_frame.pack(padx=10, pady=10)
    jdudul = ttk.Label(income_frame, text='Pemasukan',font=('aileron', 20, 'bold'))
    jdudul.pack(pady= 20)
    # kategori
    kat = ttk.Label(income_frame, text='Kategori')
    kat.pack()

    items= ('Penghasilan','Bonus','Lainnya')
    combo= ttk.Combobox(income_frame, width= 28, font=('aileron', 12, 'bold'))
    combo.configure(values=items, font=('aileron', 12, 'bold'))
    combo.pack()

    # label nominal
    nomin = ttk.Label(income_frame, text='Nominal')
    nomin.pack()

    # entry nominal
    nomin_entry = ttk.StringVar()
    nomin_entry.trace_add("write", on_entry_change)
    nominal_entry = tk.Entry(income_frame, textvariable= nomin_entry, background='white', justify='center',width=30, font=('aileron', 12, 'bold'))
    nominal_entry.pack()

    # label tgl
    tgl_labl =ttk.Label(income_frame, text="Tanggal")
    tgl_labl.pack()
    # entry 
    tgl_entry = ttk.DateEntry(income_frame, width=35)
    tgl_entry.pack()

    # label ket
    ket_label = ttk.Label(income_frame, text="Keterangan")
    ket_label.pack()
    # entry ket
    ket = tk.StringVar()
    ket_entry = ttk.Entry(income_frame, textvariable=ket,justify='center',width=30, font=('aileron', 12, 'bold'))
    ket_entry.pack()
    
    income_button = ttk.Button(income_frame, text="Submit", command=entry_income, width=30,style='Outline.TButton')
    income_button.pack(pady=10)

    back_button = ttk.Button(income_frame, text="Back", command=back_to_main, width=30,style='Outline.TButton')
    back_button.pack(pady=10)

    



def entry_income():
    idi= get_id()
    kategori= combo.get()
    nominal= nomin_entry.get()
    tanggal= tgl_entry.entry.get()
    keterangan= ket_entry.get()
    transakssi = 'INCOME'
    if not nominal or not kategori or not tanggal:
        messagebox.showerror("Error", "Mohon isi kategori, nominal, dan tanggal")
        return
    nominal = nominal.replace('.', '')
    nominal = int(nominal)
    client =connect_to_mongodb()
    if client:
        db =client['finwiz']
        user_collection = db['income']

        income_data = {'Id':idi,
                        'kategori': kategori,
                        'nominal': nominal,
                        'tanggal': tanggal,
                        'keterangan': keterangan,
                        'TRANSAKSI' : transakssi
                        }
        user_collection.insert_one(income_data)
        input_history(idi,kategori, nominal,tanggal, keterangan, transakssi)
        messagebox.showinfo("Sukses", "Income Berhasil dimasukkan")
        back_to_main()


def get_id():
    client = connect_to_mongodb()
    if client:
        db = client['finwiz']
        user_collection = db['users']
        id_data = user_collection.find_one({"username": global_username}, {"_id": 0, "Id": 1})
        if id_data:
            return id_data['Id']
        else:
            return None
    return None


def input_history(idh,kategori,nominal,tanggal,keterangan,transaksi):
    client =connect_to_mongodb()
    if client:
        db =client['finwiz']
        user_collection = db['history']

        hist_data = {'Id':idh,
                        'kategori': kategori,
                        'nominal': f'Rp.{format_number(nominal)}',
                        'tanggal': tanggal,
                        'keterangan': keterangan,
                        'TRANSAKSI' : transaksi
                        }
        user_collection.insert_one(hist_data)

#frame outcome
def outcome_fr(window):
    global comboo, nominn_entry, tgll_entry,kett_entry
    def on_entry_change(*args):
        try:
            input_number = float(nominn_entry.get().replace(".", "").replace(",", ""))
            formatted_number = format_number(input_number)
            nominn_entry.set(formatted_number)
        except ValueError:
            pass
    outcome_frame = ttk.Frame(window, width = 500, height = 800)
    outcome_frame.pack(padx=10, pady=10)
    jdudul = ttk.Label(outcome_frame, text='Pengeluaran',font=('aileron', 20, 'bold'))
    jdudul.pack(pady= 20)
    # kategori
    katt = ttk.Label(outcome_frame, text='Kategori')
    katt.pack()
    itemss= ('makan & minum','bensin','hiburan','kesehatan','kecantikan','olaharaga','pakaian','tagihan','teknologi','transportasi','lainnya')
    comboo= ttk.Combobox(outcome_frame,width=28, font=('aileron', 12, 'bold'))
    comboo.configure(values=itemss, font=('aileron', 12, 'bold'))
    comboo.pack()
    # label nominal
    nominn = ttk.Label(outcome_frame, text='Nominal')
    nominn.pack()
    # entry nominal
    nominn_entry = ttk.StringVar()
    nominn_entry.trace_add("write", on_entry_change)
    nominnal_entry = tk.Entry(outcome_frame, textvariable= nominn_entry, background='white', justify='center',width=30, font=('aileron', 12, 'bold'))
    nominnal_entry.pack()

    # label tgl
    tgll_labl = ttk.Label(outcome_frame, text="Tanggal")
    tgll_labl.pack()
    # entry tgl
    tgll_entry = ttk.DateEntry(outcome_frame, width=35)
    tgll_entry.pack()

    # label ket
    kett_label = ttk.Label(outcome_frame, text="Keterangan")
    kett_label.pack()
    # entry ket
    kett = tk.StringVar()
    kett_entry = ttk.Entry(outcome_frame, textvariable=kett,justify='center',width=30, font=('aileron', 12, 'bold'))
    kett_entry.pack()

    outcome_button = ttk.Button(outcome_frame, text="Submit", command=entry_outcome, width=30,style='Outline.TButton')
    outcome_button.pack(pady=10)

    back_button = ttk.Button(outcome_frame, text="Back", command=back_to_main, width=30,style='Outline.TButton')
    back_button.pack(pady=10)

    

def entry_outcome():
    ide= get_id()
    kategorii= comboo.get()
    nominall= nominn_entry.get()
    tanggakll= tgll_entry.entry.get()
    keterangann= kett_entry.get()
    transaksii = 'OUTCOME'
    if not nominall or not kategorii or not tanggakll:
        messagebox.showerror("Error", "Mohon isi kategori, nominal, dan tanggal")
        return
    nominall = nominall.replace('.', '')
    nominall = int(nominall)
    client =connect_to_mongodb()
    if client:
        db =client['finwiz']
        user_collection = db['outcome']

        outcome_data = {'Id':ide,
                        'kategori': kategorii,
                        'nominal': nominall,
                        'tanggal': tanggakll,
                        'keterangan': keterangann,
                        'TRANSAKSI': transaksii
                        }
        user_collection.insert_one(outcome_data)
        messagebox.showinfo("Sukses", "Pengeluaran Berhasil dimasukkan")
        input_history(ide, kategorii, nominall, tanggakll, keterangann,transaksii)
        back_to_main()
    
def format_number(angka):
    return '{:,.0f}'.format(angka).replace(',', '.')

def reset_trans():
    result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete your transaction? This action cannot be undone.")
    if result:
        client = connect_to_mongodb()
        if client:
            db = client['finwiz']
            coll2 = db['history']
            coll3 = db['income']
            coll4 = db['outcome']
            coll2.delete_many({'Id': get_id()})
            coll3.delete_many({'Id': get_id()})
            coll4.delete_many({'Id': get_id()})
            # Perform any additional actions or notifications if needed
            messagebox.showinfo("Success", "Transaction deleted successfully.")
            back_to_main()



def main_page(window):
    # Hide the login/signup page
    
    main_fr =ttk.Frame(window, width = 500, height = 200)
    main_fr.pack()
    saldo_label = ttk.Label(main_fr, text='Saldo', font=('aileron', 12, 'bold'), width=500)
    saldo_label.pack(anchor = 'w')

    total_label = ttk.Label(main_fr, text=f'Rp. {format_number(total())},-', font=('aileron', 30))
    total_label.pack(pady = 30)

    reset_button = ttk.Button(main_fr, text="Reset Transaction", command= reset_trans, width= 40,style='danger.Link.TButton' ,cursor='hand2')
    reset_button.pack(pady=15)

    income_button = ttk.Button(main_fr, text="Pemasukan", command= change_frame_to_income, width= 40,style='Outline.TButton',cursor='hand2' )
    income_button.pack(pady=15)
    
    outcome_button = ttk.Button(main_fr, text="Pengeluaran", command= change_frame_to_outcom, width= 40,style='Outline.TButton',cursor='hand2' )
    outcome_button.pack(pady=15)

    history_button = ttk.Button(main_fr, text="History", command= change_frame_to_history, width= 40,style='Outline.TButton' ,cursor='hand2')
    history_button.pack(pady=15)

    logout_button = ttk.Button(main_fr, text="Logout", command= logout, width= 40,style='secondary.TButton' ,cursor='hand2')
    logout_button.pack(pady=15)
    
    del_button = ttk.Button(main_fr, text="Delete Account", command= del_account, width= 40,style='danger.Link.TButton' ,cursor='hand2')
    del_button.pack(pady=15)

def logout():
    for widget in window.winfo_children():
        if widget != fr_login and widget != fg_pw and widget != signup_frame:
            widget.destroy()
    show_login_page()

def del_account():
    # Prompt the user with a yes/no dialog to confirm the account deletion
    result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete your account? This action cannot be undone.")
    if result:
        client = connect_to_mongodb()
        if client:
            db = client['finwiz']
            coll1 = db['users']
            coll2 = db['history']
            coll3 = db['income']
            coll4 = db['outcome']
            coll2.delete_many({'Id': get_id()})
            coll3.delete_many({'Id': get_id()})
            coll4.delete_many({'Id': get_id()})
            coll1.delete_one({'Id': get_id()})
            # Perform any additional actions or notifications if needed
            messagebox.showinfo("Success", "Account deleted successfully.")
            logout()




def create_pie_chart(main_fr):
    # Connect to MongoDB and get the data
    client = connect_to_mongodb()
    db = client['finwiz']
    hl = db['outcome']
    total = hl.find({"Id": get_id()}, {"_id": 0, 'kategori': 1, 'nominal': 1})
    data_lisst = list(total)
    if len(data_lisst) == 0:
        data = {
            'kategori': ['None'],
            'nominal': [100]}

        # Membuat dataframe dari data
        df = pd.DataFrame(data)

    else:
        # Membuat data frame dari list data
        a = pd.DataFrame(data_lisst)
        df=pd.pivot_table(a,index='kategori', values='nominal', aggfunc=sum)
        df.reset_index(inplace = True)
        

    # Create the pie chart using Matplotlib

    px = 1/plt.rcParams['figure.dpi']
    plt.figure(figsize=(400*px, 400*px))
    plt.pie(df['nominal'], labels=df['kategori'], autopct='%1.1f%%', startangle=140, textprops={'color':'white', 'fontsize':8}, colors= sns.color_palette("flare"))
    # Menambahkan judul pada pie chart
    title = plt.title("Distribusi Kategori Pengeluaran Anda",fontsize= 12 )
    title.set_color('gold')
    title
    # Menampilkan pie chart
    fig = plt.gcf()
    fig.set_facecolor('none')
    plt.axis('equal')
    # Convert the Matplotlib figure to a Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=main_fr)
    canvas.draw()

    # Pack the canvas to display the pie chart
    canvas.get_tk_widget().pack(anchor='n')

def get_data_history():
    # Add data to the treeview
    client = connect_to_mongodb()
    db = client['finwiz']
    # tbl = db['income']
    # dbl = db['outcome']

    pipeline = [
        {"$match": {"Id": get_id()}},
        {"$project": {"_id": 0, "kategori": 1, "nominal": 1, "keterangan": 1, 'tanggal': 1, "TRANSAKSI": 1}}
    ]

    hist = db['history']
    historyy = hist.aggregate(pipeline)
    df = list(historyy)
    df = pd.DataFrame(df)
    df.sort_values(by='tanggal', inplace = True)
    df.insert(0, 'No', range(1,len(df)+1))
    kol_list = df.columns.tolist()
    row_list = df.values.tolist()
    return df,kol_list, row_list


def history(window):
    hist_frame = ttk.Frame(window)
    hist_frame.pack(padx=10)
    hist_label = ttk.Label(hist_frame, text='History', font=('aileron', 20, 'bold'))
    hist_label.pack()

    # Create a Treeview widget for the history table
    
    
    
    try:
        df, kol_list, row_list=get_data_history()
        tabel = Tableview(master= hist_frame,
                          coldata=kol_list,
                          rowdata=row_list,
                          paginated=True,
                          pagesize=10,
                          autofit=True,
                          searchable=True,
                          )
        tabel.pack(fill='both', expand=YES, padx=10)
        tabel.load_table_data()
        
    except:
        warn_label = ttk.Label(hist_frame, text='DATA NOT FOUND', font=('aileron', 20, 'bold'), width=500)
        warn_label.pack()
    
    back_button = ttk.Button(hist_frame, text="Back", command=back_to_main, width=15, style='Outline.TButton')
    back_button.pack(pady=10)

    canvas = ttk.Canvas(hist_frame, width=400, height=100)
    canvas.pack(expand=False, fill= 'both')
    create_pie_chart(hist_frame)

               

def change_frame_to_history():
    for widget in window.winfo_children():
        if widget != fr_login and widget != fg_pw and widget != signup_frame:
            widget.destroy()
    history(window)
        
def change_frame_to_income():
    for widget in window.winfo_children():
        if widget != fr_login and widget != fg_pw and widget != signup_frame:
            widget.destroy()
    income_fr(window)

def change_frame_to_outcom():
    for widget in window.winfo_children():
        if widget != fr_login and widget != fg_pw and widget != signup_frame:
            widget.destroy()
    outcome_fr(window)

def back_to_main():
    for widget in window.winfo_children():
        if widget != fr_login and widget != fg_pw and widget != signup_frame:
            widget.destroy()
    main_page(window)

#fungsi ke item page
def navigate_to_items_page():
    messagebox.showinfo("Sukses", "Login berhasil!")
    fr_login.pack_forget()
    clear_fields()
    main_page(window)
    py
# Fungsi untuk menghapus teks di input fields
def clear_fields():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


#fungsi untuk lupa password
    
def update_pw():
    idpw = id_entry_pw.get()
    usernamepw = username_pw.get()
    passwordpw = password_pw.get()
    kon_passwordpw = pw_con.get()
    if not idpw or not usernamepw or not passwordpw or not kon_passwordpw:
        messagebox.showerror("Error", "Mohon isi semua kolom.")
        return
    if len(passwordpw) < 6:
        messagebox.showerror("Error", "Password Harus 6 Karakter atau Lebih.")
        return
    if passwordpw != kon_passwordpw:
        messagebox.showerror("Error", "Password dan konfirmasi password harus sama.")
        return
    client = connect_to_mongodb()
    if client:
        db = client["finwiz"]
        users_collections = db["users"]

        # Cek apakah username sudah terdaftar di database
        if not users_collections.find({"Id": idpw, "username": usernamepw}):
            messagebox.showerror("Error", "Id atau Username Tidak Valid.")
            return

        criteria = {"Id": idpw, "username": usernamepw}
        new_data = {"$set": {"password": passwordpw}}
        users_collections.update_one(criteria, new_data)
        messagebox.showinfo("Sukses", "Ganti Password Berhasil!! Silakan Login.")
        clear_fields()
        show_login_page()

    



# Fungsi untuk menampilkan halaman login

def forget_pw():
    fr_login.pack_forget()
    signup_frame.pack_forget()
    fg_pw.pack(padx=10, pady=50)

def show_login_page():
    fg_pw.pack_forget()
    signup_frame.pack_forget()
    fr_login.pack(padx=10, pady=100)

# Fungsi untuk menampilkan halaman sign up
def show_signup_page():
    fg_pw.pack_forget()
    fr_login.pack_forget()
    signup_frame.pack(padx=10, pady=80)

# Fungsi untuk melakukan login
def login():
    global global_username
    global_username = username_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Mohon isi semua kolom.")
        return

    # Menghubungkan ke MongoDB
    client = connect_to_mongodb()
    if client:
        db = client["finwiz"]
        users_collection = db["users"]

        # Cek apakah username dan password sesuai dengan data di database
        user = users_collection.find_one({"username": username, "password": password})
        if user:
            clear_fields()
            navigate_to_items_page()
            # Di sini Anda bisa melakukan navigasi ke halaman utama aplikasi setelah login sukses
        else:
            messagebox.showerror("Error", "Username atau password salah.")

# Fungsi untuk melakukan sign up
def sign_up():
    id = id_entry.get()
    name = name_entry.get()
    username = signup_username_entry.get()
    password = signup_password_entry.get()
    confirm_password = confirm_password_entry.get()

    if not id or not name or not username or not password or not confirm_password:
        messagebox.showerror("Error", "Mohon isi semua kolom.")
        return
    
    if len(password) < 6:
        messagebox.showerror("Error", "Password Harus 6 Karakter atau Lebih.")
        return
    
    if password != confirm_password:
        messagebox.showerror("Error", "Password dan konfirmasi password harus sama.")
        return

    # Menghubungkan ke MongoDB
    client = connect_to_mongodb()
    if client:
        db = client["finwiz"]
        users_collection = db["users"]

        # Cek apakah username sudah terdaftar di database
        if users_collection.find_one({"username": username}) or users_collection.find_one({"Id": id}):
            messagebox.showerror("Error", "Id atau Username sudah terdaftar.")
            return

        tgl_hari_ini = datetime.date.today()
        tgl_format_tanggal = tgl_hari_ini.strftime("%d-%m-%Y")
        # Jika belum terdaftar, tambahkan ke database
        user_data = {
            "Id": id,
            "name": name,
            "username": username,
            "password": password,
            "join date": tgl_format_tanggal
        }
        users_collection.insert_one(user_data)
        messagebox.showinfo("Sukses", "Pendaftaran berhasil! Silakan login.")
        clear_fields()
        show_login_page()

#---------------------------------------------------------------------------------------------------------
global_username = tk.StringVar()
#Login
# frame login
fr_login = ttk.Frame(window)
fr_login.pack(padx=10, pady=100)

l1=ttk.Label(fr_login, text="FinWiz",font=('Century Gothic',30))
l1.pack(pady= 50)

# label username
login_username_label = ttk.Label(fr_login, text="USERNAME")
login_username_label.pack()

# entry username
username = tk.StringVar()
username_entry = ttk.Entry(fr_login, textvariable=username, background='white', justify='center', width=23)
username_entry.pack()

# label password
login_password_label = ttk.Label(fr_login, text="PASSWORD")
login_password_label.pack()

# entry password
password = tk.StringVar()
password_entry = ttk.Entry(fr_login, textvariable=password, show='●', justify='center', width=23)
password_entry.pack()

# login button
login_button = ttk.Button(fr_login, text="Login", command= login, width= 25,style='Outline.TButton',cursor='hand2' )
login_button.pack(pady=10)

# link Sign Up
signup_link = tk.Label(fr_login, text="Belum punya akun? Sign Up",
                       fg="green", cursor="hand2")
signup_link.pack()
signup_link.bind("<Button-1>", lambda event: show_signup_page())

# link lupa password
forget_pass_link = tk.Label(fr_login, text="Forget Password?",
                       fg="green", cursor="hand2")
forget_pass_link.pack(pady=10)
forget_pass_link.bind("<Button-1>", lambda event: forget_pw())



#------------------------------------------------------------------------------
fg_pw =ttk.Frame(window)
fg_pw.pack(padx=10, pady=50)
judul = ttk.Label(fg_pw, text='Forget Password',font=('aileron', 20, 'bold'))
judul.pack(pady= 10)
    # label id
id_label_pw = ttk.Label(fg_pw, text='ID')
id_label_pw.pack()
    # entry id
id_entry_pw = tk.StringVar()
pw_id_entry = ttk.Entry(fg_pw, textvariable= id_entry_pw, background='white', justify='center',width=23)
pw_id_entry.pack()

    # label username
username_label_pw = ttk.Label(fg_pw, text="USERNAME")
username_label_pw.pack()
    # entry username
username_pw = tk.StringVar()
pw_username_entry = ttk.Entry(fg_pw, textvariable=username_pw, background='white', justify='center',width=23)
pw_username_entry.pack()

    # label password
pw_password_label = ttk.Label(fg_pw, text="NEW PASSWORD")
pw_password_label.pack()
    # entry password
password_pw = tk.StringVar()
pw_password_entry = ttk.Entry(fg_pw, textvariable=password_pw, show='●',justify='center',width=23)
pw_password_entry.pack()

    # Confirm password label
confirm_password_label_pw = ttk.Label(fg_pw, text="KONFIRMASI PASSWORD")
confirm_password_label_pw.pack()
    # entry confirm password
pw_con = tk.StringVar()
confirm_password_entry_pw = ttk.Entry(fg_pw, textvariable=pw_con,show="●", justify='center',width=23)
confirm_password_entry_pw.pack()

sub_button_pw = ttk.Button(fg_pw, text="Submit", command=update_pw, width=25,style='Outline.TButton',cursor='hand2')
sub_button_pw.pack(pady=10)

bk_button_pw = ttk.Button(fg_pw, text="Back", command=show_login_page, width=25,style='Outline.TButton',cursor='hand2')
bk_button_pw.pack()


# Sign Up

# Frame
signup_frame = ttk.Frame(window)
signup_frame.pack(padx=10, pady=80)
l2=ttk.Label(signup_frame, text="Sign Up",font=('Century Gothic',30))
# l1.place(relx=0.5, rely=0.01,  anchor=tk.CENTER)
l2.pack(pady= 50)
# label id
id_label = ttk.Label(signup_frame, text='ID')
id_label.pack()
# entry id
id_entry = tk.StringVar()
signup_id_entry = ttk.Entry(signup_frame, textvariable= id_entry, background='white', justify='center',width=23)
signup_id_entry.pack()

# label name
name_label = ttk.Label(signup_frame, text='NAME')
name_label.pack()
# entry name
name_entry = tk.StringVar()
signup_name_entry = ttk.Entry(signup_frame, textvariable= name_entry, background='white', justify='center',width=23)
signup_name_entry.pack()

# label username
signup_username_label = ttk.Label(signup_frame, text="USERNAME")
signup_username_label.pack()
# entry username
username = tk.StringVar()
signup_username_entry = ttk.Entry(signup_frame, textvariable=username, background='white', justify='center',width=23)
signup_username_entry.pack()

# label password
signup_password_label = ttk.Label(signup_frame, text="PASSWORD")
signup_password_label.pack()
# entry password
password = tk.StringVar()
signup_password_entry = ttk.Entry(signup_frame, textvariable=password, show='●',justify='center',width=23)
signup_password_entry.pack()

# Confirm password label
confirm_password_label = ttk.Label(signup_frame, text="KONFIRMASI PASSWORD")
confirm_password_label.pack()
# entry confirm password
confirm_password_entry = ttk.Entry(signup_frame, show="●", justify='center',width=23)
confirm_password_entry.pack()

# login button
signup_button = ttk.Button(signup_frame, text="Sign Up", command=sign_up, width=25,style='Outline.TButton',cursor='hand2')
signup_button.pack(pady=10)


# link login
login_link = tk.Label(signup_frame, text="Sudah punya akun? Login",
                      fg="blue", cursor="hand2")
login_link.pack()
login_link.bind("<Button-1>", lambda event: show_login_page())

show_login_page()

#-------------------------------------------------------------------------------------------------------------------------------------------
# Main Page

window.mainloop()