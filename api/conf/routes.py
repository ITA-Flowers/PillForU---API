from flask_restful import Api

from api.handlers import userHandlers as userH
from api.handlers import deviceHandler as devH
from api.handlers import dosageHandler as dosH


def generate_routes(app):
    # Create API
    api = Api(app)

    # Setting up the endpoints
    # -- User Handler
    api.add_resource(userH.Login, '/login')

    api.add_resource(userH.Register, '/register')

    api.add_resource(userH.UsersManager, '/users')
    
    # -- Device Handler
    api.add_resource(devH.DeviceManager, '/devices')
    
    # -- Dosage Handler
    api.add_resource(dosH.DosageManager, '/dosages')
    