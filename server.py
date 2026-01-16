from flask import Flask, jsonify, request, render_template
from chess import Board, Color, find_piece_in_pos, other_color
#x = 2
app = Flask(__name__)

board = Board()
current_turn = Color.W.value  # 'white'

@app.route("/")
def index():
    return render_template("chess.html")  # Serve HTML from templates folder

@app.route("/state")
def state():
    pieces_list = []
    for p in board.pieces:
        pieces_list.append({
            "type": p.__class__.__name__,
            "color": p.color.value,
            "square": p.square
        })
    return jsonify({"pieces": pieces_list, "turn": current_turn})

@app.route("/move", methods=["POST"])
def move():
    global current_turn
    data = request.get_json()
    frm = data.get("from")
    to = data.get("to")

    piece = find_piece_in_pos(board, frm)
    if not piece:
        return jsonify({"error": f"No piece at {frm}"})
    if piece.color.value != current_turn:
        return jsonify({"error": f"Not your turn!"})

    legal_moves = piece.moves(board)
    if to not in legal_moves:
        return jsonify({"error": "Illegal move!"})

    board.move_piece(piece, to)
    current_turn = other_color(piece.color).value

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)

# from datetime import date
# from datetime import datetime
# from enum import Enum

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     now = datetime.now()
#     return str(now)

# # http://127.0.0.1:5000/abc
# @app.route("/abc")
# def m1():
#     return "hello Lisa!"

# # http://127.0.0.1:5000/m2?q=Lisa
# @app.route("/m2")
# def m2():
#     sss = request.args.get('q', 'Guest')
#     return f"You reqeusted {sss}!"

# # http://127.0.0.1:5000/m3?q=Test&g=Lisa
# @app.route("/m3")
# def m3():
#     qqq = request.args.get('q', 'Hello')
#     ggg = request.args.get('g', 'Guest')
#     return f"{qqq} {ggg}!"

# @app.route("/add")
# def m4():
#     qqq = request.args.get('a', '10')
#     ggg = request.args.get('b', '20')
#     return str((int(qqq)+int(ggg)))

# @app.route("/movepiece")
# def m5():
#     current_pos = request.args.get('a', 'D4')
#     direction = request.args.get('b', 'NE')
#     print(f"move piece at {current_pos} in the {direction} direction")
#     return next_square(current_pos, Direction[direction])

# class Direction(Enum):
#     N = [0, 1, None, "8"]
#     E = [1, 0, "H", None]
#     S = [0, -1, None, "1"]
#     W = [-1, 0, "A", None]
#     NE = [1, 1, "H", "8"]
#     NW = [-1, 1, "A", "8"]
#     SW = [-1, -1, "A", "1"]
#     SE = [1, -1, "H", "1"]

# def next_square(current_square,direction):
#     # print(f"Moving {direction.name} from {current_square}")
#     x = int(current_square[1])
#     z = current_square[0]
#     arr = direction.value
#     x1 = x + arr[1]
#     z1 = (chr(ord(z) + arr[0]))
#     return (f"{z1}{x1}".upper())


# if __name__ == "__main__":
#     app.run(debug=True)

