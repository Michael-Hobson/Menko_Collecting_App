from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models import model_user
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/user/create', methods=['POST'])
def create_user_register():

    if User.validate_registration(request.form) == False:
        return redirect('/login')

    user_exists = User.get_email(request.form)
    if user_exists != None:
        flash("This email already exists", "error_registration_email")
        return redirect('/login')

    data = {
        **request.form,
        "password": bcrypt.generate_password_hash(request.form['password'])
    }

    user_id = User.create(data)

    session['first_name'] = data['first_name']
    session['user_id'] = user_id

    return redirect('/menko')


@app.route('/user/login', methods=['POST'])
def process_login():

    if User.validate_login(request.form) == False:
        return redirect('/login')

    current_user = User.get_email(request.form)
    if current_user == None:
        flash("This email does not exist", "error_email_login_info")
        return redirect('/login')

    if current_user != None:
        if not bcrypt.check_password_hash(current_user.password, request.form['password']):
            flash("Wrong credentials", "error_password_login_info")
            return redirect('/login')

        session['first_name'] = current_user.first_name
        session['user_id'] = current_user.id

        return redirect('/menko')

    else:
        flash("Wrong credentials", "error_email_login_info")
        return redirect('/login')


@app.route('/user/logout')
def logout_user():
    session.clear()
    return redirect('/')


# @app.route('/home')
# def display_homepage():
#     return render_template('index.html')
