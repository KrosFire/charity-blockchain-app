from functools import wraps
from flask import Flask, redirect, render_template, session

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
    return render_template('dashboard.html')

