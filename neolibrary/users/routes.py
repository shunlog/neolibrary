import os
import secrets
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask import current_app as app
from flask_login import login_user, current_user, logout_user, login_required
from neolibrary import graph, bcrypt, profile_pics
from neolibrary.models import User
from neolibrary.users.utils import crop_n_resize, save_profile_pic, delete_profile_pic
from neolibrary.users.forms import RegistrationForm, LoginForm, UpdateAccountForm

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
                                .decode('utf-8')
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.password = hashed_password
        graph.push(user)
        flash(f'Account created successfully. You can now log in as {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.match(graph).where(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data, force=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html', title='Account',
                           image_folder=profile_pics)

@users.route("/account/edit", methods=['GET', 'POST'])
@login_required
def edit_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            if current_user.image_file != "default.png":
                delete_profile_pic(current_user.image_file)
                picture_file = save_profile_pic(form.picture.data)
                current_user.image_file = picture_file
                current_user.username = form.username.data
                current_user.email = form.email.data
                graph.push(current_user)
                flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_account.html', title='Account',
                           image_folder=profile_pics, form=form)


@users.route("/list_users", methods=['GET','POST'])
def list_users():
    users = User().match(graph)
    if request.method == 'POST':
        user_ls = request.form.getlist('user')
        count = 0
        for username in user_ls:
            username = username[2:-1]
            count += 1
            u_obj = User().match(graph, username).first()
            if u_obj.image_file and u_obj.image_file != "default.png":
                delete_profile_pic(u_obj.image_file)
                graph.delete(u_obj)
                flash(str(count)+' users have been deleted!', 'success')
        return redirect(url_for('users.list_users'))

    return render_template('list_users.html', users=users, image_folder=profile_pics)
