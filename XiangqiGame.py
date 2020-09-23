"""
Author: Madison Woy
Date: 3/10/2020
Description: Program that contains a class called Xiangqigame that a user can use to play a game of Chinese chess

"""



"""
___________________________________________________________________________________________________________________
The following are helper functions that are used by all classes, they are placed here to clean up the classes themselves
___________________________________________________________________________________________________________________
"""


def get_direction_col(col_from_num, col_to_num):
    """
    sets the column direction in regards to the numeric value of the column change
    :return: direction_col ("inc" if col increased, "dec" if decreased and "None" if no change)
    """
    if col_from_num > col_to_num:
        direction_col = "dec"
        return direction_col
    if col_from_num < col_to_num:
        direction_col = "inc"
        return direction_col
    if col_to_num == col_from_num:
        direction_col = None
        return direction_col


def get_direction_row(row_from_num, row_to_num):
    """
    sets the direction in terms of the value of the row
    :return: direction_row ("inc" if row increased, "dec" if decreased and "None" if no change)
    """
    if row_from_num > row_to_num:
        direction_row = "dec"
        return direction_row
    if row_from_num < row_to_num:
        direction_row = "inc"
        return direction_row
    if row_to_num == row_from_num:
        direction_row = None
        return direction_row


def get_num_moves(direction_col, direction_row, col_to_num, col_from_num, row_from_num, row_to_num, num_moves=0):
    """
    returns the number of spaces moved between two squares
    *** can be specified directionally by passing "None" as an argument for direction
    :return: number of moves between from and to square
    """
    if direction_col is not None:
        num_moves = col_from_num - col_to_num
    if direction_row is not None:
        num_moves = row_from_num - row_to_num
    if num_moves < 0:
        num_moves = num_moves * -1
    return num_moves


def get_game_piece_from_num(col, row, board):
    """
    returns the piece at a numeric location
    :board: board to find piece on, allows this function to be used outside classes
    :return: piece object
    """
    return board[row][col]


def get_col_num(square):
    """
    converts a alphabet input to index output
    :param square: user defined square to move fro
    :return: col_num
    """
    col_let = square[0].upper()
    column_ref_let = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

    # find the index that matches the letter in the list above and return the index as the col number
    for x in range(9):
        if column_ref_let[x] == col_let:
            col_num = x
            return col_num

    # if the letter is not in the list above the input is invalid
    return False


def find_general(color, board, col_or_row):
    """
    helper function to find the row of the general with the given color
    :param col_or_row: specifies whether to return the col or row of the general
    :param color: general to find
    :param board: board to find on
    :return: row of general
    """

    # search all squares
    for row in range(10):
        for col in range(9):

            # when the piece in a square is a general of the color specified, return the row or col
            search_piece = get_game_piece_from_num(col, row, board)
            if search_piece != "  ":
                if vars(search_piece) == vars(General(color)) and col_or_row == 'row':
                    return row
                if vars(search_piece) == vars(General(color)) and col_or_row == 'col':
                    return col


"""
___________________________________________________________________________________________________________________
The following are classes for the game pieces 
___________________________________________________________________________________________________________________
"""


class Piece:
    """
    class that all game pieces draw attributes from
    """

    def __init__(self, color, abbreviation):
        """
        initiates class
        :param color: color of piece
        :param abbreviation: abbreviation for printing the board
        """
        self._color = color
        self._abbreviation = abbreviation

    def __str__(self):
        """
        allows for easy printing of board
        :return: 3 letter text representation of pieces
        """
        if self._color == 'black':
            color = "B"
        if self._color == 'red':
            color = "R"
        return color + str(self._abbreviation) + " "

    def get_color(self):
        """
        color of the piece
        :return: color
        """
        return self._color

    __repr__ = __str__


"""---------------------------------------------ELEPHANT-------------------------------------------------------------"""


class Elephant(Piece):
    """
    Represents a game piece, legal moves describes in legal_move function
    """

    def __init__(self, color, abbreviation="EL"):
        """
        initiates class, parent class is Piece
        """
        super().__init__(color, abbreviation)

    def legal_move(self, from_piece, row_from_num, row_to_num, col_from_num, col_to_num, current_board):
        """
        Elephant: cannot cross the river, cannot jump, moves 2 diagonally
        :return: TRUE if the move is legal
        """

        # get the direction of the row and col movement
        direction_row = get_direction_row(row_from_num, row_to_num)
        direction_col = get_direction_col(col_from_num, col_to_num)

        # check for row and column legality by ensuring that the row and col to be moved to is exactly 2 away
        if (row_from_num + 2 != row_to_num and row_from_num - 2 != row_to_num) or (
                col_from_num + 2 != col_to_num and col_from_num - 2 != col_to_num):
            return False

        # check for crossing the river
        if (from_piece.get_color == 'black' and row_to_num < 5) or (from_piece.get_color == 'red' and row_to_num > 4):
            return False

        # check for no jumps by ensuring that the space between from square and to square is clear
        if direction_row == "inc" and direction_col == "inc":
            jump_row = row_from_num + 1
            jump_col = col_from_num + 1
            if get_game_piece_from_num(jump_col, jump_row, current_board) != "  ":
                return False
        if direction_row == "inc" and direction_col == "dec":
            jump_row = row_from_num + 1
            jump_col = col_from_num - 1
            if get_game_piece_from_num(jump_col, jump_row, current_board) != "  ":
                return False
        if direction_row == "dec" and direction_col == "dec":
            jump_row = row_from_num - 1
            jump_col = col_from_num - 1
            if get_game_piece_from_num(jump_col, jump_row, current_board) != "  ":
                return False
        if direction_row == "dec" and direction_col == "inc":
            jump_row = row_from_num - 1
            jump_col = col_from_num + 1
            if get_game_piece_from_num(jump_col, jump_row, current_board) != "  ":
                return False

        # if the piece method has made it to here then the move is legal and the function returns True
        return True


"""---------------------------------------------CHARIOT-------------------------------------------------------------"""


class Chariot(Piece):
    """
    Represents a game piece, legal moves describes in legal_move function
    """

    def __init__(self, color, abbreviation="CH"):
        """
        initiates class, parent class is Piece
        """
        super().__init__(color, abbreviation)

    def legal_move(self, from_piece, row_from_num, row_to_num, col_from_num, col_to_num, current_board):
        """
        Chariot: cannot jump, moves any distance orthogonally (horizontal or vertical)
        :return: TRUE if the move is legal False if move is illegal
        """

        # get the direction of col and row movement
        direction_row = get_direction_row(row_from_num, row_to_num)
        direction_col = get_direction_col(col_from_num, col_to_num)

        # check that piece is moving orthogonally by ensuring that either the row or the column stay the same
        if direction_row is not None and direction_col is not None:
            return False

        # find the number of spaces to be moved
        num_moves = get_num_moves(direction_col, direction_row, col_to_num, col_from_num, row_from_num, row_to_num)

        # takes direction and ensures that all spaces are empty between to and from squares
        # special range to skip pass [0] (not empty by default (from)) and the to square (may be filled (capture))
        for x in [i for i in range(num_moves) if i != 0 and i != range(num_moves)]:
            if direction_row == "inc":
                jump_row = row_from_num + x
                if get_game_piece_from_num(col_from_num, jump_row, current_board) != "  ":
                    return False
            if direction_row == "dec":
                jump_row = row_from_num - x
                if get_game_piece_from_num(col_from_num, jump_row, current_board) != "  ":
                    return False
            if direction_col == "inc":
                jump_col = col_from_num + x
                if get_game_piece_from_num(jump_col, row_from_num, current_board) != "  ":
                    return False
            if direction_col == "dec":
                jump_col = col_from_num - x
                if get_game_piece_from_num(jump_col, row_from_num, current_board) != "  ":
                    return False

        # if the piece method has made it to here then the move is legal and the function returns True
        return True


"""---------------------------------------------GENERAL-------------------------------------------------------------"""


class General(Piece):
    """
    Represents a game piece, legal moves describes in legal_move function
    """

    def __init__(self, color, abbreviation="GE"):
        """
        initiates class, parent class is Piece
        """
        super().__init__(color, abbreviation)

    def legal_move(self, from_piece, row_from_num, row_to_num, col_from_num, col_to_num, current_board):
        """
        General: can move one space orthogonally and cannot leave the castle
        :return: TRUE if the move is legal False if move is illegal
        """

        # check if to_square is out of the castle
        if (self._color == 'black' and row_to_num < 7) or (self._color == 'red' and row_to_num > 2) or (
                col_to_num > 5 or col_to_num < 3):
            return False

        # set directions
        direction_row = get_direction_row(row_from_num, row_to_num)
        direction_col = get_direction_col(col_from_num, col_to_num)

        # make sure moving one space
        num_moves = get_num_moves(direction_col, direction_row, col_to_num, col_from_num, row_from_num, row_to_num)
        if num_moves > 1:
            return False

        # check that piece is moving orthogonally by ensuring that either the row or the column stay the same
        if direction_row is not None and direction_col is not None:
            return False

        # if the piece method has made it to here then the move is legal and the function returns True
        return True


"""---------------------------------------------ADVISOR-------------------------------------------------------------"""


class Advisor(Piece):
    """
    Represents a game piece, legal moves describes in legal_move function
    """

    def __init__(self, color, abbreviation="AD"):
        """
        initiates class, parent class is Piece
        """
        super().__init__(color, abbreviation)

    def legal_move(self, from_piece, row_from_num, row_to_num, col_from_num, col_to_num, current_board):
        """
        Advisor: can move one space diagonally but must stay in the castle
        :return: TRUE if the move is legal False if move is illegal
        """

        # check if to_square is out of the castle
        if (self._color == 'black' and row_to_num < 7) or (self._color == 'red' and row_to_num > 2) or (
                col_to_num > 5 or col_to_num < 3):
            return False

        # set directions
        direction_row = get_direction_row(row_from_num, row_to_num)
        direction_col = get_direction_col(col_from_num, col_to_num)

        # get number of moves in each direction
        num_moves_row = get_num_moves(None, direction_row, col_to_num, col_from_num, row_from_num, row_to_num)
        num_moves_col = get_num_moves(direction_col, None, col_to_num, col_from_num, row_from_num, row_to_num)

        # check that only one space is moved and that the num_moves_row == num_moves_col (moving diagonally)
        if (num_moves_col > 1 or num_moves_row > 1) or (num_moves_row != num_moves_col):
            return False

        # if the piece method has made it to here then the move is legal and the function returns True
        return True


"""---------------------------------------------HORSE-------------------------------------------------------------"""


class Horse(Piece):
    """
    Represents a game piece, legal moves describes in legal_move function
    """

    def __init__(self, color, abbreviation="HO"):
        """
        initiates class, parent class is Piece
        """
        super().__init__(color, abbreviation)

    def legal_move(self, from_piece, row_from_num, row_to_num, col_from_num, col_to_num, current_board):
        """
        Horse: cannot jump, moves one space orthogonally and then one space diagonally
        :return: TRUE if the move is legal False if move is illegal
        """

        # set direction
        direction_row = get_direction_row(row_from_num, row_to_num)
        direction_col = get_direction_col(col_from_num, col_to_num)

        # get num_moves in each direction by passing None as the opposite direction
        num_moves_col = get_num_moves(direction_col, None, col_to_num, col_from_num, row_from_num, row_to_num)
        num_moves_row = get_num_moves(None, direction_row, col_to_num, col_from_num, row_from_num, row_to_num)

        # check that num_moves does not exceed 2 in either direction
        if (num_moves_col > 2 or num_moves_row > 2) or (num_moves_col != 2 and num_moves_row != 2):
            return False

        # check that one num_moves is 1 and the other is 2
        if (num_moves_row == 2 and num_moves_col != 1) or (num_moves_col == 2 and num_moves_row != 1):
            return False

        # establish the direction of the first move
        first_move = None
        if num_moves_row == 2:
            first_move = "row"
        if num_moves_col == 2:
            first_move = "col"

        # check for no jumps, need to ensure that the first_move space is clear
        if first_move == "row":
            if direction_row == "inc" and get_game_piece_from_num(col_from_num, row_from_num + 1,
                                                                  current_board) != "  ":
                return False
            if direction_row == "dec" and get_game_piece_from_num(col_from_num, row_from_num - 1,
                                                                  current_board) != "  ":
                return False
        if first_move == "col":
            if direction_col == "inc" and get_game_piece_from_num(col_from_num + 1, row_from_num,
                                                                  current_board) != "  ":
                return False
            if direction_col == "dec" and get_game_piece_from_num(col_from_num - 1, row_from_num,
                                                                  current_board) != "  ":
                return False

        # if the piece method has made it to here then the move is legal and the function returns True
        return True


"""---------------------------------------------CANNON-------------------------------------------------------------"""


class Cannon(Piece):
    """
    Represents a game piece, legal moves describes in legal_move function
    """

    def __init__(self, color, abbreviation="CA"):
        """
        initiates class, parent class is Piece
        """
        super().__init__(color, abbreviation)

    def legal_move(self, from_piece, row_from_num, row_to_num, col_from_num, col_to_num, current_board):
        """
        Cannon: MUST jump at least one piece if capturing, otherwise cannot jump
            - moves any distance orthogonally (horizontal or vertical)
        :return: TRUE if the move is legal False if move is illegal
        """

        # get the direction of the row and col movement
        direction_row = get_direction_row(row_from_num, row_to_num)
        direction_col = get_direction_col(col_from_num, col_to_num)

        # check that piece is moving orthogonally by ensuring that either the row or the column stay the same
        if direction_row is not None and direction_col is not None:
            return False

        # find the number of spaces to be moved
        num_moves = get_num_moves(direction_col, direction_row, col_to_num, col_from_num, row_from_num, row_to_num)

        # check if this move results in a capture
        capture_move = False
        to_piece = get_game_piece_from_num(col_to_num, row_to_num, current_board)
        if to_piece != "  ":
            capture_move = True

        # takes direction and counts jumps made between from and to square
        # special range to skip pass [0] (not empty by default (from)) and the to square (may be filled (capture))
        jump_count = 0
        for x in [i for i in range(num_moves) if i != 0 and i != range(num_moves)]:
            if direction_row == "inc":
                jump_row = row_from_num + x
                if get_game_piece_from_num(col_from_num, jump_row, current_board) != "  ":
                    jump_count += 1
            if direction_row == "dec":
                jump_row = row_from_num - x
                if get_game_piece_from_num(col_from_num, jump_row, current_board) != "  ":
                    jump_count += 1
            if direction_col == "inc":
                jump_col = col_from_num + x
                if get_game_piece_from_num(jump_col, row_from_num, current_board) != "  ":
                    jump_count += 1
            if direction_col == "dec":
                jump_col = col_from_num - x
                if get_game_piece_from_num(jump_col, row_from_num, current_board) != "  ":
                    jump_count += 1

        # if not a capture move and jump count is zero OR is a capture move and jump count is 1 move is legal
        if jump_count == 0 and capture_move is False or (jump_count == 1 and capture_move is True):
            return True
        else:
            return False


"""---------------------------------------------SOLDIER-------------------------------------------------------------"""


class Soldier(Piece):
    """
    Represents a game piece, legal moves describes in legal_move function
    """

    def __init__(self, color, abbreviation="SO"):
        """
        initiates class, parent class is Piece
        """
        super().__init__(color, abbreviation)

    def legal_move(self, from_piece, row_from_num, row_to_num, col_from_num, col_to_num, current_board):
        """
        can only move forward unless they pas the river at which point they can move horizontally
        :return: TRUE if the move is legal False if move is illegal
        """

        # get the direction of col and row movement
        direction_row = get_direction_row(row_from_num, row_to_num)
        direction_col = get_direction_col(col_from_num, col_to_num)

        # only moves forward, red has to decrease in rows and black has to decrease
        if from_piece.get_color() == 'red' and direction_row == "dec":
            return False
        if from_piece.get_color() == 'black' and direction_row == "inc":
            return False

        # get num_moves in each direction
        num_moves_col = get_num_moves(direction_col, None, col_to_num, col_from_num, row_from_num, row_to_num)
        num_moves_row = get_num_moves(None, direction_row, col_to_num, col_from_num, row_from_num, row_to_num)

        # check if soldier only advances one space in one direction
        if num_moves_col > 1 or num_moves_row > 1 or (num_moves_col > 0 and num_moves_row > 0):
            return False

        # check if soldier crossed the river
        river_passed = None
        if from_piece.get_color() == 'black' and row_from_num <= 4:
            river_passed = True
        if from_piece.get_color() == 'red' and row_from_num >= 5:
            river_passed = True

        # check for no horizontal movement before crossing the river
        if river_passed is None and direction_col is not None:
            return False

        # if the piece method has made it to here then the move is legal and the function returns True
        return True


"""
___________________________________________________________________________________________________________________
The following code contains the game class
___________________________________________________________________________________________________________________
"""


class XiangqiGame:
    """
    class that represents a game of chinese chess
    """

    def __init__(self, game_state="UNFINISHED", board=None, black_check=None, red_check=None, turn='red'):
        """
        initializes a game with the starting pieces
        :param game_state: can be "UNFINISHED", "RED_WON" or "BLACK_WON"
        :param board: list of lists that comprises the board
        :param black_check: True is black is in check, false otherwise
        :param red_check: True if red is in check, False otherwise
        :param turn: which colors turn it currently is
        """

        # initialize board as a list of lists
        if board is None:
            board = [[], [], [], [], [], [], [], [], [], []]

        # initialize attributes
        self._game_state = game_state
        self._black_check = black_check
        self._red_check = red_check
        self._board = board
        self._turn = turn

        # initialize pieces on the board
        self.start_state()

    """---------------------------------------------HELPER METHODS---------------------------------------------------"""

    def start_state(self):
        """
        initializes game pieces
        :return: a starting board
        """
        self._board[0] = [Chariot('red'), Horse('red'), Elephant('red'), Advisor('red'), General('red'), Advisor('red'),
                          Elephant('red'), Horse('red'), Chariot('red')]
        self._board[1] = ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]
        self._board[2] = ["  ", Cannon('red'), "  ", "  ", "  ", "  ", "  ", Cannon('red'), "  "]
        self._board[3] = [Soldier('red'), "  ", Soldier('red'), "  ", Soldier('red'), "  ", Soldier('red'), "  ",
                          Soldier('red')]
        self._board[4] = ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]
        self._board[5] = ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]
        self._board[6] = [Soldier('black'), "  ", Soldier('black'), "  ", Soldier('black'), "  ", Soldier('black'),
                          "  ", Soldier('black')]
        self._board[7] = ["  ", Cannon('black'), "  ", "  ", "  ", "  ", "  ", Cannon('black'), "  "]
        self._board[8] = ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]
        self._board[9] = [Chariot('black'), Horse('black'), Elephant('black'), Advisor('black'), General('black'),
                          Advisor('black'), Elephant('black'), Horse('black'), Chariot('black')]

    def print_board(self, board=None):
        """
        prints board for self check
        """
        if board is None:
            for x in range(10):
                print(self._board[x])
        else:
            for x in range(10):
                print(board[x])

    def make_board_copy(self):
        """
        makes a copy of the current board to test moves on
        :return:
        """

        # initialize new board
        board_copy = [[], [], [], [], [], [], [], [], [], []]

        # fill each row of new board with rows from real board
        for x in range(10):
            board_copy[x] = list(self._board[x])

        return board_copy

    def update_board(self, from_piece, row_from_num, row_to_num, col_from_num, col_to_num, board=None):
        """
        updates the board with the proposed move
        :param board: if None the move is performed on the real board, if not it is performed on a temp board
        :return: a board with the proposed move executed
        """
        if board is None:
            self._board[row_from_num][col_from_num] = "  "
            self._board[row_to_num][col_to_num] = from_piece
            return
        else:
            board[row_from_num][col_from_num] = "  "
            board[row_to_num][col_to_num] = from_piece
            return board

    def get_game_piece_at_square(self, square):
        """
        find the piece at a specified square
        :return: piece
        """

        # convert the square to numeric values for row and col
        col_square = get_col_num(square)
        row_square = int(square[1:]) - 1

        # return the piece at that square
        return self._board[row_square][col_square]

    """---------------------------------------------GET METHODS------------------------------------------------------"""

    def get_game_state(self):
        """
        Determines the state of the game, changed during make_move
        :return: UNFINISHED, RED_WON, BLACK_WON
        """
        return self._game_state

    def is_in_check(self, color):
        """
        Checks if the color's general is currently in check
        :param color: color to be checked
        :return: TRUE or FALSE
        """
        if color == 'black' and self._black_check is True:
            return True
        if color == 'red' and self._red_check is True:
            return True
        else:
            return False

    """---------------------------------------------CHECK METHODS----------------------------------------------------"""

    def general_can_see(self, from_piece, row_from_num, row_to_num, col_from_num, col_to_num):
        """
        checks if generals can see each other after a move is performed
        *** Generals can only see each other via columns so no need to check changes in cols
        :return: True if the general can see, False if not
        """

        # make a copy of the board and then make proposed move
        temp_board = self.make_board_copy()
        temp_board = self.update_board(from_piece, row_from_num, row_to_num, col_from_num, col_to_num, temp_board)

        # find the locations of the generals
        col_black_general = find_general('black', temp_board, 'col')
        row_black_general = find_general('black', temp_board, 'row')
        col_red_general = find_general('red', temp_board, 'col')
        row_red_general = find_general('red', temp_board, 'row')

        # find spaces between by measuring from red general to black general
        spaces_bw_gens = get_num_moves(None, "inc", col_black_general, col_red_general, row_black_general,
                                       row_red_general)

        # generals cannot see each other if they are in different rows
        if col_red_general != col_black_general:
            return False

        # check if path is clear between generals, if it is return False
        for x in [i for i in range(spaces_bw_gens) if i != 0 and i != range(spaces_bw_gens)]:
            row_to_check = row_red_general + x
            if get_game_piece_from_num(col_red_general, row_to_check, temp_board) != "  ":
                return False

        # if the method has made it to here then if the proposed move is performed the generals will see eachother
        return True

    def checkmate_check(self, color_to_check):
        """
        checks for a checkmate state on the color AFTER a move is made (if red just moved, black is checked)
        checkmate occurs when the from_piece (the piece that is being moved) makes a move such that the opposite color
        cannot make any legal moves to save the general
            - This check happens after the board has been updated (the proposed move that led here was legal)
        :col_to_check: color of the general that may be in checkmate
        :return: True if the general is in checkmate, False if not. also updates the game_state
        """

        li_of_cols = []  # list to store cols that contain pieces of color_to_check
        li_of_rows = []  # list to store rows that contain pieces of color_to_check
        num_of_pieces = 0  # num of color_to_check pieces

        # for loops search entire board and creates a list of cols and rows of all the colors pieces
        for row in range(10):
            for col in range(9):
                if get_game_piece_from_num(col, row, self._board) != "  ":
                    cur_piece = get_game_piece_from_num(col, row, self._board)
                    if cur_piece.get_color() == color_to_check:
                        li_of_cols.append(col)
                        li_of_rows.append(row)
                        num_of_pieces += 1

        # calls recursive helper
        return self.checkmate_helper(li_of_rows, li_of_cols, 0, num_of_pieces)

    def checkmate_helper(self, li_of_rows, li_of_cols, pos, num_of_pieces):
        """
        recursively checks if the color checked in checkmate_check has any legal moves
        :param li_of_rows: list of rows that contain pieces to try and move
        :param li_of_cols: list of cols the contain pieces to try and move
        :param pos: position in lists above (together the lists above make coordinates to check)
        :param num_of_pieces: number fo pieces left to check
        :return: True if a checkmate has occurred, False if the color can still make a legal move
        """

        # base case: if num_pieces reaches 0 then no legal moves can be made and checkmate has occured
        if num_of_pieces == 0:
            return True

        # find the current piece to try and move
        cur_piece = get_game_piece_from_num(li_of_cols[pos], li_of_rows[pos], self._board)

        # try and move that piece to every square on the board
        for row in range(10):
            for col in range(9):

                # find the to_piece and test the legality of the move for the cur_piece
                to_piece = get_game_piece_from_num(col, row, self._board)
                legality_of_move = cur_piece.legal_move(cur_piece, li_of_rows[pos], row, li_of_cols[pos], col,
                                                        self._board)

                # establish if friendly fire has occurred
                friendly_fire = False
                if type(to_piece) is not str:
                    if to_piece.get_color() == cur_piece.get_color():
                        friendly_fire = True

                # check further if the move is legal and there is no friendly fire
                if legality_of_move is True and friendly_fire is False:

                    # check if the move will put the pieces own general in check
                    own_general = self.check_check(cur_piece, li_of_rows[pos], row, li_of_cols[pos], col, "own_general")

                    # check if the generals can see each other
                    general_can_see = self.general_can_see(cur_piece, li_of_rows[pos], row, li_of_cols[pos], col)

                    # if a legal move is found return false because the general can be saved
                    if own_general is False and general_can_see is False:
                        return False

        # if a legal move is not found for cur_piece, move on to the next piece
        return self.checkmate_helper(li_of_rows, li_of_cols, pos + 1, num_of_pieces - 1)

    def check_check(self, from_piece, row_from_num, row_to_num, col_from_num, col_to_num, test_type):
        """
        checks for and updates check status by testing the current move on a temp board and seeing if after the move
        occurs if either of the generals will be in check
        :test_type: allows the function to be used for multiple purposes
            "own_general": checks if the proposed move will put the current turns general in check (illegal move)
                    :return: True if the piece's own general will be in check after the move
            "update_check": updates the check status of the board
            "out_of_check": returns false if the current move does not move the general out of check
        """

        # make a copy of the board and then make proposed move
        temp_board = self.make_board_copy()
        temp_board = self.update_board(from_piece, row_from_num, row_to_num, col_from_num, col_to_num, temp_board)

        # find the locations of the generals
        col_black_general = find_general('black', temp_board, 'col')
        row_black_general = find_general('black', temp_board, 'row')
        col_red_general = find_general('red', temp_board, 'col')
        row_red_general = find_general('red', temp_board, 'row')

        # for loops search entire board for pieces
        for row in range(10):
            for col in range(9):

                # if a game piece is found check if that piece can legally capture the general
                if get_game_piece_from_num(col, row, temp_board) != "  ":
                    cur_piece = get_game_piece_from_num(col, row, temp_board)

                    if cur_piece.get_color() == 'black':

                        # check if the current piece being checked can capture the RED general legally
                        legality = cur_piece.legal_move(cur_piece, row, row_red_general, col, col_red_general,
                                                        temp_board)
                        if test_type == "own_general" and legality is True and from_piece.get_color() == 'red':
                            return True
                        if test_type == "update_check" and legality is True and from_piece.get_color() == 'black':
                            self._red_check = True
                        if test_type == "out_of_check" and legality is True and from_piece.get_color() == 'red':
                            return False

                    if cur_piece.get_color() == 'red':

                        # check if the current piece being checked can capture the BLACK general legally
                        legality = cur_piece.legal_move(cur_piece, row, row_black_general, col, col_black_general,
                                                        temp_board)
                        if test_type == "own_general" and legality is True and from_piece.get_color() == 'black':
                            return True
                        if test_type == "update_check" and legality is True and from_piece.get_color() == 'red':
                            self._black_check = True
                        if test_type == "out_of_check" and legality is True and from_piece.get_color() == 'black':
                            return False

        # if test makes it to here then there is no threat to the general and any check status can be reversed
        if test_type == "out_of_check" and from_piece.get_color() == 'black':
            self._black_check = False
        if test_type == "out_of_check" and from_piece.get_color() == 'red':
            self._red_check = False

        # if test got to this point then the move does not put the own general in check
        if test_type == "own_general":
            return False

    """---------------------------------------------MOVE METHOD------------------------------------------------------"""

    def make_move(self, sq_from, sq_to):
        """
        makes legal moves when game is unfinished
        :param sq_from: square to move from
        :param sq_to: square to move to
        :return: false if move is illegal or game has already been won, makes move otherwise
        """

        # assign numeric value to col from letter and ensures letter is in range
        col_to_num = get_col_num(sq_to)
        col_from_num = get_col_num(sq_from)
        if col_from_num is False or col_to_num is False:
            return False

        # assign correct numeric value to row
        row_from_num = int(sq_from[1:]) - 1
        row_to_num = int(sq_to[1:]) - 1

        # check to see if given squares are valid
        if row_from_num > 9 or col_to_num > 8 or row_to_num > 9 or col_from_num > 8 or sq_to == sq_from:
            return False

        # get the game pieces
        from_piece = self.get_game_piece_at_square(sq_from)
        to_piece = self.get_game_piece_at_square(sq_to)

        # check that sq_from is not blank, that the game is unfinished and the correct turn is taking place
        if (type(from_piece) is str) or (self._game_state != "UNFINISHED") or (from_piece.get_color() != self._turn):
            return False

        # check for friendly fire
        if type(to_piece) != str:
            if from_piece.get_color() == to_piece.get_color():
                return False

        # establish legality of move for the specific game piece
        legality_of_move = from_piece.legal_move(from_piece, row_from_num, row_to_num, col_from_num, col_to_num,
                                                 self._board)

        # establish if move will allow general to see the other
        general_sees_other = self.general_can_see(from_piece, row_from_num, row_to_num, col_from_num, col_to_num)

        # establish if the move will put the pieces own general in check
        own_general_in_check = self.check_check(from_piece, row_from_num, row_to_num, col_from_num, col_to_num,
                                                "own_general")

        # check for legality, general sight, and if the move ill put the general in check
        if own_general_in_check is True or general_sees_other is True or legality_of_move is False:
            return False

        # if general is in check, ensure that this move will bring them out of it
        if self.is_in_check(from_piece.get_color()) is True:
            out_of_check = self.check_check(from_piece, row_from_num, row_to_num, col_from_num, col_to_num,
                                            "out_of_check")
            if out_of_check is False:
                return False

        # if move is legal then make the move and change whose turn it is
        if legality_of_move is True:

            # update check status
            self.check_check(from_piece, row_from_num, row_to_num, col_from_num, col_to_num, "update_check")

            # make the move
            self.update_board(from_piece, row_from_num, row_to_num, col_from_num, col_to_num)

            # update turn
            if from_piece.get_color() == 'black':
                self._turn = 'red'
            if from_piece.get_color() == 'red':
                self._turn = 'black'

            # check for checkmate
            checkmate = self.checkmate_check(self._turn)
            if checkmate is True:
                if self._turn == 'black':
                    self._game_state = 'RED_WON'
                if self._turn == 'red':
                    self._game_state = 'BLACK_WON'

            # move complete
            return True
