from flask import request, jsonify
from config import create_app
from models import Wordlist
from utils import evaluate_password, save_access_log

# Create app, db, and limiter
app, db, limiter = create_app()

# Flask routes
@app.route('/check_password', methods=['POST'])
@limiter.limit("200 per minute")
def check_password():
    data = request.get_json()
    password = data.get('password', '')

    ip = request.remote_addr
    origin = request.headers.get('Origin', 'Unknown')

    result = evaluate_password(password)
    save_access_log(ip, origin, result)

    return jsonify({"check_results": result})

@app.route('/add_wordlist', methods=['POST'])
@limiter.limit("50 per minute")
def add_wordlist():
    data = request.get_json()
    new_word = data.get('word', '').lower()

    if not new_word:
        return jsonify({"error": "Word is required."}), 400

    existing_word = Wordlist.query.filter_by(word=new_word).first()

    if existing_word:
        return jsonify({"message": "Word already exists in the wordlist."}), 200

    new_word_entry = Wordlist(word=new_word)
    db.session.add(new_word_entry)
    db.session.commit()

    return jsonify({"message": f"Word '{new_word}' has been added to the wordlist."}), 201

@app.route('/delete_wordlist', methods=['DELETE'])
@limiter.limit("50 per minute")
def delete_wordlist():
    data = request.get_json()
    word_to_delete = data.get('word', '').lower()

    if not word_to_delete:
        return jsonify({"error": "Word is required."}), 400

    word_entry = Wordlist.query.filter_by(word=word_to_delete).first()

    if not word_entry:
        return jsonify({"message": "Word does not exist in the wordlist."}), 404

    db.session.delete(word_entry)
    db.session.commit()

    return jsonify({"message": f"Word '{word_to_delete}' has been deleted from the wordlist."}), 200