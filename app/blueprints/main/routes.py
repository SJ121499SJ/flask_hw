from flask import Flask, render_template, request, flash, redirect, url_for
import requests
from ..auth.forms import PokemonForm, ConfirmCatchForm, TeamForm, DeleteFromTeamForm
from app.models import PokemonCaught, team, User

from app.blueprints.main import main
from flask_login import login_required

#Route Section
@main.route('/')
def greetings():
    return render_template('greetings.html')

@main.route('/home', methods={'GET', 'POST'})
@login_required
def home():
    users = User.query.all()
    return render_template('home.html', users=users)


@main.route('/base')
def base():
    return render_template('base.html')

@main.route('/pokemon', methods = ['GET' , 'POST'])
@login_required
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_name = form.pokemon_name.data.lower()
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



@main.route('/pokemon_caught', methods=['GET','POST'])
@login_required
def pokemon_caught():
    pokemon_caught = PokemonCaught.query.all()
    return render_template('pokemon_caught.html', pokemon_caught=pokemon_caught)


@main.route('/confirm_catch', methods=['GET','POST'])
@login_required
def confirm_catch():
    form = ConfirmCatchForm()
    if request.method == 'POST' and form.validate_on_submit() and PokemonCaught.query.count() <= 5:
        pokemon_name = form.pokemon_name.data.lower()
        new_pokemon_data = {
        'pokemon_name': form.pokemon_name.data.title(),
        }
        new_pokemon = PokemonCaught()
        new_pokemon.from_dict(new_pokemon_data)
        new_pokemon.save_to_db()
        flash(f'You have successfully caught {new_pokemon.pokemon_name}','success')
        return redirect('pokemon')
    elif PokemonCaught.query.count() >= 5:
        flash('You can only catch up to 5 Pokemons', 'danger')
        return redirect('team')
    return render_template('confirm_catch.html', form=form)


@main.route('/team', methods=['GET','POST'])
@login_required
def team():
    form = TeamForm()
    pokemon_caught = PokemonCaught.query.all()
    pokemon_info = {}
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_name = form.pokemon_name.data
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
        return render_template('team.html', pokemon_info=pokemon_info, form=form)
    return render_template('team.html', pokemon_info=pokemon_info, form=form, pokemon_caught=pokemon_caught)


@main.route('/add_to_team/<int:pokemon_id>')
@login_required
def add_to_team(pokemon_id):
    pokemon = PokemonCaught.query.get(pokemon_id)
    if pokemon:
        pokemon.add_to_team(pokemon)
        flash('Added to team!', 'success')
    return render_template('team.html')


@main.route('/delete_from_team')
@login_required
def delete_from_team():
    form = DeleteFromTeamForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_name = form.pokemon_name.data.lower()
        new_pokemon_data = {
        'pokemon_name': form.pokemon_name.data.title(),
        }
        new_pokemon = PokemonCaught()
        new_pokemon.from_dict(new_pokemon_data)
        new_pokemon.delete_from_db()
        flash(f'You have successfully removed {new_pokemon.pokemon_name}','success')
        return redirect('pokemon')
    return render_template('delete_from_team.html', form=form)

@main.route('/battle')
@login_required
def battle():

    return render_template('battle.html')
