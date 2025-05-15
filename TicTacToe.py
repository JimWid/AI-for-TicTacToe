
class TicTacToe:
    def __init__(self):
        # Creating Board
        self.board = ["-", "-", "-", 
                      "-", "-", "-",
                      "-", "-", "-"]
        
        # Initializing Winner as None
        self.current_winner = None

    # Displays The Board
    def display_board(self):
        print(self.board[0] + " | " + self.board[1] + " | " + self.board[2])
        print(self.board[3] + " | " + self.board[4] + " | " + self.board[5])
        print(self.board[6] + " | " + self.board[7] + " | " + self.board[8])

    # Gets any Empty Cells
    def get_empty_cells(self):
        return [i for i, cell in enumerate(self.board) if cell == '-']

    # Checks if move is valid
    def is_valid_move(self, position):
        if 0 <= position < 9 and self.board[position] == "-":
            return True
        return False

    # Makes the move
    def make_move(self, position, player_mark):
        if self.is_valid_move(position):
            self.board[position] = player_mark

            if self.check_win(player_mark):
                self.current_winner = player_mark
            return True
        return False

    # Checks if there is a win
    def check_win(self, player_mark):
        if self.check_rows(player_mark) == True:
            return True
        if self.check_columns(player_mark) == True:
            return True
        if self.check_diagonals(player_mark) == True:
            return True
        
        return False
    
    # Checks if there is a Tie
    def check_if_tie(self):

        if not self.current_winner and not self.get_empty_cells():
            return True
        return False
        
        #if "-" not in self.board:
        #   return True

    # Checks if rows are complete
    def check_rows(self, player_mark):
        row_1 = self.board[0] == self.board[1] == self.board[2] == player_mark != "-"
        row_2 = self.board[3] == self.board[4] == self.board[5] == player_mark != "-"
        row_3 = self.board[6] == self.board[7] == self.board[8] == player_mark != "-"

        if row_1 or row_2 or row_3:
            return True
        else:
            return False

    # Checks if any columns are complete
    def check_columns(self, player_mark):
        column_1 = self.board[0] == self.board[3] == self.board[6] == player_mark != "-"
        column_2 = self.board[1] == self.board[4] == self.board[7] == player_mark != "-"
        column_3 = self.board[2] == self.board[5] == self.board[8] == player_mark != "-"

        if column_1 or column_2 or column_3:
            return True
        else:
            return False

    # Checking if any Diagonals are Complete
    def check_diagonals(self, player_mark):
        diagonal_1 = self.board[0] == self.board[4] == self.board[8] == player_mark != "-"
        diagonal_2 = self.board[6] == self.board[4] == self.board[2] == player_mark != "-"

        if diagonal_1 or diagonal_2:
            return True
        else:
            return False

    # Checks if there is winner or a Tie
    def is_game_over(self):
        return self.current_winner is not None or self.check_if_tie()

    # Resets the Board for new game
    def reset_board(self):
        self.board = ["-", "-", "-", 
                      "-", "-", "-",
                      "-", "-", "-"]
        self.current_winner = None

    def get_board_state_tuple(self):
        return tuple(tuple(row for row in self.board))
