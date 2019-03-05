import connect4

class Game:
    ai = connect4.AI()
    board = connect4.Board()
    game_ended = False

    def __init__(self, ai_players):
        self.ai_players = ai_players

    def ai_play(self, player):
        move = self.ai.best_move(self.board, player)
        self.board.play(player, move)
        print("AI player ({}) played {}".format(player, move))
        self.board.print()
    
    def human_play(self, player):
        move = int(input("Your move: [0-6] "))
        self.board.play(player, move)
        print("You ({}) played {}".format(player, move))
        self.board.print()

    def play(self, player):
        if player in self.ai_players:
            self.ai_play(player)
        else:
            self.human_play(player)

    def game_state(self):
        player1_score = self.ai.player_score(self.board, 1)
        player2_score = self.ai.player_score(self.board, 2)
        if player1_score >= 3**self.ai.EXP_LINE_WEIGHT:
            print("Player 1 wins!")
            self.game_ended = True
        elif player2_score >= 3**self.ai.EXP_LINE_WEIGHT:
            print("Player 2 wins!")
            self.game_ended = True
        elif self.board.is_full():
            print("Draw!")
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

game = Game(ai_players={2})
game.start()