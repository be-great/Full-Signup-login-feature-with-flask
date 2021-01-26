
####### DB  operation ########
from app.models import User

class Check_Get_querys:
    def __init__(self,modelUser):
        self.model =modelUser

    def checkUserName(self,username):
        # check DB for username
        check = self.model.query.filter_by(username=username).first()
        if check is None:
            ## we don't have username with that
            return -1
        else:
            return 1
    def checkEmailName(self,email):
        # check DB for username
        check = self.model.query.filter_by(email=email).first()
        if check is None:
            ## we don't have email with that
            return -1
        else:
            return 1
    def getEmailPass(self,email):
        return self.model.query.filter_by(email=email).first().password

    def checkEmailNameAndObject(self,email):
        # check DB for username
        user = self.model.query.filter_by(email=email).first()
        return user

    @staticmethod
    def checkPassMatch(password,repassword):
        if password == repassword :
            return 1
        else:
            return -1


Checks =Check_Get_querys(User)
