from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def load_wordlist():
    with open("seclist.txt", "r") as file:
        return [line.strip().lower() for line in file.readlines()]

# Load wordlist on startup
wordlist = load_wordlist()

# Function to check if the password is in the wordlist
def check_wordlist(password):
    if password.lower() in wordlist:
        return "Password is too common. Avoid using dictionary words."
    return "Password is not in the wordlist."

# Function to check password strength
def check_password_strength(password):
    if len(password) < 8:
        return "Password should be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return "Password should contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return "Password should contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return "Password should contain at least one number."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password should contain at least one special character."
    if re.search(r'(password|1234|qwerty)', password, re.IGNORECASE):
        return "Password should not contain easily guessable patterns."
    return "Password is strong."

# Route to check password strength and wordlist comparison
@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password', '')

    # Validate password strength
    strength_result = check_password_strength(password)

    # Check password against wordlist
    wordlist_result = check_wordlist(password)

    # Combine both results
    result = {
        "password": password,
        "strength": strength_result,
        "wordlist_check": wordlist_result
    }

    # Return the result as JSON
    return jsonify(result)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
