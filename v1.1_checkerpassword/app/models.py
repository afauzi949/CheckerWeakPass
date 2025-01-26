from config import create_app

# Create app, db, and limiter
app, db, limiter = create_app()

# Database Models
class AccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(255), nullable=False)
    origin = db.Column(db.String(255), nullable=False)
    respon = db.Column(db.Text, nullable=False)

class Wordlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(255), unique=True, nullable=False)
    count = db.Column(db.Integer, default=0)

# Initialize the database
with app.app_context():
    db.create_all()
