from flask import Blueprint,render_template,request ,url_for ,redirect
from app.security import secureKeys
from app.services import registerationOP,loginOP
from flask_login import login_required , current_user


user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/", methods=["GET"])
def home():
    return render_template('index.html')




@user_bp.route("/reg", methods=["GET"])
@login_required
def reg():
    return render_template('reg.html')
