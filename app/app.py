from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import random
from flask_sqlalchemy import SQLAlchemy
import uuid
import time


app = Flask(__name__)
CORS(app)
app.secret_key = '123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bingo_game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def generate_simple_session_id():
    timestamp = str(int(time.time()))[-900:]  # Current time in seconds since Epoch
    random_part = random.randint(10, 99)  # Random 4-digit number
    session_id = f"{timestamp}{random_part}"
    return session_id

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(50), unique=True, nullable=False, default=generate_simple_session_id)
    status = db.Column(db.String(10), default='waiting')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('game_session.id'), nullable=True)
    session = db.relationship('GameSession', back_populates='users')

GameSession.users = db.relationship('User', order_by=User.id, back_populates='session')

# Initialize database tables directly within app context, replacing @app.before_first_request
with app.app_context():
    db.create_all()

called_items = []

@app.route('/call_item', methods=['POST'])
def call_item():
    global called_items

    # Ensure the game is in progress
    game_session = GameSession.query.first()  # Assuming there's only one game session
    if game_session.status != 'in_progress':
        return jsonify({'success': False, 'error': 'Game is not in progress'}), 403

    remaining_items = list(set(bingo_items) - set(called_items))
    if not remaining_items:
        return jsonify({'success': False, 'error': 'All items have been called'}), 400

    # Randomly select an item that hasn't been called
    item = random.choice(remaining_items)
    called_items.append(item)

    # For simplicity, we just return the called item
    # In a real application, you might broadcast this to all participants
    return jsonify({'success': True, 'called_item': item})

#ROUTES

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

@app.route('/admin/new_session', methods=['POST'])
def new_session():
    new_session = GameSession(status='waiting')
    db.session.add(new_session)
    db.session.commit()
    return jsonify({'success': True, 'session_id': new_session.unique_id})



@app.route('/register', methods=['POST'])
def register_user():
    session_id = request.form['session_id']
    username = request.form['username']
    session = GameSession.query.filter_by(unique_id=session_id).first()
    if session and session.status == 'waiting':
        user = User(username=username, session_id=session.id)
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'User registered'})
    else:
        return jsonify({'success': False, 'error': 'Session not found or registration closed'}), 400

@app.route('/users', methods=['GET'])
def get_users():
    # Fetch all users from the database
    users = User.query.all()
    # Extract usernames and return them as a list
    usernames = [user.username for user in users]
    return jsonify(usernames=usernames)
    
    
@app.route('/admin/start_game', methods=['POST'])
def start_game():
    session_id = request.json.get('session_id')
    game_session = GameSession.query.filter_by(unique_id=session_id).first()
    if game_session:
        if game_session.status == 'waiting':
            game_session.status = 'in_progress'
            db.session.commit()
            # Confirm the status update
            updated_session = GameSession.query.filter_by(unique_id=session_id).first()
            print(f"Game session {updated_session.unique_id} status updated to {updated_session.status}")
            return jsonify({'success': True, 'message': 'Game started'}), 200
        else:
            return jsonify({'success': False, 'error': 'Game has already started or ended'}), 400
    return jsonify({'success': False, 'error': 'Session not found'}), 404

@app.route('/admin/end_game', methods=['POST'])
def end_game():
    session_id = request.json.get('session_id')
    game_session = GameSession.query.filter_by(unique_id=session_id).first()
    if game_session:
        # Update game session status to 'ended'
        game_session.status = 'ended'
        db.session.commit()
        return jsonify({'success': True, 'message': 'Game ended successfully'}), 200
    else:
        return jsonify({'success': False, 'error': 'Session not found'}), 404

@app.route('/generate_board', methods=['POST'])
def generate_board():
    username = request.form.get('username')
    game = BingoGame()
    return jsonify({'username': username, 'board': game.board})

@app.route('/admin/game_status', methods=['GET'])
def game_status():
    session_id = request.args.get('session_id')  # Or however you choose to identify the session
    game_session = GameSession.query.filter_by(unique_id=session_id).first()
    if game_session:
        users = User.query.filter_by(session_id=game_session.id).all()
        usernames = [user.username for user in users]
        return jsonify({
            'success': True,
            'game_session': {
                'id': game_session.id,
                'unique_id': game_session.unique_id,
                'status': game_session.status,
                'active_players': len(users),
                'usernames': usernames
            }
        })
    else:
        return jsonify({'success': False, 'error': 'No game session found'}), 404




# Utility function for generating a bingo board
class BingoGame:
    def __init__(self):
        self.board = self.generate_board()

    def generate_board(self):
        # Generate a 5x5 Bingo board with random items
        board = []
        items = random.sample(bingo_items, 25)  # 24 unique items for the board
        for i in range(0, 25, 5):
            board.append(items[i:i+5])
        board[2][2] = 'mainsquare'  
        return board


# List of Bingo images (file names without extension)
bingo_items = [
    "ac_milan", "afc_bournemouth", "arsenal", "borussia_dortmund", "brentford",
    "celtic_fc", "chanel", "chelsea", "dior", "dkny",
    "dolce_and_gabana", "eintracht_frankfurt", "everton", "fc_barcelona", "fc_bayern_munchen",
    "fc_copenhagen", "fc_internazionale_milano", "fc_porto", "fc_salzburg", "fc_shakhtar_donetsk",
    "fc_viktoria_plzen", "fulham", "gnk_dinamo_zagreb", "gucci", "hermes",
    "juventus", "leincester_city", "louis_vutton", "manchester_city", "michael_kors",
    "olympic_de_marseille", "prada", "rb_leipzig", "real_madrid_fc", "sevilla_fc",
    "ssc_napoli", "ted_baker", "tiffany", "tottenham_hotspur", "versace",
    "westham_united"
]




if __name__ == '__main__':
    app.run(debug=True)