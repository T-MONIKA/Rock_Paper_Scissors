import sqlite3
from tkinter import *
from tkinter import messagebox

# Function to create the USERS table if it doesn't exist
def create_users_table():
    conn = sqlite3.connect('users.db')  # Using 'users.db' as the database name
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            fname TEXT,
            lname TEXT,
            username TEXT PRIMARY KEY,
            password TEXT,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert a new user
def insert_user(fname, lname, username, password, gender):
    create_users_table()  # Ensure the table is created before insertion
    
    conn = sqlite3.connect('users.db')  # Using 'users.db' as the database name
    c = conn.cursor()
    c.execute("INSERT INTO USERS (fname, lname, username, password, gender) VALUES (?, ?, ?, ?, ?)",
              (fname, lname, username, password, gender))
    conn.commit()
    conn.close()

# Function to check if a user exists (for login)
def check_user(username, password):
    conn = sqlite3.connect('users.db')  # Using 'users.db' as the database name
    c = conn.cursor()
    c.execute("SELECT * FROM USERS WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Login Function
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        user = check_user(username, password)
        if user:
            messagebox.showinfo("Login Success", f"Welcome back, {user[0]}!")
            # Here you can call your game window or main menu function
            main_menu()  # Assuming main_menu is the function to show the game
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")
    else:
        messagebox.showerror("Input Error", "Please enter both username and password.")

# Sign Up Function
def sign_up():
    fname = fname_entry.get()
    lname = lname_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    gender = gender_var.get()

    if fname and lname and username and password and gender:
        try:
            insert_user(fname, lname, username, password, gender)
            messagebox.showinfo("Sign Up Success", "Account created successfully!")
            # Switch to the login window after successful sign-up
            login_window()
        except sqlite3.IntegrityError:
            messagebox.showerror("Sign Up Error", "Username already exists.")
    else:
        messagebox.showerror("Input Error", "Please fill in all fields.")

# Function to create and display the login window
def login_window():
    global username_entry, password_entry
    login_win = Toplevel(root)
    login_win.title("Login")
    login_win.geometry("300x250")
    
    Label(login_win, text="Username:").pack(pady=5)
    username_entry = Entry(login_win)
    username_entry.pack(pady=5)

    Label(login_win, text="Password:").pack(pady=5)
    password_entry = Entry(login_win, show="*")
    password_entry.pack(pady=5)

    Button(login_win, text="Login", command=login).pack(pady=10)
    Button(login_win, text="Sign Up", command=sign_up_window).pack(pady=5)

# Function to create and display the sign-up window
def sign_up_window():
    global fname_entry, lname_entry, username_entry, password_entry, gender_var
    sign_up_win = Toplevel(root)
    sign_up_win.title("Sign Up")
    sign_up_win.geometry("300x350")

    Label(sign_up_win, text="First Name:").pack(pady=5)
    fname_entry = Entry(sign_up_win)
    fname_entry.pack(pady=5)

    Label(sign_up_win, text="Last Name:").pack(pady=5)
    lname_entry = Entry(sign_up_win)
    lname_entry.pack(pady=5)

    Label(sign_up_win, text="Username:").pack(pady=5)
    username_entry = Entry(sign_up_win)
    username_entry.pack(pady=5)

    Label(sign_up_win, text="Password:").pack(pady=5)
    password_entry = Entry(sign_up_win, show="*")
    password_entry.pack(pady=5)

    Label(sign_up_win, text="Gender:").pack(pady=5)
    gender_var = StringVar()
    gender_var.set("Male")  # Default gender
    gender_menu = OptionMenu(sign_up_win, gender_var, "Male", "Female", "Other")
    gender_menu.pack(pady=5)

    Button(sign_up_win, text="Sign Up", command=sign_up).pack(pady=10)

# Function to create and show the main menu (game page)
def main_menu():
    # Hide the login/signup window
    for widget in root.winfo_children():
        widget.destroy()

    # Game logic goes here
    Label(root, text="Rock Paper Scissors Game", font=("Arial", 20)).pack(pady=20)

    Button(root, text="Start Game", command=start_game).pack(pady=20)
    Button(root, text="Exit", command=root.quit).pack()

# Function to start the game
def start_game():
    pass  # Replace with your game start logic

# Main window (root) setup
root = Tk()
root.title("Login and Sign Up")
root.geometry("300x250")

# Show login window first
login_window()

root.mainloop()
