import requests
import base64
from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models import model_menko
from flask_app.models.model_menko import Menko
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/menko')
def display_all_menko():
    if 'user_id' not in session:
        return redirect('/')

    menko = Menko.get_all_with_users()
    return render_template('dashboard_all_menko.html', menko=menko)


@app.route('/menko/new')
def display_create_menko():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('create_new_menko.html')


@app.route('/menko/create', methods=['POST'])
def create_menko():
    if not request.files["img_front"]:
        flash("Image is required", "error_menko_img_front")
        return redirect('/menko/new')
    else:
        front_image = Menko.get_pic_url(request.files["img_front"])
    print(front_image)

    if not request.files["img_back"]:
        flash("Image is required", "error_menko_img_back")
        return redirect('/menko/new')
    else:
        back_image = Menko.get_pic_url(request.files["img_back"])
    print(back_image)
    
    if Menko.validate_menko(request.form) == False:
        return redirect('/menko/new')

    data = {
        **request.form,
        "user_id": session['user_id'],
        "img_front": front_image['data']['url'],
        "img_back": back_image['data']['url'],
    }
    Menko.create(data)

    return redirect('/menko')


@app.route('/menko/edit/<int:id>')
def display_edit_menko(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": id
    }

    current_menko = Menko.get_one_with_user(data)

    return render_template('edit_menko.html', current_menko=current_menko)


@app.route('/menko/update/<int:id>', methods=['POST'])
def update_menko(id):
    if Menko.validate_menko(request.form) == False:
        return redirect(f'/menko/edit/{id}')
    print(request.form)

    menko_data = {
        **request.form,
        "id": id,
    }

    Menko.update_one(menko_data)
    return redirect('/menko')


@app.route('/menko/<int:id>')
def display_one_menko(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": id
    }

    current_menko = Menko.get_one_with_user(data)
    return render_template('display_menko.html', current_menko=current_menko)


@app.route('/menko/<int:id>/delete')
def delete_menko(id):

    data = {
        'id': id
    }

    Menko.delete_one_menko(data)
    return redirect('/menko')


@app.route('/menko/update/front/<int:id>', methods=['POST'])
def update_menko_photo_front(id):

    if not request.files["img_front"]:
        flash("Image is required", "error_menko_img_front")
        return redirect(f'/menko/edit/{id}')
    else:
        front_image = Menko.get_pic_url(request.files["img_front"])

    menko_data = {
        'id': id,
        "img_front": front_image['data']['url'],
    }

    Menko.update_one_photo_front(menko_data)
    return redirect('/menko')


@app.route('/menko/update/back/<int:id>', methods=['POST'])
def update_menko_photo_back(id):
    
    if not request.files["img_back"]:
        flash("Image is required", "error_menko_img_back")
        return redirect(f'/menko/edit/{id}')
    else:
        back_image = Menko.get_pic_url(request.files["img_back"])

    menko_data = {
        'id': id,
        "img_back": back_image['data']['url'],
    }

    Menko.update_one_photo_back(menko_data)
    return redirect('/menko')
