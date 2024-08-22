from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = '123'  # Replace with a proper secret key

# Function to get the list of books from the database
def get_books():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    conn.close()
    return books

# Function to authenticate user
def authenticate_user(username, password):
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE Username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user['PasswordHash'], password):
        return user
    return None

@app.route('/')
def book_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    books = get_books()
    return render_template('books.html', books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user['UserID']
            session['username'] = user['Username']
            flash('Login successful!', 'success')
            return redirect(url_for('book_list'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
