from flask import Flask, request, jsonify
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt_header
import psycopg2
from flask_cors import CORS
from dotenv import load_dotenv
import os
from routers.auth import auth
from routers.accomodation import accomodation
from routers.events.event import events
from routers.events.register import events_register
from routers.admin.event import admin_event
from routers.admin.student import admin_student
from routers.admin.organiser import admin_organiser
from routers.admin.notif import admin_notif
from routers.organiser.winner import winner_settings
from routers.organiser.event import organiser_event
from routers.organiser.resource import resource
from routers.organiser.profile import profiles

app = Flask(__name__)
CORS(app)
load_dotenv()

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

app.register_blueprint(accomodation)
app.register_blueprint(auth)
app.register_blueprint(events, url_prefix='/event')
app.register_blueprint(events_register, url_prefix='/event')
app.register_blueprint(admin_event, url_prefix='/admin')
app.register_blueprint(admin_student, url_prefix='/admin')
app.register_blueprint(admin_organiser, url_prefix='/admin')
app.register_blueprint(admin_notif, url_prefix='/admin')
app.register_blueprint(winner_settings, url_prefix='/organiser')
app.register_blueprint(organiser_event, url_prefix='/organiser')
app.register_blueprint(resource, url_prefix='/organiser')
app.register_blueprint(profiles, url_prefix='/organiser')


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)