from flask import Flask,request,jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from random import randint
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from uuid import uuid4
import sqlalchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash



login_manager = LoginManager()
app = Flask(__name__)

login_manager.init_app(app)
mysql = MySQL(app)
cors = CORS(app)


app.config['CORS_HEADERS'] = 'Content-Type'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "login"
app.secret_key = "a1dd1f01bfde77c6aa8a92c099639cc0fe03b1f89ac3bcbd1a8f38da35b2f3ad"
Base = declarative_base()

engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/login') # Connect to MystudentFlat
sessfactory = sessionmaker(bind=engine) # Create factory session to connect the DB
session = scoped_session(sessfactory) # Creating a "scoped" session that will automatically manage connections based on the context of use

# this class is for creating tables in db
class User(Base):
    __tablename__ = 'user'

    id = Column(String(36), default=lambda: str(uuid4()), primary_key=True) # create a lambda function for execute the uuid function
    email = Column(String(120), unique=True, nullable=True)
    password = Column(String(250), nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password) # encrypt the password, self is like new_user.set_password where self is new_user

    def check_password(self, password):
        return check_password_hash(self.password, password)

inspector = inspect(engine)
if not inspector.has_table('user'):
    Base.metadata.create_all(engine)

@app.route("/login", methods=["POST"])
def login():
    d = {}
    mail = request.form["mail"]
    password = request.form["password"]

    if not mail or not password:
        abort(412, description="Veuillez remplir tous les champs.")  # Check if fields are empty

    user = session.query(User).filter_by(email=mail).first()  # Retrieve the user matching the email

    if user is not None and user.check_password(password):  # Check if the user exists and the password is correct
        d["status"] = 34  # Success status
        return jsonify(d)
    else:
        abort(411, description="Nom d'utilisateur ou mot de passe incorrect.")  # Authentication error



@app.route("/register", methods=["GET", "POST"])
def register():
    d = {}
    if request.method == "POST":
        mail = request.form['mail']
        passw = request.form['password']
        confirm_passw = request.form['confirm_password']
        user = session.query(User).filter_by(email=mail).first()  # Check if user already exists with the same email

        if confirm_passw != passw:
            abort(405, description="La création du compte a échoué. Les mots de passe ne correspondent pas.")  # Password mismatch error

        if user is None:
            new_user = User(email=mail)  # Create a new user with the provided email
            new_user.set_password(passw)  # Set the hashed password for the new user
            session.add(new_user)  # Add the new user to the SQLAlchemy session
            session.commit()  # Save the new user to the database
            d["status"] = 34  # Success status
            return jsonify(d)
        else:
            abort(406, description="La création du compte a échoué. L'utilisateur existe déjà.")  # Account already Exixst



@app.route("/delete_account", methods=["POST"])
def delete_account():
    d = {}
    if request.method == "POST":
        mail = request.form["mail"]
        password = request.form["password"]
        
        user = session.query(User).filter_by(email=mail).first()
        if user is not None and user.check_password(password):
            # Account found, delete the account
            session.delete(user)
            session.commit()
            d["status"] = 34
            d["message"] = "Le compte a ete supprime avec succes"
            return jsonify(d)
        else:
            abort(411, description="Nom d'utilisateur ou mot de passe incorrect.")
        

@app.route("/all_account", methods=['GET'])
def get_allAccount():

    users = session.query(User).all()
    account_list = []
    for user in users:
        account = {
            "id": user.id,
            "password": user.password,
            "email": user.email,
        }
        account_list.append(account)
    return jsonify(account_list)

if __name__ == "__main__":
    app.run()


"""
@app.route("/logout", methods=["POST"])
def logout():
    d = {}
    user = session.query(User).filter_by(id=User.get_id(user), authentificated=True)
    if user:
        user.authentificated = False
        session.add(user)
        session.commit()
        d["status"] = 34
        return jsonify({"message": "Déconnexion réussie", d: d["status"]})
    else:
        abort(412, description="L'utilsateur n'est pas connecter.")  # Authentication error
"""