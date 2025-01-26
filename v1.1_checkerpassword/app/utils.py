import re
import string
import json
from models import db, Wordlist, AccessLog

# Utility Functions
def save_access_log(ip, origin, response_data):
    try:
        response_json = json.dumps(response_data)
        new_log = AccessLog(ip=ip, origin=origin, respon=response_json)
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        print(f"Error saving access log: {e}")

def load_wordlist():
    return [word.word.lower() for word in Wordlist.query.all()]

def check_wordlist(password):
    wordlist = load_wordlist()
    found_words = set()
    for word in wordlist:
        if re.search(rf"{re.escape(word)}", password.lower()) and word not in found_words:
            update_word_count(word)
            found_words.add(word)
            return False, word
    return True, None

def update_word_count(word):
    word_entry = Wordlist.query.filter_by(word=word).first()
    if word_entry:
        word_entry.count += 1
        db.session.commit()

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
    
    return (True, []) if not errors else (False, errors)

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