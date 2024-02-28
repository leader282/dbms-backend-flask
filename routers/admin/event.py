from flask import Flask, request, jsonify
from flask import Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt_header
from datetime import datetime
import psycopg2
from config import load_config
from uuid import uuid4


admin_event = Blueprint('admin_event', __name__)

config  = load_config()

@admin_event.route('/events', methods=['GET'])
@jwt_required()
def all_events():
    user_details = get_jwt_header()
    if(user_details['role'] != 'admin'):
        return jsonify({'message': 'Unauthorized'}), 401
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"SELECT * FROM EVENT;")
                rows = cur.fetchall()
                if not rows:
                    return jsonify({'details': ''}), 200
                else:
                    return jsonify({'data': rows}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Fetching events'}), 404

@admin_event.route('/add_event', methods=['POST'])
@jwt_required()
def add_event():
    user_details = get_jwt_header()
    if(user_details['role'] != 'admin'):
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                event_id = str(uuid4())
                if data['type'] == 'competition':
                    cur.execute(f"INSERT INTO EVENTS VALUES ('{event_id}', '{data['name']}', '{data['type']}', '{data['info']}', {data['start_date_time']}', {data['end_date_time']}', '{data['location']}', '{data['first_prize']}' , '{data['second_prize']}', '{data['third_prize']}');")
                else:
                    cur.execute(f"INSERT INTO EVENTS VALUES ('{event_id}', '{data['name']}', '{data['type']}', '{data['info']}', {data['start_date_time']}', {data['end_date_time']}', '{data['location']}', NULL, NULL, NULL);")
                return jsonify({'message': 'Event successfully added'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Adding event'}), 404

@admin_event.route('/delete_event', methods=['POST'])
@jwt_required()
def delete_event():
    data = request.get_json()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"DELETE FROM EVENT WHERE id='{data['id']};")
                return jsonify({'message': 'Event successfully deleted'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Deleting event'}), 404
    
@admin_event.route('/update_event', methods=['POST'])
@jwt_required()
def update_event():
    user_details = get_jwt_header()
    if(user_details['role'] != 'admin'):
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                if data['type'] == 'competition':
                    cur.execute(f"UPDATE EVENT SET name='{data['name']}', type='{data['type']}', info='{data['info']}', start_date_time={data['start_date_time']}, end_date_time={data['end_date_time']}, location='{data['location']}', first_prize='{data['first_prize']}', second_prize='{data['second_prize']}', third_prize='{data['third_prize']}' WHERE id='{data['id']}';")
                else:
                    cur.execute(f"UPDATE EVENTS SET name='{data['name']}', type='{data['type']}', info='{data['info']}', start_date_time={data['start_date_time']}, end_date_time={data['end_date_time']}, location='{data['location']}', first_prize=NULL, second_prize=NULL, third_prize=NULL WHERE id='{data['id']}';")
                return jsonify({'message': 'Event successfully updated'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Updating event'}), 404