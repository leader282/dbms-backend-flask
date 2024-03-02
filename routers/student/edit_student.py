from flask import Flask, request, jsonify
from flask import Blueprint
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt_header
from datetime import datetime
import psycopg2
from psql_config import load_config
from uuid import uuid4


student = Blueprint('student', __name__)

config  = load_config()

@student.route('/edit_student', methods=['PUT'])
@jwt_required()
def edit_student():
    profile_info = get_jwt_header()
    if profile_info.get('sid', 0) == 0:
        return jsonify({'message': 'User doesnot have access here'}), 404
    data = request.get_json()
    sid = profile_info.get('sid', 0)
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    allowed_fields = ['name', 'roll_number', 'phone', 'college', 'department', 'year', 'password']
    update_fields = {key: data[key] for key in allowed_fields if key in data}
    update_fields['password'] = hashed_password

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Constructing the SQL query dynamically based on the available fields
                cur.execute(f"SELECT * FROM STUDENT WHERE sid='{sid}';")
                rows = cur.fetchall()
                if(rows):
                    query = ""
                    for key, value in update_fields.items():
                        query += f"{key}='{value}', "
                    query = query[:-2]
                    cur.execute(f"UPDATE STUDENT SET " + query + f" WHERE sid='{sid}';")
                    return jsonify({'message': 'Student has been updated successfully'}), 200
                else:
                    return jsonify({'message': 'Student doesnot exist'}), 402
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Updating student'}), 402