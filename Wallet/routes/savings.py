# Wallet/routes/savings.py
from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from . import db

savings_bp = Blueprint('savings', __name__)

@savings_bp.route('/save-now')
@login_required
def save_now():
    return render_template('savings/Savenow.html', user=current_user)

# You can add more savings routes later:
# @savings_bp.route('/goals')
# @savings_bp.route('/transfer-to-savings')