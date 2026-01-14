from Wallet.routes import create_app, db

app = create_app()

#to create Tables.
with app.app_context():
    db.create_all()
    print("All tables created successfully!")