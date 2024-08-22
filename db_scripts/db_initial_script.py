import sqlite3
from werkzeug.security import generate_password_hash

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create the Books table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Books (
    BookID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Author TEXT NOT NULL,
    ISBN TEXT UNIQUE,
    PublishedYear INTEGER,
    AvailableCopies INTEGER NOT NULL,
    Image TEXT
)
""")

# Create the Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT UNIQUE NOT NULL,
    PasswordHash TEXT NOT NULL,
    Name TEXT NOT NULL,
    Email TEXT UNIQUE,
    Phone TEXT
)
""")

# Insert sample data into Books table
books = [
    ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", 1925, 5, "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/The_Great_Gatsby_Cover_1925_Retouched.jpg/220px-The_Great_Gatsby_Cover_1925_Retouched.jpg"),
    ("To Kill a Mockingbird", "Harper Lee", "9780061120084", 1960, 3, "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg/220px-To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg"),
    ("1984", "George Orwell", "9780451524935", 1949, 4, "https://upload.wikimedia.org/wikipedia/en/5/51/1984_first_edition_cover.jpg"),
    ("Moby Dick", "Herman Melville", "9781503280786", 1851, 2, "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Moby-Dick_FE_title_page.jpg/220px-Moby-Dick_FE_title_page.jpg"),
]

cursor.executemany("""
INSERT INTO Books (Title, Author, ISBN, PublishedYear, AvailableCopies, Image)
VALUES (?, ?, ?, ?, ?, ?)
""", books)

# Generate password hash
password_hash = generate_password_hash('123')

# Insert sample data into Users table
users = [
    ("user1", password_hash, "Alice Johnson", "alice.johnson@example.com", "555-1234"),
    ("user2", password_hash, "Bob Smith", "bob.smith@example.com", "555-5678"),
    ("user3", password_hash, "Carol White", "carol.white@example.com", "555-8765"),
]

cursor.executemany("""
INSERT INTO Users (Username, PasswordHash, Name, Email, Phone)
VALUES (?, ?, ?, ?, ?)
""", users)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup and sample data inserted successfully.")
