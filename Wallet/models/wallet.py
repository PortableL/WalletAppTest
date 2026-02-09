from ..extensions import db
from sqlalchemy.sql import func

class Wallet(db.Model):
    __tablename__ = "wallets"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    transaction_type = db.Column(db.String(50))  # ← ADD THIS LINE
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'))