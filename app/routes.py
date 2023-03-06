from flask import Flask, render_template, request, flash, redirect, url_for
import requests
from app.forms import PokemonForm, RegistrationForm, LoginForm, RegistrationForm
from app import app
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user

#Route Section
@app.route('/')
def greetings():
    return render_template('greetings.html')

@app.route('/home', methods =['GET'])
def home():
    return render_template('home.html')


@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/pokemon', methods = ['GET' , 'POST'])
def pokemon():
    form = PokemonForm()
    print(request.method)
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_name = form.pokemon_name.data
        print(pokemon_name)
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        if response.ok:
            pokemon_info = {
                'Name': response.json()['species']['name'].title(),
                'Ability': response.json()['abilities'][0]['ability']['name'],
                'Base_experience': response.json()['base_experience'],
                'Url_for_front_shiny': response.json()['sprites']['front_shiny'],
                'Attack_base_state': response.json()['stats'][1]['base_stat'],
                'hp_base_state': response.json()['stats'][0]['base_stat'],
                'Defense_base_state': response.json()['stats'][2]['base_stat']
                }
            print(pokemon_info)
            return render_template('pokemon.html', pokemon_info=pokemon_info, form=form)
        else:
            error = "Please enter a different name or check the spelling"
            return render_template('pokemon.html', error=error, form=form)
        
    return render_template('pokemon.html', form=form)



@app.route('/register', methods=['GET','POST'])
def register():
     form = form = RegistrationForm()
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
         return redirect(url_for('login'))
     return render_template('register.html', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Succesfully Logged In! Welcome Back, {queried_user.first_name}!', 'success')
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password'
            flash(f'{error}', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if current_user:
        logout_user()
        flash('You have logged out!','warning')
        return redirect(url_for('login'))

