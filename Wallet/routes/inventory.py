from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
# from ..models.inventory import Inventory, Item  # Create these models
from ..extensions import db

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
@login_required
def inventory_list():
    return render_template('inventory/Inventory.html', user=current_user)

@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        # Add item logic
        flash('Item added successfully!', 'success')
        return redirect(url_for('inventory.inventory_list'))
    return render_template('inventory/AddItem.html', user=current_user)