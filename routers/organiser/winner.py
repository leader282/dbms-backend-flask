from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_header
import psycopg2
from psql_config import load_config
from flask import Blueprint

winner_settings = Blueprint('winner_settings', __name__)
config  = load_config()

# @winner_settings.route('/set_winners/<string:event_id>', methods=['POST'])
# @jwt_required
# def set_winners(event_id):
#     profile_info = get_jwt_header()
#     first_winner_id = request.get_json()
#     if profile_info.get('oid', 0) == 0:
#         return jsonify({'message': 'User doesnot have access here'}), 404
#     try:
#         with psycopg2.connect(**config) as conn:
#             with conn.cursor() as cur:
#                 oid = profile_info.get('oid', 0)
#                 cur.execute(f"SELECT * FROM MANAGES WHERE organiser_id='{oid}' AND event_id='{event_id}'")
#                 rows = cur.fetchall()
#                 if len(rows) == 0:
#                     cur.execute(f"INSERT INTO MANAGES VALUES ('{event_id}', '{oid}', '{sponsorship_amount}', '{payment_status}');")
#                     return jsonify({'message': 'Event has been sponsored successfully'}), 200
#                 else:
#                     return jsonify({'message': 'Already sponsored this event'}), 404
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#         return jsonify({'message': 'Error in sponsoring'}), 404