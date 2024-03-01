from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_header
import psycopg2
from psql_config import load_config
from flask import Blueprint

winner_settings = Blueprint('winner_settings', __name__)
config  = load_config()

@winner_settings.route('/set_winners/<string:event_id>', methods=['POST'])
@jwt_required()
def set_winners(event_id):
    profile_info = get_jwt_header()
    sid1 = request.get_json()['sid1']
    sid2 = request.get_json()['sid2']
    sid3 = request.get_json()['sid3']
    if profile_info.get('oid', 0) == 0:
        return jsonify({'message': 'User does not have access here'}), 404
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM WINNERS WHERE event_id='{event_id}';")
                rows = cur.fetchall()
                if len(rows):
                    return jsonify({'message': 'Winners already set'}), 404
                else:
                    cur.execute(f"INSERT INTO WINNERS VALUES ('{event_id}', '{sid1}', '{sid2}', '{sid3}');")
                    return jsonify({'message': 'Winners set successfully'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Couldnot fetch profile'}), 404
    
    