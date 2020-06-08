import time
from itertools import product
from sys import maxsize
from copy import deepcopy


class Player:
    def __init__(self, is_human, is_max=False):
        self.is_human = is_human
        self.is_max = is_max

    def all_legal_moves(self, board):
        if self.is_max:
            return board.all_odd_moves
        else:
            return board.all_even_moves

    def all_legal_move_locations(self, board):
        if self.is_max:
            return set([move[0] for move in board.all_odd_moves])
        else:
            return set([move[0] for move in board.all_even_moves])

    def all_legal_move_values(self, board):
        if self.is_max:
            return set([move[1] for move in board.all_odd_moves])
        else:
            return set([move[1] for move in board.all_even_moves])

    @staticmethod
    def perform_move(move_location, move_value, board):
        b = deepcopy(board)
        b.board[move_location] = move_value
        return b

    def get_move(self, board):
        if self.is_human:
            return self.get_move_from_user(board)
        else:
            move = iterative_deepening_alphabeta(board)
            return move

    def get_move_from_user(self, board):
        while True:
            try:
                move_location = int(input('Enter move location {}: '.format(self.all_legal_move_locations(board))))
                if move_location not in self.all_legal_move_locations(board):
                    print('Not a valid move location')
                else:
                    break
            except ValueError:
                print('Not a valid move location')

        while True:
            try:
                move_value = int(input('Enter move value {}: '.format(self.all_legal_move_values(board))))
                if move_value not in self.all_legal_move_values(board):
                    print('Not a valid move value')
                else:
                    break
            except ValueError:
                print('Not a valid move location')

        return move_location, move_value

    def print_all_legal_moves(self, board):
        print('All moves:')
        for i, move in enumerate(self.all_legal_moves(board)):
            if i % 5 == 0 and i != 0:
                print()
            print('{} '.format(move), end='')
        print()


class Board:
    def __init__(self, length=3):
        self.length = length
        self.board = [0 for _ in range(pow(self.length, 2))]
        self.num_columns = self.num_rows = int(self.length)
        self.all_numbers = range(1, len(self.board) + 1)
        self.winning_sum = int(sum(self.all_numbers) / self.length)

    def __str__(self):
        out = ''
        for i, val in enumerate(self.board):
            out += '{:2} '.format(val)
            if ((i + 1) % self.num_columns) == 0:
                out += '\n'
        return out

    @property
    def has_winning_sum(self):
        winning_sums = [
            self.row_has_winning_sum,
            self.column_has_winning_sum,
            self.diagonal_has_winning_sum
        ]
        return any(winning_sums)

    @property
    def rows(self):
        rows = []
        for i in range(self.num_columns):
            start_idx = i * self.num_columns
            end_idx = start_idx + self.num_columns
            rows.append(self.board[start_idx:end_idx])
        return rows

    @property
    def columns(self):
        columns = []
        for i in range(self.num_rows):
            column = self.board[i::self.num_rows]
            columns.append(column)
        return columns

    @property
    def row_has_winning_sum(self):
        for row in self.rows:
            row = [val for val in row if val != 0]
            if sum(row) == self.winning_sum and len(row) == self.length:
                return True
        return False

    @property
    def column_has_winning_sum(self):
        for column in self.columns:
            column = [val for val in column if val != 0]
            if sum(column) == self.winning_sum and len(column) == self.length:
                return True
        return False

    @property
    def major_diagonal(self):
        return self.board[::self.num_columns + 1]

    @property
    def minor_diagonal(self):
        last_idx_of_first_row = self.num_columns - 1
        first_idx_of_last_row = len(self.board) - self.num_columns
        return self.board[last_idx_of_first_row:first_idx_of_last_row + 1:self.num_columns - 1]

    @property
    def diagonals(self):
        return [self.major_diagonal, self.minor_diagonal]

    @property
    def diagonal_has_winning_sum(self):
        for diagonal in self.diagonals:
            diagonal = [val for val in diagonal if val != 0]
            if sum(diagonal) == self.winning_sum and len(diagonal) == 3:
                return True
        return False

    @property
    def is_maxes_turn(self):
        even, odd = self.count_even_odd(self.board)
        if even == odd:
            return True
        else:
            return False

    @staticmethod
    def count_even_odd(vector):
        even_cnt = odd_cnt = 0
        for val in vector:
            if val == 0:
                continue
            if val % 2 == 0:
                even_cnt += 1
            else:
                odd_cnt += 1
        return even_cnt, odd_cnt

    @property
    def all_possible_move_locations(self):
        return [i for i, val in enumerate(self.board) if val == 0]

    @property
    def all_possible_move_values(self):
        used_values = [val for val in self.board if val != 0]
        return [val for val in self.all_numbers if val not in used_values]

    @property
    def all_possible_moves(self):
        return product(self.all_possible_move_locations, self.all_possible_move_values)

    @property
    def all_odd_moves(self):
        return [move for move in self.all_possible_moves if move[1] % 2 == 1]

    @property
    def all_even_moves(self):
        return [move for move in self.all_possible_moves if move[1] % 2 == 0]

    @property
    def utility(self):
        if self.has_winning_sum:
            return 100
        else:
            return 0

    def equal_even_odd(self, vector):
        even, odd = self.count_even_odd(vector)
        if even == odd:
            return True
        else:
            return False

class Game:
    @staticmethod
    def actions(state):
        if state.is_maxes_turn:
            return state.all_odd_moves
        else:
            return state.all_even_moves

    @staticmethod
    def result(state, move):
        if move is None:
            print('empty move')
        location, value = move[0], move[1]
        board = deepcopy(state)
        board.board[location] = value
        return board

    @staticmethod
    def utility(state, player):
        if player == 'MAX':
            return state.utility
        else:
            return -state.utility

    @staticmethod
    def is_terminal(state):
        num_moves = 0
        if state.is_maxes_turn:
            num_moves = len(state.all_odd_moves)
        else:
            num_moves = len(state.all_even_moves)

        return state.has_winning_sum or num_moves == 0

    @staticmethod
    def to_move(state):
        if state.is_maxes_turn:
            return 'MAX'
        else:
            return 'MIN'

    @staticmethod
    def display(state):
        print(state)

class TimeoutReached(Exception):
    pass
    

def evalfn(board):
    score = 0
    vectors = board.rows + board.columns + board.diagonals

    maxes_turn = board.is_maxes_turn

    for v in vectors:

        even, odd = board.count_even_odd(v)

        if even == 2 and odd == 1:
            if maxes_turn:
                score += 10
            else:
                score -= 10

        if odd == 3 and even == 0:
            if maxes_turn:
                score += 10

        if even == 3 and odd == 0:
            if not maxes_turn:
                score -= 10

        if 0 < even < 3:
            score += 3

        if even == 1 and maxes_turn:
            score += 3

        if even == 1 and odd == 1 and maxes_turn:
            score -= 7

    return score    

infinity = float('inf')

def iterative_deepening_alphabeta(state):
    game = Game
    start_time = time.time()

    best_action = None
    best_score = -infinity

    for depth in range(0, maxsize):
        try:
            best_action, best_score = alphabeta_cutoff_search(state, game, start_time, depth, eval_fn=evalfn)
        except TimeoutReached:
            print('Timeout reached')
            break

    print('Depth: {}, Best move: {}, Best score: {}'.format(depth-1, best_action, best_score))
    return best_action


def alphabeta_cutoff_search(state, game, start_time, d, reached_cutoff=None, eval_fn=None):
    TIMEOUT = 2

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if (time.time() - start_time) >= TIMEOUT:
            raise TimeoutReached('Timeout reached')
        if game.is_terminal(state):
            return game.utility(state, player)
        elif reached_cutoff(depth):
            return eval_fn(state)

        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if (time.time() - start_time) >= TIMEOUT:
            raise TimeoutReached('Timeout reached')
        if game.is_terminal(state):
            return game.utility(state, player)
        elif reached_cutoff(depth):
            return eval_fn(state)

        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    reached_cutoff = (reached_cutoff or
                      (lambda depth: depth > d))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a

    return best_action, best_score

def main():
    human_vs_ai = prompt_user_for_game_type()

    if human_vs_ai:
        human_player_first = 1
        players = create_players(human_player_first)
    else:
        players = [Player(is_human=0, is_max=1), Player(is_human=0, is_max=0)]

    max_, min_ = get_max_and_min(players)
    board = Board(3)

    print(board)

    while True:
        max_move = max_.get_move(board)
        board = max_.perform_move(*max_move, board)
        print(board)
        if board.has_winning_sum:
            print('Player Odds wins!')
            break
        if len(list(board.all_possible_moves)) == 0:
            print('Draw!')
            break
        if not human_vs_ai:
            input('Press enter to continue...')

        min_move = min_.get_move(board)
        board = min_.perform_move(*min_move, board)
        print(board)
        if board.has_winning_sum:
            print('Player Even wins!')
            break
        if len(list(board.all_possible_moves)) == 0:
            print('Draw!')
            break
        if not human_vs_ai:
            input('Press enter to continue...')


def prompt_user_for_game_type():
    human_vs_ai = -1

    while human_vs_ai < 0:
        human_vs_ai = input('Level up (play against optimiser) [Y/n]?:').lower()
        if human_vs_ai == '' or human_vs_ai == 'y':
            human_vs_ai = 1
        elif human_vs_ai == 'n':
            human_vs_ai = 0

    return human_vs_ai

def create_players(human_player_first):
    if human_player_first == 1:
        human_player = Player(is_human=1, is_max=1)
        ai_player = Player(is_human=0, is_max=0)
    else:
        human_player = Player(is_human=1, is_max=0)
        ai_player = Player(is_human=0, is_max=1)

    return [human_player, ai_player]


def get_max_and_min(players):
    max_ = min_ = None
    for player in players:
        if player.is_max:
            max_ = player
        else:
            min_ = player
    return max_, min_


if __name__ == '__main__':
    main()
