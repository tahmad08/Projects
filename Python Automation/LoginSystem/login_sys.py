# Basic login system for python practice

""" Goal - create a basic login system (from a reddit comment):
"Just print everything out in the console and work your way with input. 
Make a password system which is basic, then add multiple users, the ability to add new accounts, 
to change passwords, to then make sure there are 3 attempts max 
or the account gets locked for 10 seconds, etc etc."

Plan: 
1. create user class with username, pw, etc
2. basic methods for creating account, changing pw, deleting account
3. add stuff with hashes and salts
4. maybe try shifting to database at end? SQLite

Use these crypto challenges too: https://cryptopals.com/sets/1

Use Tkinter python interface?
SQLite?
Book recs? Goodreads API?
Refs: https://www.sourcecodester.com/tutorials/python/11351/python-simple-login-application.html
"""

import sqlite3
#bad practice??? --> from tkinter import *
import tkinter as tk


# tkinter setup
def setup_window(root):
    #initialize window
    root.title("A Login Application")
    width = 400
    height = 280
    # w/h for computer screen so we can specify where the window will open
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # calculate x and y coordinates for the Tk root window
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    #root.geometry is where the window opens up
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    #passing 0,0 into the resizable fxn makes the window NON-RESIZABLE
    root.resizable(0, 0)

def design_layout(root):
    #==============================VARIABLES======================================
    global USERNAME
    global PASSWORD
    USERNAME = tk.StringVar()
    PASSWORD = tk.StringVar()
    #==============================FRAMES=========================================
    #frames are containers in the widget. we have 2 frames here, Top and Form
    #bd is border width, defaults to 0. relief-the border type (shadow, groove, ridge, sunken)
    #TOP is the title container
    Top = tk.Frame(root, bd=4, relief=tk.RIDGE)
    """ https://www.python-course.eu/tkinter_layout_management.php
        pack is one of the geometry managers. There is pack, grid, and place
        pack places widgets relative to each other. limited possibilities.
    expand − When set to true, widget expands to fill any space not otherwise used in widget's parent.
    fill − Determines whether widget fills any extra space allocated to it by the packer, or keeps
        its own minimal dimensions: NONE (default), X (fill only horizontally), Y (fill only vertically),
        or BOTH (fill both horizontally and vertically).
    side − Determines which side of the parent widget packs against: TOP (default), BOTTOM, LEFT, or RIGHT.
    """
    Top.pack(side=tk.TOP, fill=tk.X)
    Form = tk.Frame(root, height=200)
    Form.pack(side=tk.TOP, pady=20)
    #==============================LABELS=========================================
    lbl_title = tk.Label(Top, text = "Simple Login Application", font=('arial', 15))
    lbl_title.pack(fill=tk.X)
    lbl_username = tk.Label(Form, text = "User:", font=('times', 14), bd=15)
    lbl_username.grid(row=0, sticky="e")
    lbl_password = tk.Label(Form, text = "Password:", font=('times', 14), bd=15)
    lbl_password.grid(row=1, sticky="e")
    global lbl_text
    lbl_text = tk.Label(Form)
    lbl_text.grid(row=2, columnspan=2)
    #==============================ENTRY WIDGETS==================================
    username = tk.Entry(Form, textvariable=USERNAME, font=(14))
    username.grid(row=0, column=1)
    password = tk.Entry(Form, textvariable=PASSWORD, show="*", font=(14))
    password.grid(row=1, column=1)
    #==============================BUTTON WIDGETS=================================
    btn_login = tk.Button(Form, text="Login", width=45, command=Login)
    btn_login.grid(pady=25, row=3, columnspan=2)
    btn_login.bind('<Return>', Login)

    
    #==============================METHODS========================================
""" creates a database connection using SQLite
https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor
conn: the connection
cursor: an object that executes SQL statements with cursor.execute("statement"),
fetches query result tuples (as a list), number of rows, description - column names
"""
def Database():
    global conn, cursor
    
    #create db called pythontut, conn and cursor
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()

    #create a table called member w mem_id, username and password columns/keys
    #mem_id is the primary key, not null with autoincrement
    #these are the constraints/integrity protections
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")

    #fetch admin entry, or create admin if none exists
    cursor.execute("SELECT * FROM `member` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `member` (username, password) VALUES('admin', 'admin')")
        conn.commit()

def Login(event=None):
    #calls database()fxn to create db/connection
    Database()
    #USERNAME and PASSWORD are the entry field entries, error if nothing entered
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        #find the user's login in the db, if it exists reset the entry fields and label
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            HomeWindow()
            USERNAME.set("")
            PASSWORD.set("")
            lbl_text.config(text="")
        else:
            #error, user/pw invalid
            lbl_text.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")   
    cursor.close()
    conn.close()

#Home window if the login is successful
def HomeWindow():
    global Home
    root.withdraw()
    Home = Toplevel()
    Home.title("Python: Simple Login Application")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.resizable(0, 0)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    lbl_home = Label(Home, text="Successfully Login!", font=('times new roman', 20)).pack()
    btn_back = Button(Home, text='Back', command=Back).pack(pady=20, fill=X)
 
def Back():
    Home.destroy()
    root.deiconify()

def main():
    global root
    root = tk.Tk()
    setup_window(root)
    design_layout(root)
    Login()
    
if __name__ == '__main__':
    main()


    
