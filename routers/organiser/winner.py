from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_header
import psycopg2
from psql_config import load_config
from flask import Blueprint

winner_settings = Blueprint('winner_settings', __name__)
config  = load_config()

# @winner_settings.route('/set_winners/<string:pos>/<string:event_id>', methods=['POST'])
# @jwt_required
# def set_winners(pos,event_id):
#     profile_info = get_jwt_header()
#     student_id = request.get_json()

#     if pos == '1':
#     if profile_info.get('oid', 0) == 0:
#         return jsonify({'message': 'User does not have access here'}), 404
#     try:
#         with psycopg2.connect(**config) as conn:
#             with conn.cursor() as cur:
#                 cur.execute(f"SELECT * FROM WINNERS WHERE event_id='{event_id}';")
#                 winner_rows = cur.fetchall()
#                 if winner_rows
    
    