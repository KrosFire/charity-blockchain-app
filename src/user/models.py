from flask import Flask, jsonify, redirect, session
from uuid import uuid4
from hashlib import sha256
from markupsafe import re
from rsa import newkeys
from database.db_setup import Database
from blockchain.blockchain import Blockchain


class User():
    def start_session(self, user):
      del user['password']
      session['logged_in'] = True
      session['user'] = user
    
    
    def signup(self, name: str, email: str, password: str) -> tuple[str, int]:
        pub_key, private_key = newkeys(512)
        
        user = {
          '_id': uuid4().hex.strip(),
          'name': name.strip(),
          'email': email.strip(),
          'password': sha256(password.encode()).hexdigest().strip(),
          'public_key': pub_key.save_pkcs1().decode().strip(),
          'balance': 0
        }
        
        users_col = Database().get_users_collection()
        
        if users_col.find_one({ 'email': user['email'] }):
          return jsonify({ 'error': 'User with this email already exists!' }), 400
        
        
        if users_col.insert_one(user):
          # We give users from the start 100 CT
          Blockchain().give_user_ct(user['_id'])
          self.start_session(user)
          return jsonify({
              'private_key': private_key.save_pkcs1().decode()
              }), 200
        
        return jsonify({ 'error': 'Signup failed' }), 400
    
    
    def signin(self, email: str, password: str) -> tuple[str, int]:
        
        users_col = Database().get_users_collection()
        password = sha256(password.encode()).hexdigest()
        
        print(email)
        print(password)
        print(users_col.find_one({ 'email': email, 'password': password }))
        user = users_col.find_one({ 'email': email, 'password': password })
        if user != None:
          self.start_session(user)
          return jsonify({ 'info': 'Successful login.' }), 200
        
        return jsonify({ 'error': 'Invalid credentials' }), 400

    def signout(self):
      session.clear()
      return redirect('/')