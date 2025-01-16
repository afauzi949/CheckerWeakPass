from flask import Flask, request, jsonify
import re
import string
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
def connect_db():
    consql = sqlite3.connect("D:\Kuliah\Magang\(PI) Diskominfo DIY\Cekpass\wordlist.db")
    return consql

# Load wordlist from database SQLite
def load_wordlist():
    consql = connect_db()
    cursor = consql.cursor()
    cursor.execute("SELECT word FROM wordlist")
    words = [row[0].lower() for row in cursor.fetchall()]
    consql.close()
    return words

# Function to check if the password is in the wordlist and update counter
def check_wordlist(password):
    wordlist = load_wordlist()
    found_words = set()  # To track already found words and avoid updating multiple times

    for word in wordlist:
        # Check if the word is part of the password
        if re.search(rf"{re.escape(word)}", password.lower()) and word not in found_words:
            # Update the counter for this word only once
            update_word_count(word)
            found_words.add(word)  # Add the word to the found set
            return False, word  # Return False and the restricted word

    return True, None  # Return True if no restricted words are found

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
        return False, errors  # Password is weak
    return True, []  # Password is strong

# Core function to evaluate the password
def evaluate_password(password):
    # Cache the results of wordlist and strength checks
    wordlist_is_valid, restricted_word = check_wordlist(password)
    strength_is_valid, strength_errors = check_password_strength(password)

    # Generate responses
    wordlist_check_msg = (
        "Password does not contain any restricted words."
        if wordlist_is_valid
        else f"Password contains a restricted word: {restricted_word}."
    )
    is_safe = 1 if strength_is_valid and wordlist_is_valid else 0

    # Return combined results
    return {
        "strength_check": (
            "Password is strong." if strength_is_valid else
            "Password is weak. Issues: " + " | ".join(strength_errors)
        ),
        "wordlist_check": wordlist_check_msg,
        "is_safe": is_safe,
        "password": password,
    }

# Flask route
@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password', '')

    # Call the evaluation function
    result = evaluate_password(password)

    # Return the result as JSON
    return jsonify({"check_results": result})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
