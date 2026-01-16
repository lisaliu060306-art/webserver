from enum import Enum
import sys

class Board:
    def __init__(self, fill_pieces=True):
        self.squares = []
        self.pieces = []

        self.position = 1
        char_arr = ["A", "B", "C", "D", "E", "F", "G", "H"]
        for col in range(8, 0, -1):    
            for row in char_arr:
                number = f"{row}{col}"
                if (self.position % 2 == 0):
                    self.col = "white"
                else:
                    self.col = "black" 
                # print(f"Creating Square with color {self.col} and numner = {number}")
                self.position += 1
                square = Square(self.col, number)
                self.squares.append(square)
        if fill_pieces == True:
            for c in Color:
                # create pawns 
                for p in range (1,9):    
                    row = "2" if c == Color.W else "7"
                    pawn = Pawn(c,f"{chr(p+64)}{row}")
                    self.pieces.append(pawn)
                # create pieces
                rn = "1" if c==Color.W else "8"
                for p in PieceName:
                    for cn in p.value:
                        x = globals()[p.name](c,f"{cn}{rn}")
                        self.pieces.append(x)
    """Check what pieces are on what squares"""
    def piece_at (self, square):
        for p in self.pieces:
            if p.square == square:
                return p
        return None
    """Check if the squares are empty"""
    def is_empty (self, square):
        return self.piece_at(square) is None
    def move_piece (self, piece, target_square):
        """
        Moves a piece to a target square, and capture the piece if there is any
        """
        captured = self.piece_at(target_square)
        if captured:
            self.pieces.remove(captured)
        piece.square = target_square

        """
        Pawn promotion
        """
        if isinstance (piece, Pawn):
            last_rank = "8" if piece.color == Color.W else "1"
            if target_square[1] == last_rank:
                new_piece = Queen (piece.color, target_square)
                self.pieces.remove(piece)
                self.pieces.append(new_piece)
                print(f"Pawn now promoted to Queen at {target_square}")

    def puts_in_check (self, piece, target_square):
        original_square = piece.square
        captured = self.piece_at(target_square)
        if captured:
            self.pieces.remove(captured)
        piece.square = target_square
        in_check = self.is_in_check(piece.color)
        piece.square = original_square
        if captured:
            self.pieces.append(captured)
        return in_check


    
        # king = None
        # for piece in self.pieces:
        #     if isinstance(piece, King) and piece.color == color:
        #         king = piece
        #         break
        # king_pos = king.square
        # for piece in self.pieces:
        #     if piece.color != color:
        #         if king_pos in piece.moves(self):
        #             return True
        # return False
    def is_in_check(self, color: Color):
        king = None
        for piece in self.pieces:
            if isinstance(piece, King) and piece.color == color:
                king = piece
                break
        king_pos = king.square
        print(f"Checking if the {color.name} king at {king_pos} is in check...")
        for piece in self.pieces:
            if piece.color != color:
                if isinstance(piece, King):
                    continue  # <- skip enemy kings to avoid recursion
                if king_pos in piece.moves(self):
                    print(f"King is in check from {piece.__class__.__name__} at {piece.square}")
                    return True
        return False

    def checkmate(self, color: Color) -> bool:
        # if not self.is_in_check(color):
        #     return False
        for p in self.pieces:
            if p.color == color:
                for move in p.moves(self):
                    original_sq = p.square
                    captured = self.piece_at(move)
                    self.move_piece(p, move)
                    # If the king is no longer in check after the move
                    if not self.is_in_check(color):
                        # Undo move
                        p.square = original_sq
                        if captured:
                            self.pieces.append(captured)
                        return False
                    # Undo move if it did not help
                    p.square = original_sq
                    if captured:
                        self.pieces.append(captured)
        #No escape move checkmate!
        return True
    


    def assert_game_status(self, color: Color):
         if self.is_in_check(color):
            print(f"{assert_check.RED.value}{color.value} king is in CHECK!{assert_check.RESET.value}")
         if self.checkmate(color):
            print(f"{assert_check.RED.value}{color.value} king is in CHECKMATE!{assert_check.RESET.value}")
        
        
class assert_check(Enum):
    RED = "\033[91m"
    RESET = "\033[0m"            
                
class PieceName(Enum):
    Rook = ["A","H"]
    Knight = ["B","G"]
    Bishop = ["C","F"]
    King =["E"]
    Queen = ["D"]
                                

class Square:
    def __init__(self, color, number):
        self.color = color
        self.number = number
    def __str__(self):
        return (f"{self.color} {self.number}")
    

class ChessError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    
    
def next_square(current_square,direction):
    # print(f"Moving {direction.name} from {current_square}")
    x = int(current_square[1])
    z = current_square[0]
    arr = direction.value
    if arr[3] and str(x) == arr[3]:
        raise ChessError("Cannot move further")
    if arr[2] and z == arr[2]:
        raise ChessError("Cannot move further")
    x1 = x + arr[1]
    z1 = (chr(ord(z) + arr[0]))
    return (f"{z1}{x1}".upper())

    # if direction == Direction.NORTH:
    #     arr = direction.value
    #     if x == 8:
    #         raise ChessError("Cannot move further")
    #     x1 = x + arr[1]
    #     z1 = (chr(ord(z) + arr[0]))
    #     return (f"{z1}{x1}")
    # elif direction == Direction.SOUTH:
    #     if x == 1:
    #         raise ChessError("Cannot move further")
    #     y = x + direction.value
    #     return (f"{z}{y}")
    # elif direction == Direction.WEST:
    #     if z == "a":
    #         raise ChessError("Cannot move further")
    #     c = (chr(ord(z) - 1))
    #     return (f"{c}{x}")
    # elif direction == Direction.EAST:
    #     if z == "h":
    #         raise ChessError("Cannot move further")
    #     c = (chr(ord(z) + 1))
    #     return (f"{c}{x}")
    # elif direction == Direction.NORTHEAST:
    #     if x == 8 or z == "h":
    #         raise ChessError("Cannot move further")
    #     y = x + 1
    #     c = (chr(ord(z) + 1))
    #     return (f"{c}{y}")

# def north_east(current_square):
#     p1 = next_square(current_square, Direction.NORTH)
#     return next_square(p1, Direction.EAST)

    
class Direction(Enum):
    NORTH = [0, 1, None, "8"]
    EAST = [1, 0, "H", None]
    SOUTH = [0, -1, None, "1"]
    WEST = [-1, 0, "A", None]
    NORTHEAST = [1, 1, "H", "8"]
    NORTHWEST = [-1, 1, "A", "8"]
    SOUTHWEST = [-1, -1, "A", "1"]
    SOUTHEAST = [1, -1, "H", "1"]

class Color(Enum):
    W = "white"
    B = "black"

def other_color(color:Color):
    return Color.B if color == Color.W else Color.W

class Image(Enum):
    King = ["\u2654", "\u265A"]
    Queen = ["\u2655", "\u265B"]
    Rook = ["\u2656", "\u265C"]
    Bishop = ["\u2657", "\u265D"]
    Knight = ["\u2658", "\u265E"]
    Pawn = ["\u2659", "\u265F"]

        
class Piece:
    def __init__(self, color, square):
        self.color = color
        self.square = square

    def multi_sq(self, start_square,directions,board):
        """
        Returns the list of squares you can go to. 
        :param start_square: Where you piece is currently 
        :param directions: Which Directions a piece can go. 
        """
        moves=[] 
        for direction in directions:
            current = start_square
            while True:
                try:
                    current = next_square(current, direction)
                    """
                    Check if a piece is on this square
                    """
                    piece_on_square = board.piece_at(current)
                    """
                    If there is no piece on the square->move there;
                    If enemy piece: capture and the stop;
                    If it is my own piece or a friendly piece just stops and cannot move further
                    """
                    if piece_on_square is None:
                        moves.append(current)
                    elif piece_on_square.color != self.color:
                        moves.append(current)
                        break
                    else:
                        break
                except ChessError:
                    break
        return moves
    
    def moves (self,board):
        raise NotImplementedError
    def __str__(self):
        return (f"[{self.color.name}] {self.__class__.__name__} at {self.square}")
    

class Pawn(Piece):
    def moves (self,board):
        moves = []
        direction = Direction.NORTH if self.color == Color.W else Direction.SOUTH
        try:
            one_step = next_square(self.square, direction)
            if board.is_empty(one_step):
                moves.append(one_step)
                """
                Take two steps if on a starting row
                """
                starting_row = "2" if self.color == Color.W else "7"
                if self.square[1] == starting_row:
                    two_step = next_square(one_step, direction)
                    if board.is_empty (two_step):
                        moves.append(two_step)
        except ChessError:
            pass
        """
        Capture diagonally
        """
        diag_dir = [Direction.NORTHEAST,Direction.NORTHWEST] if self.color == Color.W else [Direction.SOUTHEAST,Direction.SOUTHWEST]
        """
        Loop over every direction to capture
        """
        for d in diag_dir:
            try:
                diag = next_square(self.square,d)
                piece = board.piece_at(diag)
                if piece is not None and piece.color != self.color:
                    moves.append(diag)
            except ChessError:
                continue
        return moves
    
class Rook(Piece):
    def moves (self,board):
        # moves=[]
        # directions = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
        # for direction in directions:
        #     current = self.square
        #     try:
        #         while True:
        #             current = next_square(current, direction)
        #             moves.append(current)
        #     except ChessError:
        #         break
        # return moves
        return self.multi_sq(self.square, [Direction.NORTH, Direction.EAST, Direction.WEST, Direction.SOUTH],board)
    
class Bishop (Piece):
    def moves (self, board):
        return self.multi_sq(self.square, [Direction.SOUTHEAST, Direction.SOUTHWEST, Direction.NORTHWEST, Direction.NORTHEAST],board)

class Queen(Piece):
    def moves (self,board):
        return self.multi_sq(self.square, [Direction.NORTH, Direction.EAST, Direction.WEST, Direction.SOUTH,Direction.SOUTHEAST, Direction.SOUTHWEST, Direction.NORTHWEST, Direction.NORTHEAST],board)
    
class King (Piece):
    def moves(self, board):
        move = []
        for direction in Direction:
            try:
                sq = next_square(self.square, direction)
                piece = board.piece_at(sq)
                # Cannot capture own piece
                if piece and piece.color == self.color:
                    continue
                # Cannot move into check
                if board.puts_in_check(self, sq):
                    continue
                move.append(sq)
            except ChessError:
                continue
        return move
        
    
class Knight (Piece):
    def moves (self,board):
        move = []
        letter = self.square[0]
        num = int(self.square[1])
        position = [(1,2),(1,-2),(-1,-2),(-1,2),(2,1),(2,-1),(-2,1),(-2,-1)]
        for (x,y) in position:
            try:
                new_letter = chr(ord(letter)+x)
                new_num = num + y
                if new_letter <"A" or new_letter > "H":
                    raise ChessError
                if new_num < 1 or new_num > 8:
                    raise ChessError
            except ChessError:
                continue
            move.append(f"{new_letter}{new_num}")
        return move


# N = Direction.NORTH
# E = Direction.EAST
# W = Direction.WEST
# S = Direction.SOUTH

# def possible_move_knight(start_pos):
#     possible_end_positions = []
#     paths = [[N, N, E], [N, N, W], [S, S, E], [S, S, W], [E, E, N], [E, E, S], [W, W, N], [W, W, S]]
#     for p in paths:
#         end_pos = start_pos
#         for d in p:
#             end_pos = next_square(end_pos, d)
#         possible_end_positions.append(end_pos)
#     print(possible_end_positions)


# def print_board(b):

def find_piece_in_pos(b:Board, pos) -> Piece:
    for p in b.pieces:
        if p.square == pos:
            return p
    return None


def print_board(b, dots=[], checkmatePos=None):
    WHITE_BG = '\033[47m'
    BLACK_BG = '\033[42m'
    """
    yellow background for all possible moves
    """
    MOVE_BG  = '\033[43m'
    CHECKMATE_BG  = '\033[41m'  # Background RED 
    RESET = '\033[0m'
    PIECE = '♖'  

    # for p in b.pieces:
    #     im_arr = Image[p.__class__.__name__].value
    #     im = im_arr[0] if p.color == Color.W else im_arr[1]
    #     print(im)
    #     print(f"{im} at {p.square}")

    rem = 0
    for i,j in enumerate(b.squares):
        if j.number in dots:
            bg = MOVE_BG
        elif j.number == checkmatePos:
            bg = CHECKMATE_BG    
        else:
            bg = WHITE_BG if i%2 == rem else BLACK_BG
        p = find_piece_in_pos(b, j.number)
        if p: 
            im_arr = Image[p.__class__.__name__].value
            im = im_arr[0] if p.color == Color.W else im_arr[1]
        else:
            # im = "*" if j.number in dots else " "
            im = "*" if j.number in dots else " "      
        print(f"{bg} {im} {RESET}", end="")
        if i%8 == 7:
            rem = 0 if rem==1 else 1
            print("") 


def test_check_mate_2_rooks():
    b = Board(fill_pieces=False)
    b.pieces.append(King(Color.B, "A1"))
    b.pieces.append(Rook(Color.W, "B8"))
    b.pieces.append(Rook(Color.W, "H2"))
    b.pieces.append(Bishop(Color.W, "H8"))
    if(b.checkmate(Color.B)):
        chm = "A1"
    # b.assert_game_status(Color.B)
    print_board(b, [], chm)
    


def test1():
    b = Board()
    # b1 = find_piece_in_pos(b, "C1")
    # b1.square = "G5"
    print_board(b)

    # for pp in b.pieces:
    #     print(pp)
    wp = find_piece_in_pos(b, "D2")

    # Place two black pawns on the diagonals C3 and E3
    # b.pieces.append(Pawn(Color.B, "C3"))
    # b.pieces.append(Pawn(Color.B, "E3"))

    # Check moves
    print("Possible moves for D2 pawn:", wp.moves(b))

    current_player = Color.W
    while True:
        wp = input("Which piece? ").upper()
        pm = find_piece_in_pos(b, wp)
        if not pm:
            print("No piece at that position.Try again!")
            continue
        if pm.color != current_player:
            print(f"That's not your piece! It is {current_player.name}'s move now.")
            continue
        possible_moves = pm.moves(b)
        print(possible_moves)
        if not possible_moves:
            print("No legal moves for this piece. Try again!")
            continue
        print_board(b, possible_moves)
        np = input("Where do you want to move? ").upper()
        if np not in possible_moves:
            print("Illegal move. Try again!")
            continue
        if b.puts_in_check(pm,np):
            print("Illegal move: cannot put your king in check!")
            continue
        # for i in range(1, 11):
        #     sys.stdout.write("\x1b[1A\x1b[2K")  
        try:
            b.move_piece(pm, np)
        except ChessError as e:
            print(e)
            continue
        print_board(b)
        b.assert_game_status(other_color(current_player))
        current_player = Color.B if current_player == Color.W else Color.W
        if b.checkmate(current_player):
            winner = other_color(current_player)
            print(f"{current_player.name} is checkmated.{winner.name} WINS!")
            print("GAME OVER")
            break

def test2():
    b = Board()
    # Remove all pieces for simplicity
    b.pieces = []

    # White king in corner
    b.pieces.append(King(Color.W, "H1"))

    # Black pieces delivering checkmate
    b.pieces.append(Rook(Color.B, "A1"))
    b.pieces.append(Queen(Color.B, "G2"))

    # Test
    b.assert_game_status(Color.W)



if __name__ == "__main__":        
    # print(next_square("d4",Direction.NORTH))
    # print(next_square("d4",Direction.SOUTH))
    # print(next_square("d4",Direction.WEST))
    # print(next_square("d4",Direction.EAST))
    # print(next_square("d4",Direction.NORTHEAST))
    # print(next_square("d4",Direction.NORTHWEST))
    # print(next_square("d4",Direction.SOUTHEAST))
    # print(next_square("d4",Direction.SOUTHWEST))

    # pawn = Pawn ("white", "d4")
    # print(pawn.moves())
    # pawn2 = Pawn ("black", "h6")
    # print(pawn2.moves())
    # # pawn3 = Pawn("white","h8")
    # # print(pawn3.moves())


    # rook = Rook("white","d4")
    # print(rook.moves())
    # bishop = Bishop ("White","d4")
    # print(bishop.moves()
    # queen = Queen ("black","d4")
    # print(queen.moves())
    # king = King ("black","d4")
    # print(king.moves())
    # knight = Knight("white","d4")
    # print("----------")
    # print(knight.moves())



    # try:
    #     print(next_square("h8",Direction.NORTH))
    # except ChessError as e:
    #     print(e)
    # try:        
    #     print(next_square("h1",Direction.SOUTH))
    # except ChessError as e:
    #     print(e)    
    # try:
    #     print(next_square("a3",Direction.WEST))
    # except ChessError as e:
    #     print(e)
    # try:
    #     print(next_square("h3",Direction.EAST))
    # except ChessError as e:
    #     print(e)
    # try:
    #     print(next_square("d8",Direction.NORTHEAST))
    # except ChessError as e:
    #     print(e)
    # try:
    #     print(next_square("h3",Direction.NORTHEAST))
    # except ChessError as e:
    #     print(e)  
    
    # try:
    #     print(next_square("a2",Direction.SOUTHWEST))
    # except ChessError as e:
    #     print(e)
    # try:
    #     print(next_square("c1",Direction.SOUTHWEST))
    # except ChessError as e:
    #     print(e)

        
    # try:
    #     print(next_square("h3",Direction.SOUTHEAST))
    # except ChessError as e:
    #     print(e)
    # try:
    #     print(next_square("c1",Direction.SOUTHEAST))
    # except ChessError as e:
    #     print(e)        

    # try:
    #     print(next_square("a5",Direction.NORTHWEST))
    # except ChessError as e:
    #     print(e)
    # try:
    #     print(next_square("d8",Direction.NORTHWEST))
    # except ChessError as e:
    #     print(e)    
    
        
    # try:
    #     print(next_square("a8","N"))
    # except ChessError as e : 
    #     print("Donr do this ", e) 
    # 

    # test1()
        
    # test2()


    # print("\u2655")
    # arr = ["\u2659"]
    # for a in arr :
    #     print(a)

    # print(find_piece_in_pos(b, "A1"))
    # print(find_piece_in_pos(b, "B1"))
    # print(find_piece_in_pos(b, "C1"))

    # print(f"{WHITE_BG} {PIECE} {RESET}")
    # White pawn at D2 (starting position)

    test_check_mate_2_rooks()