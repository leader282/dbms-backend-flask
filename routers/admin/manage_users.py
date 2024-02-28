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
                    return jsonify({'data': rows}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Fetching events'}), 404

@admin_manage_user.route('/remove_student/<int:id>', methods=['DELETE'])
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
                cur.execute(f"DELETE FROM STUDENT WHERE id='{id}';")
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
                cur.execute(f"SELECT * FROM ORGANISER;")
                rows = cur.fetchall()
                if not rows:
                    return jsonify({'details': ''}), 200
                else:
                    return jsonify({'data': rows}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'message': 'Error Fetching events'}), 404

@admin_manage_user.route('/remove_organiser/<int:id>', methods=['DELETE'])
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
    
