
#packages
from flask import Flask
from flask import render_template
from flask import request
import chess
import chess.engine

# engine_path = r"C:\Users\14244\Desktop\Chesspp\chessgui\engine\stockfish-windows-x86-64-avx2.exe"
engine_path = r"C:\Users\14244\Desktop\Chesspp\chessgui\engine\switch_board.exe"

# create chess engine instance
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

# web app instance
app = Flask(__name__)

# root(index) route
@app.route('/')
def root():
	return render_template('chessinator.html')
	
# make move API
@app.route('/make_move', methods=['POST'])
def make_move():

	# extract fen string from http post request body
	fen = request.form.get('fen')
	
	# init python chess board instance
	board = chess.Board(fen)
	
	# search for best move
	result = engine.play(board, chess.engine.Limit(time=20.0))
	
	# update internal python chess board state
	board.push(result.move)
	
	# extract FEN from current board state
	fen = board.fen()
	
	return {'fen': fen}

# main driver
if __name__ == '__main__':
	#start HTTP server
	app.run(debug=True, threaded=True)
	
