from functools import wraps
from json import JSONDecoder, JSONEncoder
from flask import Flask, redirect, render_template, request, session, jsonify
from blockchain.blockchain import Blockchain
from main import app
from user.models import User
from database.db_setup import Database

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

@app.route('/user/donation', methods=['POST'])
def donate():
    data = JSONDecoder().decode(request.data.decode())
    bc = Blockchain()
    
    status, info = bc.make_donation(session['user']['_id'], int(data['amount']), data['private-key'])
    return jsonify({ 'info': info }), 200 if status else 400

@app.route('/user/balance')
def balance():
    balance = Blockchain().get_user_balance(session['user']['_id'])
    return jsonify({ 'balance': balance }), 200
