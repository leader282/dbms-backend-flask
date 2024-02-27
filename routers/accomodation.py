from flask import Flask, request, jsonify
from flask import Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt_header
from datetime import datetime
import psycopg2
from config import load_config
from uuid import uuid4


accomodation = Blueprint('accomodation', __name__)

config  = load_config()


@accomodation.route('/get_accomodation', methods=['GET'])
@jwt_required()
def get_accomodation():
    user_details = get_jwt_header()
    user_id = user_details['sid']
    print(user_id)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"SELECT * FROM accomodated_at WHERE participant_id='{user_id}';")
                rows = cur.fetchall()
                if not rows:
                    return jsonify({'details': ''}), 200
                else:
                    return jsonify({'data': rows}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Fetching accomodation'}), 404
                
@accomodation.route('/book_accomodation', methods=['POST'])
@jwt_required()
def book_accomodation():
    user_details = get_jwt_header()
    user_id = user_details['sid']
    data = request.get_json()
    # accomodation_datails = {}
    # accomodation_datails['location'] = data['location']
    # accomodation_datails['check_in'] = data['from']
    # accomodation_datails['check_out'] = data['to']
    # accomodation_datails['food_type'] = data['food_type']
    # accomodation_datails['payment'] = data['payment']

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"SELECT * FROM logistics WHERE location='{data['location']}' and check_in = '{data['from']}' and check_out = '{data['to']}' and food_type = '{data['food_type']}';")
                rows = cur.fetchall()
                print(rows)
                if not rows:
                    logistics_id = str(uuid4())
                    try:
                        cur.execute(f"INSERT INTO logistics VALUES ('{logistics_id}', '{data['location']}', '{data['from']}', '{data['to']}', '{data['food_type']}', {int (data['payment'])});")
                    except (Exception, psycopg2.DatabaseError) as error:
                        print(error)
                        return jsonify({'message': 'Error registering logistics'}), 404
                else:
                    logistics_id = rows[0][0]
                try:
                    cur.execute(f"INSERT INTO accomodated_at VALUES ('{user_id}', '{logistics_id}', 'pending');")
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                    return jsonify({'message': 'Error accomodating user'}), 404
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error accomodating user'}), 404
    return jsonify({'message': "Accomodation successful"}), 200
    
