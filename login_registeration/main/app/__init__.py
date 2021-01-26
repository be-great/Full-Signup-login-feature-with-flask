#import sys
#sys.path.insert(0,'/home/miss/hospital/parted_things/login_registeration/main')
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.enviroment.config import Config
from flask_login import LoginManager
from flask_mail import Mail
app1 = Flask(__name__,template_folder="../template/",static_folder="../static/")
app1.config.from_object(Config())
db = SQLAlchemy(app1)
mail =Mail(app1)
db.create_all() # create all table
############# flask_login#########################
login_manager = LoginManager()
login_manager.login_view='auth.login'
login_manager.init_app(app1)
from app.models import User
@login_manager.user_loader
def load_user(user_id):## user id from the cookie
    return User.query.get(int(user_id)) ## return User object

##########################Blueprint#########################
from app.view.viewfunction import user_bp
from app.view.auth import auth
from app.errors import error
app1.register_blueprint(user_bp)
app1.register_blueprint(auth)
app1.register_blueprint(error)
