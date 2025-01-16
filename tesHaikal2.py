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

# Function to check if the password is in the wordlist
def check_wordlist(password):
    wordlist = load_wordlist()
    for word in wordlist:
        # Check if the word is part of the password
        if re.search(rf"{re.escape(word)}", password.lower()):
            return False, word  # Return False and the restricted word
    return True, None  # Return True if no restricted words are found

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

######################
    # Generate strength_check message
def valStrengh (password): 
    strength_is_valid, strength_errors = check_password_strength(password)
    if strength_is_valid:
        return "Password is strong."
    else:
        return "Password is weak. Issues: " + " | ".join(strength_errors)

 # Check password against wordlist
def valWordlist (password):
    wordlist_is_valid, restricted_word = check_wordlist(password)

    # Generate wordlist_check message
    if wordlist_is_valid:
        return "Password does not contain any restricted words."
    else:
        return f"Password contains a restricted word: {restricted_word}."

# Determine overall password safety (Bool)
def valSafe(password):
    strength_is_valid, strength_errors = check_password_strength(password) #jangan hapus strength_errors
    wordlist_is_valid, restricted_word = check_wordlist(password) #jangan hapus restricted_word
    if strength_is_valid and wordlist_is_valid:
        return 1
    else:
        return 0


#######################
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
            "strength_check": valStrengh(password),
            "wordlist_check": valWordlist(password),
            # "breach_check": pwned_result,
            "is_safe": valSafe(password),
            "password": password
        }
    }

    # Return the result as JSON
    return jsonify(result)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
