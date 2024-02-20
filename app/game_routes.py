from flask import Blueprint, jsonify, request
from .models import BingoGame, db, User, GameSession, bingo_items, create_bingo_board
import random

game_bp = Blueprint('game_bp', __name__)

@game_bp.route('/register', methods=['POST'])
def register_user():
    username = request.form.get('username')
    session_id = request.form.get('session_id')
    
    game_session = GameSession.query.filter_by(unique_id=session_id).first()
    if not game_session or game_session.status != 'waiting':
        return jsonify({'success': False, 'error': 'Invalid or closed session'}), 400

    if username and not User.query.filter_by(username=username, session_id=game_session.id).first():
        user = User(username=username, session=game_session)
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': True, 'username': username})
    else:
        return jsonify({'success': False, 'error': 'Username is taken or invalid'}), 400

@game_bp.route('/generate_board', methods=['POST'])
def generate_board():
    username = request.form.get('username')
    game = BingoGame()
    return jsonify({'username': username, 'board': game.board})
