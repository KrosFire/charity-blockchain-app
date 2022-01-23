from functools import wraps
from json import JSONDecoder, JSONEncoder
from flask import Flask, redirect, render_template, request, session
from main import app
from user.models import User

@app.route('/user/signup', methods=['POST'])
def signup():
    data = JSONDecoder().decode(request.data.decode())
    return User().signup(data['name'], data['email'], data['password'])

@app.route('/user/signin', methods=['POST'])
def signin():
    data = JSONDecoder().decode(request.data.decode())
    return User().signin(data['email'], data['password'])

@app.route('/user/signout')
def signout():
    return User().signout()