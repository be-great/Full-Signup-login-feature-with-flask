 #####################        using sha256      ##########################3
import os
from hashlib import sha256
class Sha256_:
    def encrypt_Sha256_(self,hash_string):
        sha_signature = sha256(hash_string.encode()).hexdigest()
        return sha_signature
    def decrypt_Sha256_Check_User(self,The_string,The_hash):
        The_string_hash= self.encrypt_Sha256_(The_string)
        if The_string_hash != The_hash:
            return -1
        else:
            return 1
class secureKeys:
    def registeration():
        return os.environ['registerationSecureKey']
    def login():
        return os.environ['loginSecureKey']



hash_sha256 =  Sha256_()
