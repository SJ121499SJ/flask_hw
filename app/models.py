from app import db, login
from flask_login import UserMixin #only use on your user class
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


team = db.Table(
    'team',
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon_caught.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    team = db.relationship('PokemonCaught', secondary = team, backref='owner', lazy='dynamic')
 
    
    #hashes our password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    #check password hash
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    # use this method to register our user attributes
    def from_dict(self,data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
    
    # Save to our databse
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class PokemonCaught(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String, nullable="False")
    team = db.relationship('User', secondary = team, backref='pokemon', lazy='dynamic')
    
    # use this method to register our user attributes
    def from_dict(self,data):
        self.pokemon_name = data['pokemon_name']
    
    # Save to our databse
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    #Delete from database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def add_to_team(self, pokemon_id):
        self.team.append(pokemon_id)
        db.session.commit()
    
    def remove_from_team(self, pokemon_id):
        self.team.remove(pokemon_id)
        db.session.commit()



