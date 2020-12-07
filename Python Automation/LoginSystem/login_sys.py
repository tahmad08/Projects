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
"""

import sqlite3
import tkinter as tk

# tkinter setup
def setup_window():
    #initialize window
    root = tk.Tk()
    root.title("Simple Login Application")
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
    root.resizable(0, 0)
            
def main():
    setup_window()
    
if __name__ == '__main__':
    main()


    
