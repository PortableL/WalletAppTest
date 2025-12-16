from Wallet import create_app, db
from Wallet.models import User

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f"\n=== Total Users in Database: {len(users)} ===\n")
    
    if len(users) == 0:
        print("No users found in database!")
    else:
        for user in users:
            print(f"ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"Username: {user.username}")
            print(f"Full Name: {user.fullname}")
            print("-" * 40)