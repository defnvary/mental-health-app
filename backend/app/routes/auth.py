from flask import Blueprint, request, jsonify
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/create-user', methods = ['POST'])
def create_user():
    # get data from request
    data = request.get_json()
    print(data)

    # validate required fields, empty data, contains emai, contains password
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required!'}), 400
    
    # check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'User already exists with this email'}), 409

    # create new user
    new_user = User(email=data['email'], password=data['password'])  # type: ignore  

    # save to database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created', 'user_id': new_user.id}), 201
    


@auth_bp.route('/users', methods = ['GET'])
def list_users():
    # get all users from database
    users = User.query.all()

    # convert to list format for JSON response
    users_list = []
    for user in users:
        users_list.append({
            'id': user.id,
            'email': user.email
        })
    
    return jsonify({'users': users_list})
