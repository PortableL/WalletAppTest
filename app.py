from flask import Flask, render_template, request, redirect, url_for, Request, flash
 

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'


wallet_balance = {"balance": 0.00}


@app.route('/')
def index():
    return redirect(url_for('login'))

# balance reflect
@app.route('/home')
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


#login.html
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print("Username:", username)
        print("Password:", password)

        if username and password:
            flash("Login Succesful!", "success")
            # Login successful → redirect to home
            return redirect(url_for('home'))
        else:
            # Invalid login → show message
            flash("Invalid Login", "error")

    # For GET request or failed POST, render login page
    return render_template('Login.html')







if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

