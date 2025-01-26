from config import create_app, db
from models import AccessLog, Wordlist
from routes import init_routes

app, limiter = create_app()
init_routes(app, limiter)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
