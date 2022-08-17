import string
from flask import Blueprint, Flask, render_template, request, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired
from .models import users_collection

auth = Blueprint('auth', __name__)

# login form class
class FormLogin(FlaskForm):
    userName = StringField("Username: ", [DataRequired()])
    password = PasswordField("Password: ", [DataRequired()])
    submit = SubmitField("Accedi")

@auth.route('/Login', methods=['GET','POST'])
def login():
    userName = ""
    password = ""
    prevUrl = request.referrer

    form = FormLogin()
    if form.validate_on_submit():
        userName = form.userName.data
        password = form.password.data
        try:
            # cerchiamo nel database i dati inseriti se esistono
            user = users_collection.find_one({"userName":userName, "password":password},{"_id":0, "userName":1, "admin":1})
            username = user['userName']
            admin = user['admin']
            form.userName.data = ""
            form.password.data = ""
            # reindiriziamo alla home
            if not admin:
                session['user'] = username
                flash(f"Bentornato {username}", "success")
            else:
                session['admin'] = username
                flash(f"Bentornato admin {username}", "success")
            return redirect(url_for("views.home"))
        except:
            # si ricarica la pagina e resettiamo i dati inseriti dall utente con un messaggio di errore
            form.userName.data = ""
            form.password.data = ""
            flash("Utente non registrato", "error")

    return render_template('login.html', form=form, prevUrl=prevUrl)

@auth.route('/Logout')
def logout():
    session.pop('user', None)
    session.pop('admin', None)
    flash("Disconnesso", "error")
    return redirect(url_for('views.home'))

# Signin form class
class FormSignin(FlaskForm):
    firstName = StringField("Nome: ", [DataRequired()])
    lastName = StringField("Cognome: ", [DataRequired()])
    mail = EmailField("Email: ", [DataRequired()])
    userName = StringField("Username: ", [DataRequired()])
    password = PasswordField("Password: ", [DataRequired()])
    ConfirmPassword = PasswordField("Conferma password: ", [DataRequired()])
    submit = SubmitField("Registrati")

import re

@auth.route('/Sign-in', methods=['GET','POST'])
def sign_in():
    fName = ""
    lName = ""
    user = ""
    mail = ""
    password = ""
    password2 = ""
    prevUrl = request.referrer

    form = FormSignin()
    if form.validate_on_submit():
        fName = form.firstName.data
        lName = form.lastName.data
        user = form.userName.data
        mail = form.mail.data
        password = form.password.data
        password2 = form.ConfirmPassword.data

        nameRegex = r'^[a-zA-Z]*\s?[a-zA-Z]*'
        if re.fullmatch(nameRegex, fName):
            if " " in fName:
                fName = str.lower(fName).split(" ")
                newString = ""
                for name in fName:
                    name = str.capitalize(name)
                    newString += name + " "
                fName = newString
            else:
                fName = str.capitalize(fName)
            if re.fullmatch(nameRegex, lName):
                if " " in lName:
                    lName = str.lower(lName).split(" ")
                    newString = ""
                    for name in lName:
                        name = str.capitalize(name)
                        newString += name + " "
                    lName = newString
                else:
                    lName = str.capitalize(lName)
                mailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                if re.fullmatch(mailRegex, mail):
                    symbols = list("@_!#$%^&*()<>?/\|}{~:]")
                    userNotOk = any(c in user for c in symbols)
                    if not userNotOk:
                        userExist = users_collection.find_one({"userName":user})
                        if not userExist:
                            if password == password2:
                                maxId = users_collection.find({},{'user_id':1}).sort("user_id", -1).limit(1)
                                for i in maxId:
                                    n = (int)(i["user_id"]) + 1
                                newUser = {"user_id":n, "firstName":fName, "lastName":lName, "userName":user, "password":password, "mail":mail, "admin":False}
                                result = users_collection.insert_one(newUser)
                                form.firstName.data = ""
                                form.lastName.data = ""
                                form.userName.data = ""
                                form.mail.data = ""
                                form.password.data = ""
                                form.ConfirmPassword.data = ""

                                # reindiriziamo alla home
                                session['user'] = user
                                flash(f"Benvenuto {user}", "success")
                                return redirect(url_for("views.home"))
                            else:
                                form.password.data = ""
                                form.ConfirmPassword.data = ""
                                flash("Le password non coincidono", "error")
                                return render_template('sign_in.html', form=form)
                        else:
                            form.userName.data = ""
                            flash("Username già in uso", "error")
                            return render_template('sign_in.html', form=form)
                    else:
                        form.userName.data = ""
                        flash("Username non valido", "error")
                        return render_template('sign_in.html', form=form)
                else:
                    form.mail.data = ""
                    flash("Email non valida", "error")
                    return render_template('sign_in.html', form=form)
            else:
                form.lastName.data = ""
                flash("Cognome non valido", "error")
                return render_template('sign_in.html', form=form)
        else:
            form.firstName.data = ""
            flash("Nome non valido", "error")
            return render_template('sign_in.html', form=form)
        
    return render_template('sign_in.html', form=form, prevUrl=prevUrl)
