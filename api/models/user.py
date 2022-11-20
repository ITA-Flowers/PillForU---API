import bcrypt as bc
from enum import Enum
from flask import jsonify

from api.conf.config import FORMAT

class ROLE(Enum):
    CARETAKER = 'caretaker'
    PUPIL = 'pupil'

class User:
    def __init__(self, login : str, password : str, role : ROLE, phone_number : str, uuid = None):
        self.uuid = uuid
        self.login = login
        self.password = password
        self.role = role.value
        self.phone_number = phone_number

    def get_json(self, json_obj = True):
        json_data = []
        content = {'uuid': self.uuid, 
                   'login': self.login,
                   'password': self.password,
                   'role': self.role,
                   'phone_number': self.phone_number}
        
        json_data.append(content)

        if json_obj:
            return jsonify(json_data)

        return content

    # Bcrypt hashing
    @staticmethod
    def hash_passwd(password : str) -> str:
        salt = bc.gensalt()
        hash_pw = bc.hashpw(password.encode(FORMAT), salt).decode(FORMAT)
        return hash_pw

    @staticmethod
    def check_passwd(password : str, hashed_password : str) -> bool:
        return bc.checkpw(password.encode(FORMAT), hashed_password.encode(FORMAT))
    
    