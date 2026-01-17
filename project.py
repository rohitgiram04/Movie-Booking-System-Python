import tkinter as tk
from tkinter import messagebox
import csv
import random
import hashlib
from tkinter import ttk

# File to store movie and booking data
MOVIES_FILE = "movies_data.csv"
BOOKINGS_FILE = "bookings_data.csv"

# Admin credentials storage
stored_username = None
stored_password = None
unique_key = None

# Encryption functions
def encrypt_data(data, key):
    return ''.join(chr(ord(char) + key) for char in data)

def decrypt_data(data, key):
    return ''.join(chr(ord(char) - key) for char in data)

# File to store admin credentials
ADMIN_FILE = "cinema_admin_credentials.txt"

# Function to write to CSV files
def write_movie_data(movie_data):
    with open(MOVIES_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(movie_data)

def write_booking_data(booking_data):
    with open(BOOKINGS_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(booking_data)

# Generate unique key during sign-up
def generate_unique_key():
    return random.randint(1000, 9999)

# Admin sign-up
def admin_signup():
    def submit_signup():
        global stored_username, stored_password, unique_key
        admin_username = username_entry.get()
        admin_password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        favorite_movie = favorite_movie_entry.get()

        if len(admin_password) < 8 or not any(char.isdigit() for char in admin_password):
            messagebox.showerror("Error", "Password must be at least 8 characters long and contain letters and numbers.")
            return
        
        if admin_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        unique_key = generate_unique_key()
        stored_username = admin_username
        stored_password = hashlib.sha256(admin_password.encode()).hexdigest()

        with open(ADMIN_FILE, "w") as file:
            file.write(stored_username + "\n")
            file.write(stored_password + "\n")
            file.write(favorite_movie + "\n")
            file.write(str(unique_key) + "\n")

        messagebox.showinfo("Success", f"Admin signed up successfully! Your unique key is {unique_key}.")
        signup_window.destroy()

    signup_window = tk.Toplevel(root)
    signup_window.title("Admin Sign-Up")
    
    tk.Label(signup_window, text="Username").pack(pady=10)
    username_entry = tk.Entry(signup_window)
    username_entry.pack()

    tk.Label(signup_window, text="Create Password").pack(pady=10)
    password_entry = tk.Entry(signup_window, show="*")
    password_entry.pack()
    
    tk.Label(signup_window, text="Confirm Password").pack(pady=10)
    confirm_password_entry = tk.Entry(signup_window, show="*")
    confirm_password_entry.pack()
    
    tk.Label(signup_window, text="Favorite Movie (for password recovery)").pack(pady=10)
    favorite_movie_entry = tk.Entry(signup_window)
    favorite_movie_entry.pack()

    tk.Button(signup_window, text="Submit", command=submit_signup).pack(pady=10)

# Admin login
def admin_login():
    def submit_login():
        global stored_username, stored_password, unique_key
        admin_username = username_entry.get()
        admin_password = password_entry.get()

        if not stored_password or not stored_username:
            try:
                with open(ADMIN_FILE, "r") as file:
                    stored_username = file.readline().strip()
                    stored_password = file.readline().strip()
                    unique_key = int(file.readlines()[-1].strip())
            except FileNotFoundError:
                messagebox.showerror("Error", "No admin registered.")
                login_window.destroy()
                return

        hashed_password = hashlib.sha256(admin_password.encode()).hexdigest()

        if admin_username == stored_username and hashed_password == stored_password:
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            admin_panel()
        else:
            messagebox.showerror("Error", "Incorrect username or password!")
    
    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    
    tk.Label(login_window, text="Enter Admin Username").pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Enter Admin Password").pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Login", command=submit_login).pack(pady=10)

# Admin panel with view movie catalog and bookings
def admin_panel():
    admin_panel_window = tk.Toplevel(root)
    admin_panel_window.title("Admin Panel")

    def view_catalog():
        catalog_window = tk.Toplevel(admin_panel_window)
        catalog_window.title("Movies Catalog")

        movies = []
        with open(MOVIES_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                movies.append(row)

        tree = ttk.Treeview(catalog_window, columns=('Movie', 'Time', 'Seats Available'), show='headings')
        tree.heading('Movie', text='Movie')
        tree.heading('Time', text='Time')
        tree.heading('Seats Available', text='Seats Available')

        for row in movies:
            tree.insert('', 'end', values=row)

        tree.pack(fill=tk.BOTH, expand=True)

    def view_bookings():
        bookings_window = tk.Toplevel(admin_panel_window)
        bookings_window.title("Bookings List")

        bookings = []
        with open(BOOKINGS_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                bookings.append(row)

        tree = ttk.Treeview(bookings_window, columns=('User', 'Movie', 'Seats Booked'), show='headings')
        tree.heading('User', text='User')
        tree.heading('Movie', text='Movie')
        tree.heading('Seats Booked', text='Seats Booked')

        for row in bookings:
            tree.insert('', 'end', values=row)

        tree.pack(fill=tk.BOTH, expand=True)

    tk.Button(admin_panel_window, text="View Movie Catalog", command=view_catalog).pack(pady=10)
    tk.Button(admin_panel_window, text="View Bookings", command=view_bookings).pack(pady=10)
    tk.Button(admin_panel_window, text="Logout", command=admin_panel_window.destroy).pack(pady=10)

# Add Movie from Root Page (admin functionality)
def add_movie():
    def submit_movie():
        movie_name = movie_name_entry.get()
        movie_time = movie_time_entry.get()
        seats_available = seats_available_entry.get()
        write_movie_data([movie_name, movie_time, seats_available])
        messagebox.showinfo("Success", "Movie added successfully!")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Movie")
    
    tk.Label(add_window, text="Movie Name").pack(pady=5)
    movie_name_entry = tk.Entry(add_window)
    movie_name_entry.pack(pady=5)
    
    tk.Label(add_window, text="Movie Time").pack(pady=5)
    movie_time_entry = tk.Entry(add_window)
    movie_time_entry.pack(pady=5)
    
    tk.Label(add_window, text="Seats Available").pack(pady=5)
    seats_available_entry = tk.Entry(add_window)
    seats_available_entry.pack(pady=5)
    
    tk.Button(add_window, text="Submit", command=submit_movie).pack(pady=10)

# User login and book seats
def user_booking():
    def submit_booking():
        user_name = user_name_entry.get()
        selected_movie = movie_listbox.get(tk.ACTIVE)
        seats_to_book = seats_entry.get()

        # Fetch movie data and update seat availability
        movies = []
        with open(MOVIES_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == selected_movie:
                    available_seats = int(row[2])
                    if int(seats_to_book) <= available_seats:
                        row[2] = str(available_seats - int(seats_to_book))
                        write_booking_data([user_name, selected_movie, seats_to_book])
                        messagebox.showinfo("Success", f"Booked {seats_to_book} seats for {selected_movie}!")
                    else:
                        messagebox.showerror("Error", "Not enough seats available!")
                        return
                movies.append(row)

        # Update the CSV file
        with open(MOVIES_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(movies)

        booking_window.destroy()

    booking_window = tk.Toplevel(root)
    booking_window.title("Book Movie Tickets")

    tk.Label(booking_window, text="Your Name").pack(pady=5)
    user_name_entry = tk.Entry(booking_window)
    user_name_entry.pack(pady=5)

    tk.Label(booking_window, text="Select Movie").pack(pady=5)

    # Display movies in a listbox
    movie_listbox = tk.Listbox(booking_window)
    with open(MOVIES_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            movie_listbox.insert(tk.END, row[0])
    movie_listbox.pack(pady=5)

    tk.Label(booking_window, text="Number of Seats").pack(pady=5)
    seats_entry = tk.Entry(booking_window)
    seats_entry.pack(pady=5)

    tk.Button(booking_window, text="Book", command=submit_booking).pack(pady=10)

# Main application window
root = tk.Tk()
root.title("Cinema Booking System")

welcome_label = tk.Label(root, text="Welcome to Cinema Booking System", font=("Arial", 16, "bold"))
welcome_label.pack(pady=20)

admin_signup_button = tk.Button(root, text="Admin Sign Up", bg="#FF5722", fg="white", font=("Arial", 14, "bold"), command=admin_signup)
admin_signup_button.pack(pady=10)

admin_login_button = tk.Button(root, text="Admin Login", bg="#FF9800", fg="white", font=("Arial", 14, "bold"), command=admin_login)
admin_login_button.pack(pady=10)

add_movie_button = tk.Button(root, text="Add Movie", bg="#2196F3", fg="white", font=("Arial", 14, "bold"), command=add_movie)
add_movie_button.pack(pady=10)

user_booking_button = tk.Button(root, text="Book Movie Tickets", bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), command=user_booking)
user_booking_button.pack(pady=10)

# Run the application
root.mainloop()
