from flask import Flask, request, jsonify
from flask import Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt_header
from datetime import datetime
import psycopg2
from config import load_config
from uuid import uuid4


admin_manage_user = Blueprint('admin_manage_user', __name__)

config  = load_config()

@admin_manage_user.route('/all_students', methods=['GET'])
@jwt_required()
def all_students():
    user_details = get_jwt_header()
    if(user_details['role'] != 'admin'):
        return jsonify({'message': 'Unauthorized'}), 401
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"SELECT * FROM STUDENT;")
                rows = cur.fetchall()
                if not rows:
                    return jsonify({'details': ''}), 200
                else:
                    all_students_list = []
                    for row in rows:
                        student = {
                            'sid':  row[0],
                            'email': row[1],
                            'name': row[2],
                            'roll_number': row[3],
                            'phone': row[4],
                            'college': row[5],
                            'department': row[6],
                            'year': row[7],
                            'type': row[8]
                        }
                        all_students_list.append(student)
                    return jsonify(all_students_list), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Fetching events'}), 404

@admin_manage_user.route('/remove_student/<string:id>', methods=['DELETE'])
@jwt_required()
def remove_user(id):
    user_details = get_jwt_header()
    if(user_details['role'] != 'admin'):
        return jsonify({'message': 'Unauthorized'}), 401
    # data = request.get_json()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"DELETE FROM STUDENT WHERE sid='{id}';")
                return jsonify({'message': 'User successfully deleted'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Deleting user'}), 404
    
@admin_manage_user.route('/all_organisers', methods=['GET'])
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
        return jsonify({'message': 'Error Fetching events'}), 404

@admin_manage_user.route('/remove_organiser/<string:id>', methods=['DELETE'])
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
        return jsonify({'message': 'Error Deleting user'}), 404
    
