from flask import Blueprint, Flask, render_template, request, session, redirect, url_for, flash

views = Blueprint('views', __name__)

@views.route('/')
def base():
    return render_template('base.html')

@views.route('/Homepage')
def home():
    return render_template('homepage.html')