from flask import Flask, request, jsonify
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt_header
import psycopg2
from config import load_config
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
load_dotenv()

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')                     # Change this to a random secret in production
jwt = JWTManager(app)
salt = os.environ.get('SALT')
cost_factor = os.environ.get('COST_FACTOR')

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

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/signup_student', methods=['POST'])
def signup_student():
    data = request.get_json()
    # hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    email = data['email']
    # sid = "24DB" + bcrypt.generate_password_hash(email).decode('utf-8')[:16]
    sid = "24DB" + bcrypt.hashpw(email.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')[:16]
    print(f"Password: {data['password']}, Hashed Password: {hashed_password}")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"SELECT * FROM STUDENT WHERE email='{email}';")
                rows = cur.fetchall()
                if(rows):
                    return jsonify({'message': 'User already exists'}), 404
                else:
                    cur.execute(f"SELECT * FROM ORGANISERS WHERE email='{email}';")
                    rows = cur.fetchall()
                    if(rows):
                        return jsonify({'message': 'Organiser already exists'}), 404
                    else:
                        cur.execute(f"INSERT INTO STUDENT VALUES ('{sid}', '{email}', '{data['name']}', '{data['roll_number']}', '{data['phone']}', '{data['college']}', '{data['department']}', {(int)(data['year'])}, '{data['type']}', '{hashed_password}');")
                        return jsonify({'message': 'User successfully registered'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Creating user'}), 404
    
@app.route('/signup_organiser', methods=['POST'])
def signup_organiser():
    data = request.get_json()
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    email = data['email']
    oid = "24OR" + bcrypt.hashpw(email.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')[:16]

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"SELECT * FROM ORGANISERS WHERE email='{email}';")
                rows = cur.fetchall()
                if(rows):
                    return jsonify({'message': 'Organiser already exists'}), 404
                else:
                    cur.execute(f"SELECT * FROM STUDENT WHERE email='{email}';")
                    rows = cur.fetchall()
                    if(rows):
                        return jsonify({'message': 'User already exists'}), 404
                    else:
                        cur.execute(f"INSERT INTO ORGANISERS VALUES ('{oid}', '{email}', '{data['name']}', '{data['phone']}', '{hashed_password}');")
                        return jsonify({'message': 'Organiser successfully registered'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Creating user'}), 404

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    # print(email, password)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"SELECT * FROM STUDENT WHERE email='{email}';")
                rows = cur.fetchall()
                if rows:
                    hashed_password = rows[0][9]
                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                        profile_info = {
                            'sid': rows[0][0],
                            'email': rows[0][1],
                            'name': rows[0][2],
                            'phone': rows[0][3],
                            'roll_number': rows[0][4],
                            'college': rows[0][5],
                            'department': rows[0][6],
                            'year': rows[0][7],
                            'type': rows[0][8]
                        }
                        access_token = create_access_token(identity=email, additional_headers=profile_info)
                        return jsonify({'access_token': access_token}), 200
                    else:
                        return jsonify({'message': 'Invalid credentials'}), 404
                else:
                    cur.execute(f"SELECT * FROM ORGANISERS WHERE email='{email}';")
                    rows = cur.fetchall()
                    if rows:
                        hashed_password = rows[0][4]
                        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                            profile_info = {
                                'oid': rows[0][0],
                                'email': rows[0][1],
                                'name': rows[0][2],
                                'phone': rows[0][3]
                            }
                            access_token = create_access_token(identity=email, additional_headers=profile_info)
                            return jsonify({'access_token': access_token}), 200
                        else:
                            return jsonify({'message': 'Invalid credentials'}), 404
                    else:
                        return jsonify({'message': 'User does not exist'}), 404
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'User does not exist'}), 404

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    profile_info = get_jwt_header()
    print(profile_info)
    return profile_info

if __name__ == '__main__':
    app.run(debug=True)