from flask import Blueprint,render_template ,request ,redirect , url_for , session
from app.services import registerationOP,loginOP ,Temp_registerationOP ,EmailVerify
from app.security import secureKeys ,hash_sha256
from app.models import User , Temporary_User
from app.daos import Checks
from app import db
from flask_login import login_user ,logout_user ,current_user
from flask_mail import Message

auth = Blueprint('auth', __name__)

###########################################################################
@auth.route("/login", methods=["GET","POST"])
def login():
    error=""
    if request.method =="POST":
        answer=loginOP.login_check(request.form['email'],request.form['password'])
        if answer[0] == secureKeys.login():

            login_user(answer[1])
            session.permanent = True
            return redirect(url_for('user_bp.reg'))
        error=error+answer[0]
    return render_template('login.html',error=error)

@auth.route("/reset_password", methods=["GET","POST"])
def reset_request():
    ##### if user is login go to home it need to logout first ####
    if current_user.is_authenticated:
            return redirect(url_for('user_bp.home'))
    # check vaild email
    error =''
    if request.method =="POST":
        user= Checks.checkEmailNameAndObject(request.form.get('email'))
        if user is None :
            error =error +"Email doesn't Existes"
        else:
            ## send email
            EmailVerify(user).send_reset_email()
            error =error +"Check your Email"
    return render_template('Checks_login/Emailcheck.html',error=error)

@auth.route("/reset_password/<token>", methods=["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('user_bp.home'))
    user=User.verify_reset_token(token)
    if user is None:
        return redirect(url_for('auth.reset_request',error="That is an invalid or expired request"))
    error=''
    if request.method =="POST":
        if request.form.get('password') != request.form.get('repassword'):
            error=error+"Password Not Match"
        else:
            hashed_password = hash_sha256.encrypt_Sha256_(request.form.get('password'))
            user.password = hashed_password
            db.session.commit()
            return redirect(url_for('auth.login'))

    return render_template('Checks_login/reset_password.html', error=error)

#############################################################################

@auth.route("/signup", methods=["GET","POST"])
def signup():
    error=""
    if request.method =="POST":

        v=registerationOP.registerationCheck(request)
        error=error+v
    if error ==secureKeys.registeration():
        user=Temp_registerationOP.Tempo_checks(request)
        check=EmailVerify(user).send_email_verify()
        if check:
            return render_template('Checks_login/verifyEmail.html')
        else:
            return render_template('errors/500.html',error="there is porblem with email server")
    return render_template('signup.html',error=error)

## reset
@auth.route("/verify/<token>", methods=["GET"])
def verify_signin(token):
    ## register to real DB and delete from temporary_user
    temporary_user=Temporary_User.verify_reset_token(token)

    if temporary_user is None:
        return redirect(url_for('auth.signup',error="That is an invalid or expired request"))

    registerationOP.registerObject(temporary_user)
    return redirect(url_for('auth.login'))
###########################################################################
@auth.route("/logout", methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for('user_bp.home'))
