from flask import Flask, request, jsonify
from flask import Blueprint
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt_header
from datetime import datetime
import psycopg2
from config import load_config
from uuid import uuid4


admin_organiser = Blueprint('admin_organiser', __name__)

config  = load_config()

@admin_organiser.route('/all_organisers', methods=['GET'])
@jwt_required()
def all_organisers():
    user_details = get_jwt_header()
    if(user_details['role'] != 'admin'):
        return jsonify({'message': 'Unauthorized'}), 401
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"SELECT * FROM ORGANISERS;")
                organiser_rows = cur.fetchall()
                if not organiser_rows:
                    return jsonify({'details': ''}), 200
                else:
                    all_organisers_list = []
                    for organiser_row in organiser_rows:
                        oid = organiser_row[0]
                        events_sponsored = []
                        try:
                            cur.execute(f"SELECT * FROM MANAGES WHERE organiser_id='{oid}';")
                            manages_rows = cur.fetchall()
                            if len(manages_rows):
                                for manages_row in manages_rows:
                                    # print(row)
                                    if manages_row[4] == 'approved':
                                        event_id = manages_row[0]
                                        try:
                                            cur.execute(f"SELECT * FROM EVENT WHERE id='{event_id}';")
                                            event_rows = cur.fetchall()
                                            if len(event_rows):
                                                events_sponsored.append(
                                                    {
                                                        'eid': event_id,
                                                        'name': event_rows[0][1],
                                                        'payment_status': manages_row[4]

                                                    }
                                                )
                                        except:
                                            print(f'Error fetching event {event_id}')
                                        # else:
                                        #     print("Not approved")
                        except:
                            print(f'Error fetching events for organiser {oid}')
                        # print(events_sponsored)
                        # print("here here")
                        # print(organiser_row)
                        organiser = {
                            'oid':  organiser_row[0],
                            'email': organiser_row[1],
                            'name': organiser_row[2],
                            'phone': organiser_row[3],
                            'events_sponsored': events_sponsored,
                        }
                        # print(organiser)
                        all_organisers_list.append(organiser)
                    return jsonify(all_organisers_list), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Fetching organisers'}), 404

@admin_organiser.route('/remove_organiser/<string:id>', methods=['DELETE'])
@jwt_required()
def remove_organiser(id):
    user_details = get_jwt_header()
    if(user_details['role'] != 'admin'):
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"DELETE FROM ORGANISER WHERE id='{id}';")
                return jsonify({'message': 'User successfully deleted'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Deleting organiser'}), 404
    
@admin_organiser.route('/add_organiser', methods=['POST'])
@jwt_required()
def add_organiser():
    user_details = get_jwt_header()
    if(user_details['role'] != 'admin'):
        return jsonify({'message': 'Unauthorized'}), 401
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
        return jsonify({'message': 'Error Creating organiser'}), 404