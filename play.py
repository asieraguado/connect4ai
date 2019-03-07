import connect4

print("You can view the game board using color emoji circles, which makes it easier to see and play. If your terminal doesn't display color emoji, a matrix of numbers will be used.")
ans = input("Does your terminal support color emoji (y/N)?")

if ans == 'y' or ans == 'Y':
    use_emoji = True
else:
    use_emoji = False

game = connect4.Game(ai_players={2}, input_function=input, output_function=print, use_emoji=use_emoji)
game.start()