from flask import Flask, request, jsonify
import re
import string
import sqlite3
import os
import json

app = Flask(__name__)

# Connect to SQLite database
def connect_db():
    consql = sqlite3.connect("wordlist.db")
    return consql

# Initialize database
def init_db():
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'wordlist.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Buat tabel respon jika belum ada
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS respon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            origin TEXT NOT NULL,
            respon TEXT NOT NULL
        )
        ''')
        
        # Buat tabel wordlist jika belum ada
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS wordlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE,
            count INTEGER DEFAULT 0
        )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

def save_access_log(ip, origin, response_data):
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'wordlist.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Konversi response_data ke JSON string
        response_json = json.dumps(response_data)
        
        # Simpan ke database
        cursor.execute(
            'INSERT INTO respon (ip, origin, respon) VALUES (?, ?, ?)',
            (ip, origin, response_json)
        )
        
        conn.commit()
        conn.close()
        print(f"Access log saved for IP: {ip}")
    except Exception as e:
        print(f"Error saving access log: {e}")

# Load wordlist from database SQLite
def load_wordlist():
    with connect_db() as consql:
        cursor = consql.cursor()
        cursor.execute("SELECT word FROM wordlist")
        words = [row[0].lower() for row in cursor.fetchall()]
    return words

# Function to check if the password is in the wordlist and update counter
def check_wordlist(password):
    wordlist = load_wordlist()
    found_words = set()
    for word in wordlist:
        if re.search(rf"{re.escape(word)}", password.lower()) and word not in found_words:
            update_word_count(word)
            found_words.add(word)
            return False, word
    return True, None

# Function to update the word count in the database
def update_word_count(word):
    consql = connect_db()
    cursor = consql.cursor()
    cursor.execute("UPDATE wordlist SET count = count + 1 WHERE word = ?", (word,))
    consql.commit()
    consql.close()

# Function to check password strength with detailed feedback
def check_password_strength(password):
    errors = []

    if len(password) < 12:
        errors.append("Password should be at least 12 characters long.")
    if not re.search(r'[A-Z]', password):
        errors.append("Password should contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        errors.append("Password should contain at least one lowercase letter.")
    if not re.search(r'[0-9]', password):
        errors.append("Password should contain at least one number.")
    if not any(char in string.punctuation for char in password):
        errors.append("Password should contain at least one special character.")
    if re.search(r'(.)\1{3,}', password):
        errors.append("Password contains too many repeated characters.")
    if re.search(r'(012|123|234|345|456|567|678|789|987|876|765|654|543|432|321)', password):
        errors.append("Password contains sequential numbers.")
    if errors:
        return False, errors
    return True, []

# Core function to evaluate the password
def evaluate_password(password):
    wordlist_is_valid, restricted_word = check_wordlist(password)
    strength_is_valid, strength_errors = check_password_strength(password)

    strength_check_msg = (
        "Password is strong." 
        if strength_is_valid 
        else f"Password is weak. Issues: " + " | ".join(strength_errors)
    )
    wordlist_check_msg = (
        "Password does not contain any restricted words."
        if wordlist_is_valid
        else f"Password contains a restricted word: {restricted_word}."
    )
    is_safe = 1 if strength_is_valid and wordlist_is_valid else 0

    return {
        "strength_check": strength_check_msg,
        "wordlist_check": wordlist_check_msg,
        "is_safe": is_safe,
        "password": password,
    }

# Flask route
@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password', '')

    # Get IP and origin
    ip = request.remote_addr
    origin = request.headers.get('Origin', 'Unknown')

    # Call the evaluation function
    result = evaluate_password(password)

    # Save access log
    save_access_log(ip, origin, result)

    # Return the result as JSON
    return jsonify({"check_results": result})

@app.route('/add_wordlist', methods=['POST'])
def add_wordlist():
    data = request.get_json()
    new_word = data.get('word', '').lower()

    if not new_word:
        return jsonify({"error": "Word is required."}), 400

    consql = connect_db()
    cursor = consql.cursor()
    cursor.execute("SELECT word FROM wordlist WHERE word = ?", (new_word,))
    existing_word = cursor.fetchone()

    if existing_word:
        consql.close()
        return jsonify({"message": "Word already exists in the wordlist."}), 200

    cursor.execute("INSERT INTO wordlist (word) VALUES (?)", (new_word,))
    consql.commit()
    consql.close()

    return jsonify({"message": f"Word '{new_word}' has been added to the wordlist."}), 201

@app.route('/delete_wordlist', methods=['DELETE'])
def delete_wordlist():
    data = request.get_json()
    word_to_delete = data.get('word', '').lower()

    if not word_to_delete:
        return jsonify({"error": "Word is required."}), 400

    with connect_db() as consql:
        cursor = consql.cursor()
        cursor.execute("SELECT word FROM wordlist WHERE word = ?", (word_to_delete,))
        existing_word = cursor.fetchone()

        if not existing_word:
            return jsonify({"message": "Word does not exist in the wordlist."}), 404

        cursor.execute("DELETE FROM wordlist WHERE word = ?", (word_to_delete,))
        consql.commit()

    return jsonify({"message": f"Word '{word_to_delete}' has been deleted from the wordlist."}), 200

# Run the application
if __name__ == '__main__':
    init_db()  # Initialize database when starting the application
    app.run(debug=True)
