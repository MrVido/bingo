from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

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