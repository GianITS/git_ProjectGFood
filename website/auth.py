from flask import Blueprint, Flask, render_template, request, session, redirect, url_for, flash

auth = Blueprint('auth', __name__)

@auth.route('/Login')
def login():
    return render_template('login.html')

@auth.route('/Sign-up')
def sign_up():
    return render_template('sign_up.html')
