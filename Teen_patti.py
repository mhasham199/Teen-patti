import random

# Card-related constants
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}

# Game State Variables
user_coins = 1000
computer_coins = 1000
pot = 0
user_hand = []
computer_hand = []
deck = []


# Initialize and shuffle the deck with all 52 cards
def initialize_deck():
    """Creates and shuffles a deck of cards."""
    global deck
    deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
    random.shuffle(deck)


# Deals a single card from the deck
def deal_card():
    """Deals one card from the top of the deck."""
    return deck.pop()


# Distributes three cards to both the user and computer
def deal_hands():
    """Distributes 3 cards each to the user and computer."""
    global user_hand, computer_hand
    user_hand = [deal_card() for _ in range(3)]
    computer_hand = [deal_card() for _ in range(3)]


# Creates an ASCII representation of a card
def display_card(card):
    """Generates a visual representation of a card for display."""
    symbol = suit_symbols[card['suit']]
    rank = f"{card['rank']:<2}"
    return [
        "┌───────┐",
        f"│ {rank}    │",
        "│       │",
        f"│   {symbol}   │",
        "│       │",
        f"│    {rank} │",
        "└───────┘",
    ]


# Displays the player's cards in a single, compact line
def display_hand_inline(hand):
    """Displays all cards in a player's hand inline."""
    card_lines = [display_card(card) for card in hand]
    for i in range(7):
        print("  ".join(card[i] for card in card_lines))


# Displays the current balances of the user, computer, and the pot
def show_balances():
    """Displays the current coin balances and the pot."""
    print(f"\n=> User Coins: {user_coins}")
    print(f"=> Computer Coins: {computer_coins}")
    print(f"=> Pot: {pot}\n")


# Places a bet for either the user or the computer
def place_bet(player, amount):
    """Places a bet for the specified player and updates the pot."""
    global user_coins, computer_coins, pot
    if player == "User" and user_coins >= amount:
        user_coins -= amount
        pot += amount
        return True
    elif player == "Computer" and computer_coins >= amount:
        computer_coins -= amount
        pot += amount
        return True
    return False


# Transfers the pot winnings to the winning player and resets the pot
def distribute_winnings(winner):
    """Transfers the pot amount to the winner and resets the pot."""
    global user_coins, computer_coins, pot
    if winner == "User":
        user_coins += pot
    elif winner == "Computer":
        computer_coins += pot
    pot = 0


# Evaluates the score of a player's hand and provides the reason
def evaluate_hand(hand):
    """Evaluates a hand's score and returns the rank and reason."""
    ranks_in_hand = [card['rank'] for card in hand]
    suits_in_hand = [card['suit'] for card in hand]

    rank_values = sorted([ranks.index(rank) for rank in ranks_in_hand])

    if len(set(ranks_in_hand)) == 1:  # Trail/Trio
        return (5, rank_values[-1], "Trail (Three of a Kind)")
    if len(set(suits_in_hand)) == 1 and rank_values[2] - rank_values[0] == 2:  # Pure Sequence
        return (4, rank_values[-1], "Pure Sequence (Straight Flush)")
    if rank_values[2] - rank_values[0] == 2:  # Sequence
        return (3, rank_values[-1], "Sequence (Straight)")
    if len(set(suits_in_hand)) == 1:  # Flush
        return (2, rank_values[-1], "Flush")
    if len(set(ranks_in_hand)) == 2:  # Pair
        pair_value = max(rank_values, key=ranks_in_hand.count)
        return (1, pair_value, "Pair")
    return (0, rank_values[-1], "High Card")  # High Card


# Determines the winner by comparing the evaluated scores of both players
def determine_winner():
    """Determines the winner by comparing scores and reasons."""
    user_score = evaluate_hand(user_hand)
    computer_score = evaluate_hand(computer_hand)

    if user_score > computer_score:
        return "User", user_score[2]
    else:
        return "Computer", computer_score[2]


# Manages a single round of betting, dealing, and determining the winner
def play_round():
    """Plays a single round of Teen Patti, including betting and showing results."""
    global user_coins, computer_coins, user_hand, computer_hand

    print("\n--- New Round ---")
    show_balances()

    # Deal hands to both players at the start of the round
    deal_hands()

    # Show user's cards before asking for the bet
    print("\nYour cards:")
    display_hand_inline(user_hand)

    # Place initial bets
    try:
        user_bet = int(input("Enter your bet amount: "))
    except ValueError:
        print("Invalid input. Exiting round.")
        return
    if user_bet > user_coins:
        print("You don't have enough coins to place this bet.")
        return
    place_bet("User", user_bet)

    computer_has_played = False  # Track if computer has placed a bet

    while True:
        ready = input("\nAre you ready for the computer's bet? (yes/no): ").strip().lower()
        if ready == 'yes':
            if not computer_has_played:
                # First round: computer only bets
                computer_bet = min(random.randint(1, 500), computer_coins)
                place_bet("Computer", computer_bet)
                print(f"\nComputer bet: ({computer_bet} coins).")
                computer_has_played = True
            else:
                # Subsequent rounds: 70% bet, 30% reveal winner
                if random.random() < 0.7:
                    computer_bet = min(random.randint(1, 500), computer_coins)
                    place_bet("Computer", computer_bet)
                    print(f"\nComputer bet: ({computer_bet} coins).")
                else:
                    print("\nComputer chose to reveal the winner!")
                    print("\nRevealing cards and determining the winner...")

                    print("\nUser's cards:")
                    display_hand_inline(user_hand)
                    print("\nComputer's cards:")
                    display_hand_inline(computer_hand)

                    winner, reason = determine_winner()
                    print(f"\nThe winner is {winner}!")
                    print(f"Reason: {reason}")

                    distribute_winnings(winner)

                    # Show updated balances
                    print("\nUpdated Balances:")
                    show_balances()
                    return

        else:
            print("Exiting round. Goodbye!")
            return

        # User action loop
        while True:
            print("\nOptions:")
            print("   1. Place another bet")
            print("   2. Reveal winner\n")

            choice = input("Enter your choice (1/2): ")
            if choice == '1':
                try:
                    additional_bet = int(input("\nEnter additional bet amount (up to 500): "))
                    if additional_bet > 500 or additional_bet > user_coins:
                        print("Invalid bet amount.")
                    else:
                        place_bet("User", additional_bet)
                        print(f"\nYou added {additional_bet} coins to the pot.")
                        break  # Go back to the computer's bet phase
                except ValueError:
                    print("Invalid input.")
            elif choice == '2':
                print("\nRevealing cards and determining the winner...")
                print("\nUser's cards:")
                display_hand_inline(user_hand)
                print("\nComputer's cards:")
                display_hand_inline(computer_hand)

                winner, reason = determine_winner()
                print(f"\nThe winner is {winner}!")
                print(f"Reason: {reason}")

                distribute_winnings(winner)

                # Show updated balances
                print("\nUpdated Balances:")
                show_balances()
                return
            else:
                print("Invalid choice. Try again.")


# Starts the game and continues until one player runs out of coins
def start_game():
    """Starts the Teen Patti game and continues until the game ends."""
    print("\n--- Welcome to Teen Patti ---")
    initialize_deck()

    while user_coins > 0 and computer_coins > 0:
        play_round()

        # Ask user if they are ready for the next round
        ready_for_next_round = input("\nAre you ready for the next round? (yes/no): ").strip().lower()
        if ready_for_next_round != 'yes':
            print("You have exited the game. Goodbye!")
            break
        

    print("\nGame Over!")
    show_balances()



# Start the game
start_game()
