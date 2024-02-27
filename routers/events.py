from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_header
import psycopg2
from config import load_config
from flask import Blueprint

events = Blueprint('events', __name__)
config  = load_config()

@events.route('/', methods=['GET'])
@jwt_required()
def get_all_events():
    profile_info = get_jwt_header()
    all_events_list = []
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, type, start_date_time, end_date_time FROM EVENTS;")
                rows = cur.fetchall()
                sid = profile_info.get('sid', 0)
                oid = profile_info.get('oid', 0)
                for row in rows:
                    eid = row[0]
                    event = {
                        'eid': eid,
                        'name': row[1],
                        'type': row[2],
                        'start_date_time': row[3],
                        'end_date_time': row[4]
                    }
                    if sid:
                        cur.execute(f"SELECT * FROM PARTICIPATION WHERE student_id='{sid}' AND event_id='{eid}';")
                        rows = cur.fetchall()
                        if len(rows):
                            event['registered'] = False
                        else:
                            event['registered'] = True
                        cur.execute(f"SELECT * FROM VOLUNTEERS WHERE student_id='{sid}' AND event_id='{eid}';")
                        rows = cur.fetchall()
                        if len(rows):
                            event['volunteered'] = False
                        else:
                            event['volunteered'] = True
                    elif oid:
                        cur.execute(f"SELECT * FROM MANAGES WHERE organiser_id='{oid}' AND event_id='{eid}';")
                        rows = cur.fetchall()
                        if len(rows):
                            event['sponsored'] = False
                        else:
                            event['sponsored'] = True
                    all_events_list.append(event)
                return jsonify(all_events_list), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error fetching events'}), 404

@events.route('/<string:event_id>', methods=['GET'])
@jwt_required()
def get_an_event(event_id):
    profile_info = get_jwt_header()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM EVENTS WHERE id='{event_id}';")
                row = cur.fetchall()[0]
                sid = profile_info.get('sid', 0)
                oid = profile_info.get('oid', 0)
                event = {
                    'eid': row[0],
                    'name': row[1],
                    'type': row[2],
                    'info': row[3],
                    'start_date_time': row[4],
                    'end_date_time': row[5],
                    'location': row[6],
                    'first_prize': row[7],
                    'second_prize': row[8],
                    'third_prize': row[9],
                    'created_at': row[10]
                }
                if sid:
                    cur.execute(f"SELECT * FROM PARTICIPATION WHERE student_id='{sid}';")
                    rows = cur.fetchall()
                    if len(rows):
                        event['registered'] = False
                    else:
                        event['registered'] = True
                elif oid:
                    cur.execute(f"SELECT * FROM MANAGES WHERE organiser_id='{oid}';")
                    rows = cur.fetchall()
                    if len(rows):
                        event['sponsored'] = False
                    else:
                        event['sponsored'] = True
                return jsonify({'event': event}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error fetching events'}), 404
    
@events.route('/register/<string:event_id>', methods=['POST'])
@jwt_required()
def register(event_id):
    profile_info = get_jwt_header()
    if profile_info.get('oid', 0):
        return jsonify({'message': 'Organiser doesnot have access here'}), 404
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                sid = profile_info.get('sid', 0)
                cur.execute(f"INSERT INTO PARTICIPATION VALUES ('{event_id}', '{sid}');")
                return jsonify({'message': 'Registered in event successfully'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error fetching events'}), 404