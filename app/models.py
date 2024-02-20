from flask_sqlalchemy import SQLAlchemy
import uuid
import random

db = SQLAlchemy()

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    status = db.Column(db.String(10), default='waiting')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('game_session.id'), nullable=True)
    session = db.relationship('GameSession', back_populates='users')

# Function to generate bingo board
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