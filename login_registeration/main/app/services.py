#### using DB operation so logic checks ####
############################################
from flask import url_for
from app.models import User ,Temporary_User
from app.security import hash_sha256 ,secureKeys
from app import db , mail
from app.daos import Check_Get_querys
from flask_mail import Message
from app import app1

class UserServiceregister(Check_Get_querys):
    def __init__(self,db,model):
        Check_Get_querys.__init__(self,model)
        self.db = db

    # from Temporary user
    def registerObject(self,temporary_user):
        username_=temporary_user.username
        email_=temporary_user.email
        password_=temporary_user.password
        new_user=self.model(username=username_,email=email_,password=password_)
        self.db.session.add(new_user)
        self.db.session.delete(temporary_user)
        self.db.session.commit()
    def registerRequest(self,request):
        username_=request.form["username"]
        email_=request.form["email"]
        password_=request.form["password"]
        hash_password_ =hash_sha256.encrypt_Sha256_(password_)
        new_user=self.model(username=username_,email=email_,password=hash_password_)
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user

    ## this for soome one singup again without verify
    def Tempo_checks(self,request):
        classChecks=Check_Get_querys(self.model)
         ## check username and email
        check=classChecks.checkUserName(request.form['username'])
        check1=classChecks.checkEmailName(request.form['email'])
        if check1==1 or check==1:
            # have same email
            if check1==1:
                updateUser=self.model.query.filter_by(email=request.form['email']).first()

            # have same username
            else:
                updateUser=self.model.query.filter_by(username=request.form['username']).first()

            updateUser.username=request.form['username']
            updateUser.email=request.form['email']
            updateUser.password=request.form['password']
            self.db.session.commit()
            return updateUser
        else:
            return self.registerRequest(request)


        ## if some thing

    #########  check password => username => email => go registeration #####
    def registerationCheck(self,request):
         classChecks=Check_Get_querys(self.model)
        ## check password
         check=classChecks.checkPassMatch(request.form["password"],request.form["repassword"])
         if check ==-1:
             return "password Not Match"
         else: ## check username
             check=classChecks.checkUserName(request.form['username'])
             if check ==1:
                 return "Username is Not available"
             else: ## check email
                 check=classChecks.checkEmailName(request.form['email'])
                 if check ==1:
                     return "Email is Not available"
                 else:
                     ## append the user registeration

                     return secureKeys.registeration()

class UserServicelogin(Check_Get_querys):
    def __init__(self,model):
        self.model = model
    def login_check(self,email,password):
        ## check email
        user=Check_Get_querys(self.model).checkEmailNameAndObject(email)
        if user ==None:
            return "Email is't found" ,None
        else: ## check password
            check=hash_sha256.decrypt_Sha256_Check_User(password, Check_Get_querys(self.model).getEmailPass(email))
            if check ==-1:
                return "Password is Wrong" , None
            else:
                return secureKeys.login() , user
class EmailVerify:

    def __init__(self,user):
        self.user=user

    def send_email_verify(self):
        url= 'auth.verify_signin'
        message ="Verfiy email"
        return self.send_model(url,message)
    def send_reset_email(self):
        url= 'auth.reset_token'
        message ="Reset Your Password"
        self.send_model(url,message)


    def send_model(self,url,message):
        token = self.user.get_reset_token()
        msg = Message(sender=app1.config["MAIL_USERNAME"],recipients=[self.user.email],subject=message)  # message to send
        msg.body=f'''To {message} visit the following link:\n{url_for(url,token=token,_external=True)}\nif you did not make this request then simply ignore this email no change will made'''
        check=True
        try :
            mail.send(msg)
        except:
            check=False
        return check

registerationOP = UserServiceregister(db,User)
loginOP = UserServicelogin(User)
Temp_registerationOP=UserServiceregister(db,Temporary_User)
