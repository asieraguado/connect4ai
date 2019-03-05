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

    def print(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                print(self.matrix[i][j], end=" ")
            print()
    
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