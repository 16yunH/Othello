from othellolib import test_board, game, create_player, move_input, move_AI, move_AI_random

def main():
    print("Welcome to Othello! Choose the mode of play:")
    print("1. Normal: Human vs Human")
    print("2. Challenge: Human vs AI")
    print("3. crazy: AI vs AI!")
    opponent = input("Enter your choice (1/2/3): ")
    if opponent == '1':
        name1 = input("Enter name for Player1: ")
        name2 = input("Enter name for Player2: ")
        player1 = create_player(f'⚫️  {name1}', move_input)
        player2 = create_player(f'⚪️  {name2}', move_input)
    elif opponent == '2':
        name1 = input("Enter name for Player1: ")
        player1 = create_player(f'⚫️  {name1}', move_input)
        player2 = create_player('⚪️  AI', move_AI)
    elif opponent == '3':
        player1 = create_player('⚫️  AI1', move_AI_random)
        player2 = create_player('⚪️  AI2', move_AI_random)
    else:
        print("Invalid choice. Defaulting to Human vs AI.")
        name1 = input("Enter name for Player1: ")
        player1 = create_player(f'⚫️  {name1}', move_input)
        player2 = create_player('⚪️  AI', move_AI)
    game(player1, player2)

if __name__ == "__main__":
    test_board()
    main()
