from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import psycopg2
from config import load_config
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
load_dotenv()

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')  # Change this to a random secret in production
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Mock user database
users = []

# Function to connect to the PostgreSQL database server
def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

config  = load_config()

#     try:
#         with psycopg2.connect(**config) as conn:
#             with conn.cursor() as cur:
#                 # Executing the selected query
#                 cur.execute(query_list[query_number-1])
#                 rows = cur.fetchall()
#                 # Printing the results using query_output function
#                 query_output(rows, query_number)

#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/signup_student', methods=['POST'])
def signup_student():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    email = data['email']
    sid = "24DB" + bcrypt.generate_password_hash(email).decode('utf-8')[:16]
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"SELECT * FROM STUDENT WHERE email='{email}';")
                rows = cur.fetchall()
                if(rows):
                    return jsonify({'message': 'User already exists'}), 404
                else:
                    cur.execute(f"INSERT INTO STUDENT VALUES ('{sid}', '{email}', '{data['name']}', '{data['roll_number']}', '{data['phone']}', '{data['college']}', '{data['department']}', {(int)(data['year'])}, '{data['type']}', '{hashed_password}');")
                    return jsonify({'message': 'User successfully registered'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'User created successfully'}), 404
    
@app.route('/signup_organiser', methods=['POST'])
def signup_organiser():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    email = data['email']
    oid = "24OR" + bcrypt.generate_password_hash(email).decode('utf-8')[:16]
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"SELECT * FROM ORGANISERS WHERE email='{email}';")
                rows = cur.fetchall()
                if(rows):
                    return jsonify({'message': 'Organiser already exists'}), 404
                else:
                    cur.execute(f"INSERT INTO ORGANISERS VALUES ('{oid}', '{email}', '{data['name']}', '{data['phone']}', '{hashed_password}');")
                    return jsonify({'message': 'Organiser successfully registered'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Organiser created successfully'}), 404

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = next((user for user in users if user['username'] == data['username']), None)
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        access_token = create_access_token(identity=data['username'])
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({'message': 'Protected content!'}), 200

if __name__ == '__main__':
    app.run(debug=True)