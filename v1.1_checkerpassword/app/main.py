from routes import app, db

def main():
    # Additional setup or configuration can be added here if needed
    with app.app_context():
        db.create_all()  # Ensure database tables are created
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()