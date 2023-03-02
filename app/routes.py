from flask import Flask, render_template, request
import requests
from app.forms import PokemonForm, RegistrationForm, LoginForm
from app import app

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



@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm() 
    if request.method == 'POST' and form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        password = form.password.data
        app.config.get('REGISTERED_USERS')[email] = {'Full Name':full_name, 'password':password}
        print(app.config.get('REGISTERED_USERS'))
    return render_template('registration.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in app.config.get('REGISTERED_USERS') and password == app.config.get('REGISTERED_USERS').get(email).get('password'):
            return f"Login Successful! Welcome {app.config.get('REGISTERED_USERS').get(email).get('Full Name').upper()}"
        else:
            error = 'Incorrect Email/Password'
            return render_template('login.html', error=error, form=form)
    return render_template('login.html', form=form)
    return render_template('login.html', form=form)
