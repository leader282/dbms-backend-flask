from flask import Flask, request, jsonify
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt_header
import psycopg2
from config import load_config
from flask_cors import CORS
from dotenv import load_dotenv
import os
from routers.auth import auth
from routers.accomodation import accomodation
from routers.events import events
from routers.admin.event import admin_event

app = Flask(__name__)
CORS(app)
load_dotenv()

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

app.register_blueprint(accomodation)
app.register_blueprint(auth)
app.register_blueprint(events, url_prefix='/event')
app.register_blueprint(admin_event, url_prefix='/admin')


@app.route('/')
def hello():
    return 'Hello, World!'





if __name__ == '__main__':
    app.run(debug=True)