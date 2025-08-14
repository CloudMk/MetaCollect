from flask import Flask, render_template, request, jsonify
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS submissions (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     email TEXT NOT NULL
                     )''')
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error initializing database: {e}")

# Call init_db when the app starts
init_db()

@app.route('/')
def welcom():
    return render_template('view/welcome.html')

@app.route('/auth')
def index():
    return render_template('view/auth.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    
    if name and email:
        try:
            # Store data in SQLite database
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO submissions (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Merci pour votre soumission !'}), 200
        except Error as e:
            print(f"Error saving to database: {e}")
            return jsonify({'message': 'Erreur lors de l\'enregistrement.'}), 500
    else:
        return jsonify({'message': 'Veuillez remplir tous les champs.'}), 400