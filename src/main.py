from functools import wraps
from flask import Flask, redirect, render_template, session
from blockchain.blockchain import Blockchain
from database.db_setup import Database

def login_req(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        return redirect('/')
    return wrap

app = Flask(__name__)
app.secret_key = 'my_little_secret'
from user import routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/')
@login_req
def dashboard():
    bc = Blockchain()
    balance = bc.get_user_balance(session['user']['_id'])
    transactions = bc.list_transactions()
    
    return render_template('dashboard.html', balance=balance, transactions=transactions)

