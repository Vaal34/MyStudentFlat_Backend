from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_login import LoginManager, login_required, current_user
from random import randint


login_manager = LoginManager()

app = Flask(__name__)

login_manager.init_app(app)

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "login"
app.config["SECRET_KEY"] = "a1dd1f01bfde77c6aa8a92c099639cc0fe03b1f89ac3bcbd1a8f38da35b2f3ad"
Base = declarative_base()

engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/login') # Connect to MystudentFlat
sessfactory = sessionmaker(bind=engine) # Create factory session to connect the DB
session = scoped_session(sessfactory) # Creating a "scoped" session that will automatically manage connections based on the context of use

# this class is for creating tables in db
class User(Base):
    __tablename__ = 'user'


    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    password = Column(String(80))

inspector = inspect(engine)
if not inspector.has_table('user'):
    Base.metadata.create_all(engine)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

@app.route("/login",methods=["GET", "POST"]) # permet de se connecter
def login():
    d = {}
    if request.method == "POST":
        mail = request.form["mail"]
        password = request.form["password"]
        
        login = session.query(User).filter_by(email=mail, password=password).first()
        if login is not None:
            # account found
            d["status"] = 34
            return jsonify(d)
        else:
            # account not exist
            d["status"] = 31
            d["message"] = "Nom d'utilisateur ou mot de passe incorrect"
            return jsonify(d)
            


@app.route("/register", methods=["GET", "POST"]) # permet de creer un compte
def register():
    d = {}
    if request.method == "POST":
        mail = request.form['mail']
        passw = request.form['password']
        confirm_passw = request.form['confirm_password']
        username = session.query(User).filter_by(email=mail).first()

        if confirm_passw != passw:
            d["status"] = 31
            d["message"] = "Les mots de passe ne correspondent pas"
            return jsonify(d)

        if username is None:
            register = User(email = mail, password = passw)
            session.add(register)
            session.commit()
            d["status"] = 34
            return jsonify(d)
        else:
            # already exist
            d["status"] = 31
            return jsonify(d)
        
@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    d = {}
    if request.method == "POST":
        mail = request.form["mail"]
        password = request.form["password"]
        
        login = session.query(User).filter_by(email=mail, password=password).first()
        if login is not None:
            # Account found, delete the account
            session.delete(login)
            session.commit()
            d["status"] = 34
            d["message"] = "Le compte a ete supprime avec succes"
            return jsonify(d)
        else:
            # Incorrect username or password
            d["status"] = 31
            d["message"] = "Nom d'utilisateur ou mot de passe incorrect"
            return jsonify(d)
        
if __name__ == "__main__":
    app.run()