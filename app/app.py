from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import random
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
CORS(app)
app.secret_key = '123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bingo_game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
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

@app.route('/admin/new_session', methods=['POST'])
def new_session():
    session = GameSession()
    db.session.add(session)
    db.session.commit()
    return jsonify({'success': True, 'session_id': session.unique_id}), 201



@app.route('/register', methods=['POST'])
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

@app.route('/admin/start_game', methods=['POST'])
def start_game():
    session_id = request.form.get('session_id')
    game_session = GameSession.query.filter_by(unique_id=session_id).first()
    if game_session and game_session.status == 'waiting':
        game_session.status = 'in_progress'
        db.session.commit()
        return jsonify({'success': True, 'message': 'Game started'}), 200
    else:
        return jsonify({'success': False, 'error': 'Session not found or already started'}), 400


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


    # You can add more methods for game logic, like checking for a win

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_board', methods=['POST'])
def generate_board():
    username = request.form.get('username')
    game = BingoGame()
    return jsonify({'username': username, 'board': game.board})


if __name__ == '__main__':
    app.run(debug=True)