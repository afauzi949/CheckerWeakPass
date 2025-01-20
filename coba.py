from flask import Flask, request, jsonify
import re
import requests
import string
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
def connect_db():
    consql = sqlite3.connect("CheckerWeakPass\wordlist.db")
    return consql

# Load wordlist from database SQLite
def load_wordlist():
    consql = connect_db()
    cursor = consql.cursor()
    cursor.execute("SELECT word FROM wordlist")
    words = [row[0].lower() for row in cursor.fetchall()]
    consql.close()
    return words

# Function to check if the password is in the wordlist
def check_wordlist(password):
    wordlist = load_wordlist()
    for word in wordlist:
        # Check if the word is part of the password
        if re.search(rf"{re.escape(word)}", password.lower()):
            return f"Password contains a restricted word: {word}."
    return "Password does not contain any restricted words."

# Function to check password strength with detailed feedback
def check_password_strength(password):
    errors = []
    len_error = False
    upper_error = False
    lower_error = False
    number_error = False
    symbols_error = False
    repeat_error = False
    sequantial_number_error = False
    
    if len(password) < 12:
        errors.append("Password should be at least 12 characters long.")
        len_error = True
    if not re.search(r'[A-Z]', password):
        errors.append("Password should contain at least one uppercase letter.")
        upper_error = True
    if not re.search(r'[a-z]', password):
        errors.append("Password should contain at least one lowercase letter.")
        lower_error = True
    if not re.search(r'[0-9]', password):
        errors.append("Password should contain at least one number.")
        number_error = True
    if not any(char in string.punctuation for char in password):
        errors.append("Password should contain at least one special character.")
        symbols_error = True
    if re.search(r'(.)\1{3,}', password):
        errors.append("Password contains too many repeated characters.")
        repeat_error = True
    if re.search(r'(012|123|234|345|456|567|678|789|987|876|765|654|543|432|321)', password):
        errors.append("Password contains sequential numbers.")
        sequantial_number_error = True
        
    result = {
            "len_error" : len_error,
            "upper_error" : upper_error,
            "lower_error" : lower_error,
            "number_error" : number_error,
            "symbols_error" : symbols_error,
            "repeat_error" : repeat_error,
            "sequantial_number_error" : sequantial_number_error,
        }
    
    return result

# Route to check password strength and wordlist comparison
@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password', '')

    # Validate password strength
    strength_result = check_password_strength(password)

    # Check password against wordlist
    wordlist_result = check_wordlist(password)

    # Combine all results into a single response dictionary
    result = {
        "check_results": {
            "strength_check": strength_result,
            "wordlist_check": wordlist_result,
            "password": password
        }
    }

    # Return the result as JSON
    return jsonify(result)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
