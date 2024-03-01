from flask import Flask, request, jsonify
from flask import Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt_header
from datetime import datetime
import psycopg2
from psql_config import load_config
from uuid import uuid4


admin_notif = Blueprint('admin_notif', __name__)

config  = load_config()

@admin_notif.route('/notifs/<string:oid>', methods=['GET'])
@jwt_required()
def all_notifs(oid):
    user_details = get_jwt_header()
    if(user_details['role'] != 'admin'):
        return jsonify({'message': 'Unauthorized'}), 401
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"SELECT event_id, EVENT.name, type FROM EVENT, MANAGES, ORGANISERS WHERE organiser_id=oid AND event_id=id AND request_status='pending' AND oid={oid};")
                rows = cur.fetchall()
                all_notifs_list = []
                for row in rows:
                    notif = {
                        'event_id': row[0],
                        'ename': row[1],
                        'type': row[2]
                    }
                    all_notifs_list.append(notif)
                return jsonify(all_notifs_list), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Fetching events'}), 404
    
@admin_notif.route('/notifs/approve/<string:oid>/<string:eid>', methods=['PUT'])
@jwt_required()
def approve_event(oid, eid):
    user_details = get_jwt_header()
    if(user_details['role'] != 'admin'):
        return jsonify({'message': 'Unauthorized'}), 401
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"UPDATE MANAGES SET request_status='approved' WHERE organiser_id={oid} AND event_id={eid}")
                return jsonify({'message': 'Event has been approved successfully'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Fetching events'}), 404
    
@admin_notif.route('/notifs/reject/<string:oid>/<string:eid>', methods=['PUT'])
@jwt_required()
def reject_event(oid, eid):
    user_details = get_jwt_header()
    if(user_details['role'] != 'admin'):
        return jsonify({'message': 'Unauthorized'}), 401
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Executing the selected query
                cur.execute(f"UPDATE MANAGES SET request_status='rejected' WHERE organiser_id={oid} AND event_id={eid}")
                return jsonify({'message': 'Event has been rejected successfully'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Fetching events'}), 404