from copy import deepcopy
import random

class Board:
    # Constants
    BOARD_SIZE_I = 6
    BOARD_SIZE_J = 7

    def __init__(self):
        self.matrix = [[0 for col in range(self.BOARD_SIZE_J)] for row in range(self.BOARD_SIZE_I)]

    def play(self, player, slot):
        if player != 1 and player != 2:
            raise AttributeError("Player is not valid.")
        if slot < 0 or slot > self.BOARD_SIZE_J:
            raise AttributeError("Slot is not valid.")
        top = 0
        while top < self.BOARD_SIZE_I and self.matrix[top][slot] == 0:
            top += 1
        if top == 0:
            raise AttributeError("Can't insert chip into that slot")
        self.matrix[top-1][slot] = player

    def print(self, print_function, use_emoji=False):
        if use_emoji:
            print("\u0030\uFE0F\u20E3  \u0031\uFE0F\u20E3  \u0032\uFE0F\u20E3  \u0033\uFE0F\u20E3  \u0034\uFE0F\u20E3  \u0035\uFE0F\u20E3  \u0036\uFE0F\u20E3")
        else:
            print("0 1 2 3 4 5 6")
            print("-------------")
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if (use_emoji):
                    char = '\U000026AB'
                    if self.matrix[i][j] == 1:
                        char = '\U0001F534'
                    elif self.matrix[i][j] == 2:
                        char = '\U0001F535'
                else:
                    char = "{}".format(self.matrix[i][j])
                print_function(char, end=" ")
            print_function()
    
    def is_full(self):
        full = True
        for j in range(self.BOARD_SIZE_J):
            full = full and self.matrix[0][j]!=0
            if full == False:
                break
        return full

class AI:
    EXP_LINE_WEIGHT = 5

    def player_score(self, board, player):
        if player == 1:
            rival = 2
        else:
            rival = 1
        score = 0
        for i in range(len(board.matrix)):
            for j in range(len(board.matrix[i])):
                if board.matrix[i][j] == player:
                    # Horizontal
                    a = i+1
                    b = j
                    tmp_score = 0
                    while (a < board.BOARD_SIZE_I and a <= i+3):
                        if board.matrix[a][b] == player:
                            tmp_score += 1
                        elif board.matrix[a][b] == rival:
                            tmp_score = 0
                            break
                        a += 1
                    tmp_score **= self.EXP_LINE_WEIGHT
                    score += tmp_score
                    # Vertical
                    a = i
                    b = j+1
                    tmp_score = 0
                    while (b < board.BOARD_SIZE_J and b <= j+3):
                        if board.matrix[a][b] == player:
                            tmp_score += 1
                        elif board.matrix[a][b] == rival:
                            tmp_score = 0
                            break
                        b += 1
                    tmp_score **= self.EXP_LINE_WEIGHT
                    score += tmp_score
                    # Lower diagonal
                    a = i+1
                    b = j+1
                    tmp_score = 0
                    while (a < board.BOARD_SIZE_I and b < board.BOARD_SIZE_J and a <= i+3 and b <= j+3):
                        if board.matrix[a][b] == player:
                            tmp_score += 1
                        elif board.matrix[a][b] == rival:
                            tmp_score = 0
                            break
                        a += 1
                        b += 1
                    tmp_score **= self.EXP_LINE_WEIGHT
                    score += tmp_score
                    # Upper diagonal
                    a = i-1
                    b = j+1
                    tmp_score = 0
                    while (a >= 0 and b < board.BOARD_SIZE_J and a >= i-3 and b <= j+3):
                        if board.matrix[a][b] == player:
                            tmp_score += 1
                        elif board.matrix[a][b] == rival:
                            tmp_score = 0
                            break
                        a -= 1
                        b += 1
                    tmp_score **= self.EXP_LINE_WEIGHT
                    score += tmp_score
        return score

    def simulate_score(self, board, mover, player, slot):
        sim_board = deepcopy(board)
        try:
            sim_board.play(mover, slot)
            return self.player_score(sim_board, player)
        except AttributeError:
            return -1

    def best_move(self, board, player):
        best_score = -1
        best_moves = []
        if player == 1:
            rival = 2
        else:
            rival = 1
        for slot in range(board.BOARD_SIZE_J):
            move_value = self.simulate_score(board, player, player, slot) + self.simulate_score(board, rival, rival, slot) - self.simulate_score(board, player, rival, slot)
            if move_value > best_score:
                best_moves = [slot]
                best_score = move_value
            if move_value == best_score:
                best_moves.append(slot)
        return random.choice(best_moves)

class Game:
    ai = AI()
    board = Board()
    game_ended = False

    def __init__(self, ai_players, input_function, output_function, use_emoji = False):
        self.ai_players = ai_players
        self.input = input_function
        self.output = output_function
        self.use_emoji = use_emoji
        if use_emoji:
            self.print_player_1 = '\U0001F534'
            self.print_player_2 = '\U0001F535'

    def ai_play(self, player):
        move = self.ai.best_move(self.board, player)
        self.board.play(player, move)
        if self.use_emoji and player == 1:
            self.output("AI player ({}) played {}".format(self.print_player_1, move))
        elif self.use_emoji and player == 2:
            self.output("AI player ({}) played {}".format(self.print_player_2, move))
        else:
            self.output("AI player ({}) played {}".format(player, move))
        self.board.print(self.output, self.use_emoji)
    
    def human_play(self, player):
        move = None
        while move is None:
            try:
                move = int(self.input("Your move: [0-6] "))
                self.board.play(player, move)
            except KeyboardInterrupt:
                print()
                exit(0)
            except:
                move = None
                continue
        if self.use_emoji and player == 1:
            self.output("You ({}) played {}".format(self.print_player_1, move))
        elif self.use_emoji and player == 2:
            self.output("You ({}) played {}".format(self.print_player_2, move))
        else:
            self.output("You ({}) played {}".format(player, move))
        self.board.print(self.output, self.use_emoji)

    def play(self, player):
        if player in self.ai_players:
            self.ai_play(player)
        else:
            self.human_play(player)

    def game_state(self):
        player1_score = self.ai.player_score(self.board, 1)
        player2_score = self.ai.player_score(self.board, 2)
        if player1_score >= 3**self.ai.EXP_LINE_WEIGHT:
            self.output("Player 1 wins!")
            self.game_ended = True
        elif player2_score >= 3**self.ai.EXP_LINE_WEIGHT:
            self.output("Player 2 wins!")
            self.game_ended = True
        elif self.board.is_full():
            self.output("Draw!")
            self.game_ended = True
    
    def start(self):
        while True:
            self.play(1)
            self.game_state()
            if self.game_ended:
                break
            self.play(2)
            self.game_state()
            if self.game_ended:
                break