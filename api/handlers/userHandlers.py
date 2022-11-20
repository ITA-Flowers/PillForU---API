from flask import request, Response
from flask_restful import Resource
import re
import json

import api.database.db as db
import api.codes.errors as errors
import api.codes.successes as successes
import api.models.user as mduser


# @app.route('/login')
class Login(Resource):    
    @staticmethod
    def post():
        resp = Response()
        
        try:
            # Get user credentials
            login = request.json.get('login').strip()
            password = request.json.get('password').strip()
        except Exception as why:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        # Check if any param is none
        if login is None or password is None:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        # Get user if it is existed
        user = db.get_user_by_login(login)

        # Check if user is not existed
        if user is None:
            resp = Response(json.dumps(errors.UNAUTHORIZED[0]), status=errors.UNAUTHORIZED[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        hashed_password = user['password']
    
        # Check if password is valid
        if not mduser.User.check_passwd(password=password, hashed_password=hashed_password):
            resp = Response(json.dumps(errors.UNAUTHORIZED[0]), status=errors.UNAUTHORIZED[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        resp = Response(json.dumps(successes.GOOD_CREDENTIALS[0]), status=successes.GOOD_CREDENTIALS[1])
        resp.headers.set('Access-Control-Allow-Origin', '*')
        resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return resp


# @app.route('/register')
class Register(Resource):
    @staticmethod
    def _validate_role(role : str) -> bool:
        for _r in mduser.ROLE:
            if role == _r.value:
                return True, _r
            
        return False, None
    
    @staticmethod
    def _validate_phone_number(phone_number : str) -> bool:
        pattern = r"^[0-9]{9}$"
        
        if re.match(pattern, phone_number):
            return True

        return False
        
    
    @staticmethod
    def post():
        try:
            # Get user data
            login, password, role, phone_number = (
                request.json.get('login').strip(),
                request.json.get('password').strip(),
                request.json.get('role').strip(),
                request.json.get('phone_number').strip(),
            )
        except Exception as why:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        
        # Check if any field is none
        if login is None or password is None or role is None or phone_number is None:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        
        # Check if `role` and `phone_number` are valid
        valid_role, role = Register._validate_role(role)
        valid_phone_number = Register._validate_phone_number(phone_number)
        
        if not valid_role or not valid_phone_number:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        
        # Get user if it is existed
        user = db.get_user_by_login(login)

        # Check if user exists
        if user is not None:
            resp = Response(json.dumps(errors.ALREADY_EXIST[0]), status=errors.ALREADY_EXIST[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        
        # Create a new user
        user = mduser.User(login, mduser.User.hash_passwd(password), role, phone_number)

        # Add new user to database
        db.add_user(user)

        resp = Response(json.dumps(successes.REGISTRATION_COMPLETE[0]), successes.REGISTRATION_COMPLETE[1])
        resp.headers.set('Access-Control-Allow-Origin', '*')
        resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return resp


# @app.route('/users')
class UsersManager(Resource):
    @staticmethod
    def get():
        # Check if there is `uuid` param
        try: uuid = request.json.get('uuid').strip()
        except Exception as _: uuid = None

        if not uuid:
            # Check if there is `login` param
            try: login = request.json.get('login').strip()
            except Exception as _: login = None
            
            if not login:
                
                # Get all users
                users = db.get_users()
                resp = Response(json.dumps(users), status=200)
                resp.headers.set('Access-Control-Allow-Origin', '*')
                resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
                resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
                return resp

            # Get user by login
            user = db.get_user_by_login(login)
        
            # If user does not exists
            if user is None:
                resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
                resp.headers.set('Access-Control-Allow-Origin', '*')
                resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
                resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
                return resp
            else:
                resp = Response(json.dumps(user), status=200)
                resp.headers.set('Access-Control-Allow-Origin', '*')
                resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
                resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
                return resp

        # Get user by uuid
        user = db.get_user_by_uuid(uuid)
        
        # If user does not exists
        if user is None:
            resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        else:
            return user
        
    @staticmethod
    def put():
        try:
            # Get user data
            login, password, role, phone_number = (
                request.json.get('login').strip(),
                request.json.get('password').strip(),
                request.json.get('role').strip(),
                request.json.get('phone_number').strip(),
            )
        except Exception as why:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        
        # Check if any field is none
        if login is None or password is None or role is None or phone_number is None:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        
        # Check if `role` and `phone_number` are valid
        valid_role, role = Register._validate_role(role)
        valid_phone_number = Register._validate_phone_number(phone_number)
        
        if not valid_role or not valid_phone_number:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        # Create a new user instance
        user = mduser.User(login, mduser.User.hash_passwd(password), role, phone_number)

        # Update user data
        if db.update_user(user):
            resp = Response(json.dumps(successes.RESOURCE_UPDATED[0]), status=successes.RESOURCE_UPDATED[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        
        resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
        resp.headers.set('Access-Control-Allow-Origin', '*')
        resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return resp
    
    @staticmethod
    def delete():
        try:
            # Get user credentials
            login = request.json.get('login').strip()
        except Exception as why:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        # Check if any param is none
        if login is None:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        # Get user if it is existed
        user = db.get_user_by_login(login)

        # Check if user is not existed
        if user is None:
            resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        uuid = user['uuid']
        
        db.delete_user(uuid)
        
        resp = Response(json.dumps(successes.RESOURCE_DELETED[0]), status=successes.RESOURCE_DELETED[1])
        resp.headers.set('Access-Control-Allow-Origin', '*')
        resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return resp