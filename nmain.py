from flask import Flask, request, jsonify
import re
import hashlib
import requests
import string

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

# Function to check if password has been exposed in data breaches
def check_pwned_password(password):
    try:
        # Create SHA-1 hash of the password
        sha1_pass = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix, suffix = sha1_pass[:5], sha1_pass[5:]
        
        # Query the API
        response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')
        
        if response.status_code == 200:
            # Check if password hash exists in the response
            for line in response.text.splitlines():
                hash_suffix, count = line.split(':')
                if hash_suffix == suffix:
                    return f'This password has been exposed in {count} data breaches.'
            
            return 'This password hasn\'t been found in any known data breaches.'
            
    except Exception as e:
        return 'Unable to check password breach status.'

# Function to check password strength
def check_password_strength(password):
    if len(password) < 12:
        return "Password should be at least 12 characters long."
    if not re.search(r'[A-Z]', password):
        return "Password should contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return "Password should contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return "Password should contain at least one number."
    if not re.search(r'(.)\1{5,}', password):
        return "Password mengandung karakter ganda terlalu banyak"
    if not re.search(re.search(r'(012|123|234|345|456|567|678|789|987|876|765|654|543|432|321)', password)):
        return "Password mengandung angka urut"
    if not any(char in string.punctuation for char in password):
        return "Password should contain at least one special character."
    if re.search(r'(password|1234|qwerty|admin)', password, re.IGNORECASE):
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

    # Check if password has been exposed in data breaches
    pwned_result = check_pwned_password(password)

    # Combine all results into a single response dictionary
    result = {
        "check_results": {
            "strength_check": strength_result,
            "wordlist_check": wordlist_result,
            "breach_check": pwned_result,
            "password": password
        }
    }

    # Return the result as JSON
    return jsonify(result)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

