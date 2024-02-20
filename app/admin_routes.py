from flask import Blueprint, jsonify, request
from .models import db, GameSession

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/new_session', methods=['POST'])
def new_session():
    session = GameSession()
    db.session.add(session)
    db.session.commit()
    return jsonify({'success': True, 'session_id': session.unique_id}), 201

@admin_bp.route('/start_game', methods=['POST'])
def start_game():
    session_id = request.form.get('session_id')
    game_session = GameSession.query.filter_by(unique_id=session_id).first()
    if game_session and game_session.status == 'waiting':
        game_session.status = 'in_progress'
        db.session.commit()
        return jsonify({'success': True, 'message': 'Game started'}), 200
    else:
        return jsonify({'success': False, 'error': 'Session not found or already started'}), 400
