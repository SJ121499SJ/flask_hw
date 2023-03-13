from flask import Flask, render_template, request, flash, redirect, url_for
import requests
from app.blueprints.auth.forms import PokemonForm, RegistrationForm, LoginForm, RegistrationForm,EditProfileForm
from app.blueprints.auth import auth
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user, login_required

#Route Section
@auth.route('/register', methods=['GET','POST'])
def register():
     form =  RegistrationForm()
     if request.method == 'POST' and form.validate_on_submit():
         new_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email':form.email.data.lower(),
            'password': form.password.data
         }

         new_user = User()
         new_user.from_dict(new_user_data)
         new_user.save_to_db()
         flash('You have successfully registered','success')
         return redirect('login')
     return render_template('register.html', form=form)




@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Succesfully Logged In! Welcome Back, {queried_user.first_name}!', 'success')
            return redirect(url_for('main.home'))
        else:
            error = 'Invalid email or password'
            flash(f'{error}', 'danger')
    return render_template('login.html', form=form)


@auth.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
         new_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email':form.email.data.lower(),
            'password': form.password.data
         }
         queried_user = User.query.filter_by(email=new_user_data['email']).first()
         if queried_user:
             flash('Email already exists', 'danger')
             return redirect(url_for('auth.edit_profile'))
         else:
             current_user.from_dict(new_user_data)
             current_user.save_to_db()
             flash('Profile has been updated', 'success')
             return redirect(url_for('main.home'))

    return render_template('edit_profile.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out!','warning')
        return redirect(url_for('auth.login'))

