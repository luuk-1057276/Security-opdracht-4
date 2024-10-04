from flask import Flask, redirect, url_for, render_template, request, session, request, Blueprint, jsonify
from models.SQLalchemy import db
from routes.admin import admin
from routes.api import api
from routes.auth import auth
from routes.inquiry import inquiry
from models.model import *
import random
import string
import hashlib
import os
file_path = os.path.abspath(os.getcwd())+"/database/wp3.db"

app = Flask(__name__, template_folder='templates')
app.secret_key = 'wp3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path  # Use your SQLite database file path
db.init_app(app)

with app.app_context():
    db.create_all()
    
# get current path
print(os.path.dirname(os.path.abspath(__file__)))

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(auth)
app.register_blueprint(inquiry, url_prefix='/inquiry')

# # ! debug mode staat aan maar werkt niet dus weghalen
# environ["FLASK_DEBUG"] = '1'


@app.route("/")
def index():
    return redirect(url_for('auth.login'))


@app.template_filter('add_line_breaks')
def add_line_breaks(text):
    return text.replace('\n', ' ')


@app.route("/my_account", methods=['GET', 'POST'])
def my_account():
    is_old = check_is_old(session['mail'])
    return render_template("user/my_account.jinja", is_old=is_old)

@app.route("/hash_password", methods=['GET', 'POST'])
def hash_password():
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    password = get_password(session['mail'])
    salted_password = password + salt
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    hash_old_password(session['mail'], hashed_password, salt)
    return redirect(url_for('my_account'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
