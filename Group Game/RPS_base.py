user1 = input("Enter P1 name: ")
user2 = input("Enter P2 name: ")

moves = ["scissors", "paper", "rock"]
user1_answers = []
user2_answers = []

wins = []
loses = []

while True:
    user1_move = input("Enter P1 move:")
    user2_move = input("Enter P2 move:")
    user1_answers.append(user1_move)
    user2_answers.append(user2_move)

    if user1_answers[-1] == user2_answers[-1]: # TIE
        print("Tie!")

    elif user1 != user2: 
        # USER 1 == SCISSORS
        if user1_answers[-1] == moves[0]: # scissors beat paper, scissors lose rock
            if user2_answers[-1] == moves[1]:
                print(f"{user1} wins. Scissors beats paper")
                wins.append(user1)
                loses.append(user2)

            elif user2_answers[-1] == moves[2]:
                print(f"{user2} wins. Rock beats scissors")
                wins.append(user2)
                loses.append(user1)
            else:
                print("invalid move")
        
        # USER 1 == PAPER
        elif user1_answers[-1] == moves[1]: # paper beats rock, paper lose scissors
            if user2_answers[-1] == moves[0]:
                print(f"{user2} wins. Scissors beats paper")
                wins.append(user2)
                loses.append(user1)
            
            elif user2_answers[-1] == moves[2]:
                print(f"{user1} wins. Paper beats rock")
                wins.append(user2)
                loses.append(user1)

            else:
                print("invalid move")
        
        # USER1 == ROCK
        elif user1_answers[-1] == moves[2]: # rock beats scissors, rock lose paper
            if user2_answers[-1] == moves[0]:
                print(f"{user1} wins. Rock beats Scissors")
                wins.append(user1)
                loses.append(user2)
            
            elif user2_answers[-1] == moves[1]:
                print(f"{user2} wins. Paper beats rock")
                wins.append(user2)
                loses.append(user1)

            else:
                print("invalid move")
        
        play_again = input("Play again? (y/n): ")
        if play_again.lower() != "y":
            break