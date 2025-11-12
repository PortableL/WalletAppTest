from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

wallet_balance = {"balance": 0.00}

# balance reflect
@app.route('/')
def home():
    return render_template('Home.html', balance=wallet_balance["balance"])

# cash in options
@app.route('/cashin-options')
def cashin_options():
    return render_template('CashInOptions.html')

# to add cash in value
@app.route('/cashin', methods=['GET', 'POST'])
def cashin():
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            if amount <= 0:
                raise ValueError("Invalid amount")
            wallet_balance['balance'] += amount
            return redirect(url_for('home'))
        except:
            return "Invalid input", 400
    return render_template('Cashin.html')

# Savenow button
@app.route('/save-now')
def save_now():
    return render_template('Savenow.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
