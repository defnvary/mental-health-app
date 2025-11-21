from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def hello_world():
    return "Hello, World from Postgres + Flask"

@main_bp.route('/test', methods=['GET'])
def test():
    return "Test route is working"