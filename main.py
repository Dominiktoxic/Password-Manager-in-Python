from cryptography.fernet import Fernet
import os
from tkinter import *
from tkinter import messagebox
import random
import string

class PasswordManager():

    # Initialize the Password Manager

    def __init__(self):
        self.passwords = {}
        self.keyfile = "key.key"
        self.passfile = "passes.pass"
        self.masterpwdfile = "mstrpwd.pass"
        self.masterpwd = None

        # Checking for "key.key"
        if self.keyfile in os.listdir():
            with open(self.keyfile, "rb") as f:
                self.key = f.read()
        else:
            self.create_keyfile()
        
        # Checking for "passes.pass"
        if self.passfile in os.listdir():
            with open("passes.pass", "r") as f:
                for line in f:
                    site, encrypted = line.split("|")
                    self.passwords[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
        else:
            self.create_passfile()
        
        # Checking for "mstrpwd.pass"
        if self.masterpwdfile in os.listdir():
            with open(self.masterpwdfile, "rb") as f:
                self.masterpwd = f.read()
        else:
            with open(self.masterpwdfile, "wb") as f:
                self.masterpwd = "main123"
                f.write(Fernet(self.key).encrypt(self.masterpwd.encode()))
    
    # Create Keyfile
    def create_keyfile(self):
        with open(self.keyfile, "wb") as f:
            self.key = Fernet.generate_key()
            f.write(self.key)
    
    # Create Passwords File
    def create_passfile(self):
        with open(self.passfile, "x") as f:
            pass
    
    # Add Passwords
    def add_password(self, site, password):
        self.passwords[site] = password
        with open(self.passfile, "+a") as f:
            line = site + "|" + Fernet(self.key).encrypt(password.encode()).decode() + "\n"
            f.write(line)
    
    # View Passwords
    def view_password(self, site):
        return self.passwords[site]
    
    # Check Master Password
    def master_password(self):
        with open(self.masterpwdfile, "rb") as f:
            return Fernet(self.key).decrypt(f.read()).decode()
    
    # Change Master Password
    def change_mstr_password(self, password):
        with open(self.masterpwdfile, "wb") as f:
            self.masterpwd = Fernet(self.key).encrypt(password.encode())
            f.write(self.masterpwd)

pm = PasswordManager()

# Functions
def generate_password():
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    passwordEntry.delete(0, "end")
    passwordEntry.insert(0, password)

def add_password(site, password):
    if site == "" or password == "":
        pass
    else:
        pm.add_password(site, password)

def retrieve_password(site):
    if site == "":
        pass
    else:
        try:
            password = pm.view_password(site)
            messagebox.showinfo("Email and Password",f"Username/Email: {site} \n Password: {password}")
        except KeyError:
            print(f"{site} cannot be found.")

def input_mstr_pwd():
    mstrPwd = input("What would you like to change the Master Password to: ")
    change_master_password(mstrPwd)

def change_master_password(password):
    pm.change_mstr_password(password)
    print(f"The Master Password was changed to {password}")

# Variables
masterPwd = pm.master_password()
pwd = ""

# Master Password Check
while pwd != masterPwd:
    pwd = input("What is the Master Password (Starter is main123): ")

# Constants
MAX_WIDTH = 500
MAX_HEIGHT = 500

# Initializing Window
app = Tk()
app.maxsize(MAX_WIDTH, MAX_HEIGHT)
app.minsize(MAX_WIDTH, MAX_HEIGHT)
app.title("Password Manager")

logo = PhotoImage(file="logo.png")

label = Label(app, image=logo)
label.place(x=35, y=0)

username = Label(app, text="Username/Email", font=("Arial", 15))
username.place(x=180, y=150)

usernameEntry = Entry(app, font=("Arial", 15))
usernameEntry.place(x=140, y=190)

password = Label(app, text="Password", font=("Arial", 15))
password.place(x=205, y=230)

passwordEntry = Entry(app, font=("Arial", 15))
passwordEntry.place(x=140, y=270)

generatePassword = Button(app, text="Generate Password", font=("Arial", 9), command=generate_password)
generatePassword.place(x=370, y=270)

submit = Button(app, text="Submit", font=("Arial", 12), command=lambda: add_password(usernameEntry.get(), passwordEntry.get()))
submit.place(x=150, y=320)

retrievePass = Button(app, text="Retrieve Password", font=("Arial", 12), command=lambda: retrieve_password(usernameEntry.get()))
retrievePass.place(x=250, y=320)

changeMasterPassword = Button(app, text="Change Master Password", font=("Arial", 12), command=input_mstr_pwd)
changeMasterPassword.place(x=160, y=385)

app.mainloop()