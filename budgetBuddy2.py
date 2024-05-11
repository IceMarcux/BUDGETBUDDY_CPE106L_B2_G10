# import modules 
from tkinter import *
from PIL import Image
import sqlite3
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox

# object for database
data = Database(db='test.db')

# global variables
count = 0
selected_rowid = 0

# functions
def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get())
       
def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

def fetch_records():
    f = data.fetchRecord('select rowid, * from expense_record')
    global count
    for rec in f:
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1
    tv.after(400, refreshData)

def select_record(event):
    global selected_rowid
    selected = tv.focus()    
    val = tv.item(selected, 'values')
  
    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass


def update_record():
    global selected_rowid

    selected = tv.focus()
	# Update record
    try:
        data.updateRecord(namevar.get(), amtvar.get(), dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as ep:
        messagebox.showerror('Error',  ep)

	# Clear entry boxes
    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    tv.after(400, refreshData)
    

def totalBalance():
    f = data.fetchRecord(query="Select sum(item_price) from expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo('Current Balance: ', f"Total Expense: ' {j} \nBalance Remaining: {5000 - j}")

def refreshData():
    for item in tv.get_children():
      tv.delete(item)
    fetch_records()
    
def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()

window = Tk()
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.state('zoomed')
window.resizable(0, 0)
window.title('Login and Registration Page')

# Window Icon Photo
icon = PhotoImage(file='images\\pic-icon.png')
window.iconphoto(True, icon)

LoginPage = Frame(window)
RegistrationPage = Frame(window)

for frame in (LoginPage, RegistrationPage):
    frame.grid(row=0, column=0, sticky='nsew')


def show_frame(frame):
    frame.tkraise()


show_frame(LoginPage)


# ========== DATABASE VARIABLES ============
Email = StringVar()
FullName = StringVar()
Password = StringVar()
ConfirmPassword = StringVar()

# =====================================================================================================================
# =====================================================================================================================
# ==================== LOGIN PAGE =====================================================================================
# =====================================================================================================================
# =====================================================================================================================

design_frame1 = Listbox(LoginPage, bg='#0c71b9', width=115, height=50, highlightthickness=0, borderwidth=0)
design_frame1.place(x=0, y=0)

design_frame2 = Listbox(LoginPage, bg='#1e85d0', width=115, height=50, highlightthickness=0, borderwidth=0)
design_frame2.place(x=676, y=0)

design_frame3 = Listbox(LoginPage, bg='#1e85d0', width=100, height=33, highlightthickness=0, borderwidth=0)
design_frame3.place(x=75, y=106)

design_frame4 = Listbox(LoginPage, bg='#f8f8f8', width=100, height=33, highlightthickness=0, borderwidth=0)
design_frame4.place(x=676, y=106)

# ====== Email ====================
email_entry = Entry(design_frame4, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                    textvariable=Email)
email_entry.place(x=134, y=170, width=256, height=34)
email_entry.config(highlightbackground="black", highlightcolor="black")
email_label = Label(design_frame4, text='• Email account', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
email_label.place(x=130, y=140)

# ==== Password ==================
password_entry1 = Entry(design_frame4, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2,
                        textvariable=Password)
password_entry1.place(x=134, y=250, width=256, height=34)
password_entry1.config(highlightbackground="black", highlightcolor="black")
password_label = Label(design_frame4, text='• Password', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
password_label.place(x=130, y=220)


# function for show and hide password
def password_command():
    if password_entry1.cget('show') == '•':
        password_entry1.config(show='')
    else:
        password_entry1.config(show='•')


# ====== checkbutton ==============
checkButton = Checkbutton(design_frame4, bg='#f8f8f8', command=password_command, text='show password')
checkButton.place(x=140, y=288)

# ========= Buttons ===============
SignUp_button = Button(LoginPage, text='Sign up', font=("yu gothic ui bold", 12), bg='#f8f8f8', fg="#89898b",
                       command=lambda: show_frame(RegistrationPage), borderwidth=0, activebackground='#1b87d2', cursor='hand2')
SignUp_button.place(x=1100, y=175)

# ===== Welcome Label ==============
welcome_label = Label(design_frame4, text='Welcome', font=('Arial', 20, 'bold'), bg='#f8f8f8')
welcome_label.place(x=130, y=15)

# ======= top Login Button =========
login_button = Button(LoginPage, text='Login', font=("yu gothic ui bold", 12), bg='#f8f8f8', fg="#89898b",
                      borderwidth=0, activebackground='#1b87d2', cursor='hand2')
login_button.place(x=845, y=175)

login_line = Canvas(LoginPage, width=60, height=5, bg='#1b87d2')
login_line.place(x=840, y=203)

# ==== LOGIN  down button ============
loginBtn1 = Button(design_frame4, fg='#f8f8f8', text='Login', bg='#1b87d2', font=("yu gothic ui bold", 15),
                   cursor='hand2', activebackground='#1b87d2', command=lambda: login())
loginBtn1.place(x=133, y=340, width=256, height=50)


# ======= ICONS =================

# ===== Email icon =========
email_icon = Image.open('images\\email-icon.png')
photo = ImageTk.PhotoImage(email_icon)
emailIcon_label = Label(design_frame4, image=photo, bg='#f8f8f8')
emailIcon_label.image = photo
emailIcon_label.place(x=105, y=174)

# ===== password icon =========
password_icon = Image.open('images\\pass-icon.png')
photo = ImageTk.PhotoImage(password_icon)
password_icon_label = Label(design_frame4, image=photo, bg='#f8f8f8')
password_icon_label.image = photo
password_icon_label.place(x=105, y=254)

# ===== picture icon =========
picture_icon = Image.open('images\\pic-icon.png')
photo = ImageTk.PhotoImage(picture_icon)
picture_icon_label = Label(design_frame4, image=photo, bg='#f8f8f8')
picture_icon_label.image = photo
picture_icon_label.place(x=280, y=5)

# ===== Left Side Picture ============
side_image = Image.open('images\\vector.png')
photo = ImageTk.PhotoImage(side_image)
side_image_label = Label(design_frame3, image=photo, bg='#1e85d0')
side_image_label.image = photo
side_image_label.place(x=50, y=10)


# ============ LOGIN DATABASE CONNECTION =========
connection = sqlite3.connect('RegLog.db')
cur = connection.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS RegLog(Email TEXT PRIMARY KEY, FullName TEXT, Password TEXT, "
            "ConfirmPassword TEXT)")
connection.commit()
connection.close()


def login():
    conn = sqlite3.connect("RegLog.db")
    cursor = conn.cursor()

    find_user = 'SELECT * FROM RegLog WHERE Email = ? and Password = ?'
    cursor.execute(find_user, [(email_entry.get()), (password_entry1.get())])

    result = cursor.fetchall()
    if result:
        messagebox.showinfo("Success", 'Logged in Successfully.')
    else:
        messagebox.showerror("Failed", "Wrong Login details, please try again.")


# ===================================================================================================================
# ===================================================================================================================
# === FORGOT PASSWORD  PAGE =========================================================================================
# ===================================================================================================================
# ===================================================================================================================


def forgot_password():
    win = Toplevel()
    window_width = 350
    window_height = 350
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    position_top = int(screen_height / 4 - window_height / 4)
    position_right = int(screen_width / 2 - window_width / 2)
    win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    win.title('Forgot Password')
    win.iconbitmap('images\\aa.ico')
    win.configure(background='#f8f8f8')
    win.resizable(0, 0)

    # Variables
    email = StringVar()
    password = StringVar()
    confirmPassword = StringVar()

    # ====== Email ====================
    email_entry2 = Entry(win, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                         textvariable=email)
    email_entry2.place(x=40, y=30, width=256, height=34)
    email_entry2.config(highlightbackground="black", highlightcolor="black")
    email_label2 = Label(win, text='• Email account', fg="#89898b", bg='#f8f8f8',
                         font=("yu gothic ui", 11, 'bold'))
    email_label2.place(x=40, y=0)

    # ====  New Password ==================
    new_password_entry = Entry(win, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2,
                               textvariable=password)
    new_password_entry.place(x=40, y=110, width=256, height=34)
    new_password_entry.config(highlightbackground="black", highlightcolor="black")
    new_password_label = Label(win, text='• New Password', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
    new_password_label.place(x=40, y=80)

    # ====  Confirm Password ==================
    confirm_password_entry = Entry(win, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2
                                   , textvariable=confirmPassword)
    confirm_password_entry.place(x=40, y=190, width=256, height=34)
    confirm_password_entry.config(highlightbackground="black", highlightcolor="black")
    confirm_password_label = Label(win, text='• Confirm Password', fg="#89898b", bg='#f8f8f8',
                                   font=("yu gothic ui", 11, 'bold'))
    confirm_password_label.place(x=40, y=160)

    # ======= Update password Button ============
    update_pass = Button(win, fg='#f8f8f8', text='Update Password', bg='#1b87d2', font=("yu gothic ui bold", 14),
                         cursor='hand2', activebackground='#1b87d2', command=lambda: change_password())
    update_pass.place(x=40, y=240, width=256, height=50)

    # ========= DATABASE CONNECTION FOR FORGOT PASSWORD=====================
    def change_password():
        if new_password_entry.get() == confirm_password_entry.get():
            db = sqlite3.connect("RegLog.db")
            curs = db.cursor()

            insert = '''update RegLog set Password=?, ConfirmPassword=? where Email=? '''
            curs.execute(insert, [new_password_entry.get(), confirm_password_entry.get(), email_entry2.get(), ])
            db.commit()
            db.close()
            messagebox.showinfo('Congrats', 'Password changed successfully')

        else:
            messagebox.showerror('Error!', "Passwords didn't match")


forgotPassword = Button(design_frame4, text='Forgot password', font=("yu gothic ui", 8, "bold underline"), bg='#f8f8f8',
                        borderwidth=0, activebackground='#f8f8f8', command=lambda: forgot_password(), cursor="hand2")
forgotPassword.place(x=290, y=290)


# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================


# =====================================================================================================================
# =====================================================================================================================
# ==================== REGISTRATION PAGE ==============================================================================
# =====================================================================================================================
# =====================================================================================================================

design_frame5 = Listbox(RegistrationPage, bg='#0c71b9', width=115, height=50, highlightthickness=0, borderwidth=0)
design_frame5.place(x=0, y=0)

design_frame6 = Listbox(RegistrationPage, bg='#1e85d0', width=115, height=50, highlightthickness=0, borderwidth=0)
design_frame6.place(x=676, y=0)

design_frame7 = Listbox(RegistrationPage, bg='#1e85d0', width=100, height=33, highlightthickness=0, borderwidth=0)
design_frame7.place(x=75, y=106)

design_frame8 = Listbox(RegistrationPage, bg='#f8f8f8', width=100, height=33, highlightthickness=0, borderwidth=0)
design_frame8.place(x=676, y=106)

# ==== Full Name =======
name_entry = Entry(design_frame8, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                   textvariable=FullName)
name_entry.place(x=284, y=150, width=286, height=34)
name_entry.config(highlightbackground="black", highlightcolor="black")
name_label = Label(design_frame8, text='•Full Name', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
name_label.place(x=280, y=120)

# ======= Email ===========
email_entry = Entry(design_frame8, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                    textvariable=Email)
email_entry.place(x=284, y=220, width=286, height=34)
email_entry.config(highlightbackground="black", highlightcolor="black")
email_label = Label(design_frame8, text='•Email', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
email_label.place(x=280, y=190)

# ====== Password =========
password_entry = Entry(design_frame8, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2,
                       textvariable=Password)
password_entry.place(x=284, y=295, width=286, height=34)
password_entry.config(highlightbackground="black", highlightcolor="black")
password_label = Label(design_frame8, text='• Password', fg="#89898b", bg='#f8f8f8',
                       font=("yu gothic ui", 11, 'bold'))
password_label.place(x=280, y=265)


def password_command2():
    if password_entry.cget('show') == '•':
        password_entry.config(show='')
    else:
        password_entry.config(show='•')


checkButton = Checkbutton(design_frame8, bg='#f8f8f8', command=password_command2, text='show password')
checkButton.place(x=290, y=330)


# ====== Confirm Password =============
confirmPassword_entry = Entry(design_frame8, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                              textvariable=ConfirmPassword)
confirmPassword_entry.place(x=284, y=385, width=286, height=34)
confirmPassword_entry.config(highlightbackground="black", highlightcolor="black")
confirmPassword_label = Label(design_frame8, text='• Confirm Password', fg="#89898b", bg='#f8f8f8',
                              font=("yu gothic ui", 11, 'bold'))
confirmPassword_label.place(x=280, y=355)

# ========= Buttons ====================
SignUp_button = Button(RegistrationPage, text='Sign up', font=("yu gothic ui bold", 12), bg='#f8f8f8', fg="#89898b",
                       command=lambda: show_frame(LoginPage), borderwidth=0, activebackground='#1b87d2', cursor='hand2')
SignUp_button.place(x=1100, y=175)

SignUp_line = Canvas(RegistrationPage, width=60, height=5, bg='#1b87d2')
SignUp_line.place(x=1100, y=203)

# ===== Welcome Label ==================
welcome_label = Label(design_frame8, text='Welcome', font=('Arial', 20, 'bold'), bg='#f8f8f8')
welcome_label.place(x=130, y=15)

# ========= Login Button =========
login_button = Button(RegistrationPage, text='Login', font=("yu gothic ui bold", 12), bg='#f8f8f8', fg="#89898b",
                      borderwidth=0, activebackground='#1b87d2', command=lambda: show_frame(LoginPage), cursor='hand2')
login_button.place(x=845, y=175)

# ==== SIGN UP down button ============
signUp2 = Button(design_frame8, fg='#f8f8f8', text='Sign Up', bg='#1b87d2', font=("yu gothic ui bold", 15),
                 cursor='hand2', activebackground='#1b87d2', command=lambda: submit())
signUp2.place(x=285, y=435, width=286, height=50)

# ===== password icon =========
password_icon = Image.open('images\\pass-icon.png')
photo = ImageTk.PhotoImage(password_icon)
password_icon_label = Label(design_frame8, image=photo, bg='#f8f8f8')
password_icon_label.image = photo
password_icon_label.place(x=255, y=300)

# ===== confirm password icon =========
confirmPassword_icon = Image.open('images\\pass-icon.png')
photo = ImageTk.PhotoImage(confirmPassword_icon)
confirmPassword_icon_label = Label(design_frame8, image=photo, bg='#f8f8f8')
confirmPassword_icon_label.image = photo
confirmPassword_icon_label.place(x=255, y=390)

# ===== Email icon =========
email_icon = Image.open('images\\email-icon.png')
photo = ImageTk.PhotoImage(email_icon)
emailIcon_label = Label(design_frame8, image=photo, bg='#f8f8f8')
emailIcon_label.image = photo
emailIcon_label.place(x=255, y=225)

# ===== Full Name icon =========
name_icon = Image.open('images\\name-icon.png')
photo = ImageTk.PhotoImage(name_icon)
nameIcon_label = Label(design_frame8, image=photo, bg='#f8f8f8')
nameIcon_label.image = photo
nameIcon_label.place(x=252, y=153)

# ===== picture icon =========
picture_icon = Image.open('images\\pic-icon.png')
photo = ImageTk.PhotoImage(picture_icon)
picture_icon_label = Label(design_frame8, image=photo, bg='#f8f8f8')
picture_icon_label.image = photo
picture_icon_label.place(x=280, y=5)

# ===== Left Side Picture ============
side_image = Image.open('images\\vector.png')
photo = ImageTk.PhotoImage(side_image)
side_image_label = Label(design_frame7, image=photo, bg='#1e85d0')
side_image_label.image = photo
side_image_label.place(x=50, y=10)


# =====================================================================================================================
# =====================================================================================================================
# ==================== DATABASE CONNECTION ============================================================================
# =====================================================================================================================
# =====================================================================================================================

connection = sqlite3.connect('RegLog.db')
cur = connection.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS RegLog(Email TEXT PRIMARY KEY, FullName TEXT, Password TEXT, "
            "ConfirmPassword TEXT)")
connection.commit()
connection.close()


def submit():
    check_counter = 0
    warn = ""
    if name_entry.get() == "":
        warn = "Full Name can't be empty"
    else:
        check_counter += 1

    if email_entry.get() == "":
        warn = "Email Field can't be empty"
    else:
        check_counter += 1

    if password_entry.get() == "":
        warn = "Password can't be empty"
    else:
        check_counter += 1

    if confirmPassword_entry.get() == "":
        warn = "Sorry, can't sign up make sure all fields are complete"
    else:
        check_counter += 1

    if password_entry.get() != confirmPassword_entry.get():
        warn = "Passwords didn't match!"
    else:
        check_counter += 1

    if check_counter == 5:
        try:
            connection = sqlite3.connect("RegLog.db")
            cur = connection.cursor()
            cur.execute("INSERT INTO RegLog values(?,?,?,?)",
                        (Email.get(), FullName.get(), Password.get(), ConfirmPassword.get()))

            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "New account created successfully")

        except Exception as ep:
            messagebox.showerror('', ep)
    else:
        messagebox.showerror('Error', warn)

# create tkinter object
ws = Tk()
ws.title('Daily Expenses')

# variables
f = ('Times new roman', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

# Frame widget
f2 = Frame(ws)
f2.pack() 

f1 = Frame(
    ws,
    padx=10,
    pady=10,
)
f1.pack(expand=True, fill=BOTH)


# Label widget
Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)

# Entry widgets 
item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

# Entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))


# Action buttons
cur_date = Button(
    f1, 
    text='Current Date', 
    font=f, 
    bg='#04C4D9', 
    command=setDate,
    width=15
    )

submit_btn = Button(
    f1, 
    text='Save Record', 
    font=f, 
    command=saveRecord, 
    bg='#42602D', 
    fg='white'
    )

clr_btn = Button(
    f1, 
    text='Clear Entry', 
    font=f, 
    command=clearEntries, 
    bg='#D9B036', 
    fg='white'
    )

quit_btn = Button(
    f1, 
    text='Exit', 
    font=f, 
    command=lambda:ws.destroy(), 
    bg='#D33532', 
    fg='white'
    )

total_bal = Button(
    f1,
    text='Total Balance',
    font=f,
    bg='#486966',
    command=totalBalance
)

total_spent = Button(
    f1,
    text='Total Spent',
    font=f,
    command=lambda:data.fetchRecord('select sum(ite)')
)

update_btn = Button(
    f1, 
    text='Update',
    bg='#C2BB00',
    command=update_record,
    font=f
)

del_btn = Button(
    f1, 
    text='Delete',
    bg='#BD2A2E',
    command=deleteRow,
    font=f
)

# grid placement
cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))

# Treeview widget
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side="left")

# add heading to treeview
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name", )
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

# binding treeview
tv.bind("<ButtonRelease-1>", select_record)

# style for treeview
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

# Vertical scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

# calling function 
fetch_records()

# infinite loop
ws.mainloop()