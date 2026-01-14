from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models.wallet import Wallet, Transaction
from ..extensions import db
from ..utils import no_cache

wallet_bp = Blueprint('wallet', __name__)

# Home/Dashboard - Show wallet balance and recent transactions
@wallet_bp.route('/home')
@login_required
def home():
    # Get or create wallet for current user
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    if not wallet:
        wallet = Wallet(user_id=current_user.id, balance=0.0)
        db.session.add(wallet)
        db.session.commit()
    
    # Get recent transactions (last 10)
    transactions = Transaction.query.filter_by(wallet_id=wallet.id)\
                                   .order_by(Transaction.date.desc())\
                                   .limit(10).all()
    
    return render_template('wallet/Home.html', 
                         user=current_user, 
                         wallet=wallet,
                         transactions=transactions)


# Cash In Options page
@wallet_bp.route('/cashin-options')
@login_required
def cashin_options():
    return render_template('wallet/CashInOptions.html', user=current_user)


# Cash In - Add money to wallet
@wallet_bp.route('/cashin', methods=['GET', 'POST'])
@login_required
def cashin():
    if request.method == 'POST':
        try:
            # Get and validate amount
            amount = float(request.form.get('amount', 0))
            
            if amount <= 0:
                flash('Amount must be greater than 0', category='error')
                return redirect(url_for('wallet.cashin'))
            
            # Get or create user's wallet
            wallet = Wallet.query.filter_by(user_id=current_user.id).first()
            if not wallet:
                wallet = Wallet(user_id=current_user.id, balance=0.0)
                db.session.add(wallet)
                db.session.flush()  # Get wallet.id before creating transaction
            
            # Update balance
            wallet.balance += amount
            
            # Create transaction record
            transaction = Transaction(
                amount=amount,
                transaction_type='cash_in',
                description=request.form.get('description', 'Cash In'),
                wallet_id=wallet.id
            )
            db.session.add(transaction)
            
            # Save to database
            db.session.commit()
            
            flash(f'Successfully added ₱{amount:.2f} to your wallet!', category='success')
            return redirect(url_for('wallet.home'))
            
        except ValueError:
            flash('Invalid amount. Please enter a valid number.', category='error')
            return redirect(url_for('wallet.cashin'))
        
        except Exception as e:
            db.session.rollback()  # Rollback if error occurs
            flash('An error occurred. Please try again.', category='error')
            print(f"Error: {e}")  # For debugging
            return redirect(url_for('wallet.cashin'))
    
    # GET request - show the form
    return render_template('wallet/Cashin.html', user=current_user)


# Optional: Cash Out route
@wallet_bp.route('/cashout', methods=['GET', 'POST'])
@login_required
def cashout():
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            
            if amount <= 0:
                flash('Amount must be greater than 0', category='error')
                return redirect(url_for('wallet.cashout'))
            
            # Get wallet
            wallet = Wallet.query.filter_by(user_id=current_user.id).first()
            
            if not wallet or wallet.balance < amount:
                flash('Insufficient balance', category='error')
                return redirect(url_for('wallet.cashout'))
            
            # Update balance
            wallet.balance -= amount
            
            # Create transaction
            transaction = Transaction(
                amount=amount,
                transaction_type='cash_out',
                description=request.form.get('description', 'Cash Out'),
                wallet_id=wallet.id
            )
            db.session.add(transaction)
            db.session.commit()
            
            flash(f'Successfully withdrawn ₱{amount:.2f}', category='success')
            return redirect(url_for('wallet.home'))
            
        except ValueError:
            flash('Invalid amount', category='error')
            return redirect(url_for('wallet.cashout'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred', category='error')
            return redirect(url_for('wallet.cashout'))
    
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    return render_template('wallet/CashOut.html', user=current_user, wallet=wallet)