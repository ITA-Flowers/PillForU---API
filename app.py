from flask import Flask

from api.database import db
from api.conf import routes
from api.conf import config as conf

# Creating Flask app
def create_app():
    app = Flask(__name__)    
    
    # DB Config
    app.config['MYSQL_HOST']     = conf.MYSQL_HOST
    app.config['MYSQL_USER']     = conf.MYSQL_USER
    app.config['MYSQL_PASSWORD'] = conf.MYSQL_PASSWORD
    app.config['MYSQL_DB']       = conf.MYSQL_DB
    
    # DB Connect
    db.sql_connect(app)
    
    # Setting up endpoints
    routes.generate_routes(app)
    
    return app


# Driver
if __name__ == '__main__':
    # Create app
    try:
        app = create_app()
    except Exception as why:
        print('Errors occured:')
        print(f'{type(why)} : {why}')
        exit(1)

    # Run app
    app.run(host=conf.HOST, port=conf.PORT, debug=conf.DEBUG_MODE)
