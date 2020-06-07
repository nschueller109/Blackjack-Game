import random

suits = ('♥', '♦', '♠', '♣')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10,
         'Q':10, 'K':10, 'A':11}

playing = True

class Card:

    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + self.suit

class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for rank in ranks:
            for suit in suits:
                self.deck.append(Card(rank,suit))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n '+ card.__str__()
        return 'The deck has: ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'A':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Place your bet "))
        except ValueError:
            print("Your bet must be a numerical value")

        else:
            if chips.bet > chips.total:
                print("Insufficient Funds, your bet cannot exceed ", chips.total)
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop

    while True:
        choice = input("Would you like to hit or stand? ")

        if choice.upper()[0] == 'H':
            hit(deck,hand)

        elif choice.upper()[0] == 'S':
            print("You choose to stand. The dealer will now play.")
            playing = False

        else:
            print("Sorry please try again")
            continue
        break

def show_some(player,dealer):
    print("\nDealer's Hand: ")
    print('',dealer.cards[1])
    print("The dealer's remaining card is hidden")
    print("\nPlayer's Hand: ", *player.cards, sep = '\n ')

def show_all(player,dealer):
    print("\nPlayer's Hand: ", *player.cards, sep = '\n ')
    print("Your final value = ",player.value)
    print("\nDealer's Hand: ", *dealer.cards, sep = '\n ')
    print("The dealer's final value = ",dealer.value)

def player_busts(player,dealer,chips):
    print("\nBUSTED")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("\nYou are victorious!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("\nDealer busted. You win!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("\nDealer wins")
    chips.lose_bet()

def push(player,dealer):
    print("\nDealer and player tie! It's a push")


##### GAME MODULE #####

#Print an opening statement
print("\n\n\nWelcome to Nate's Casino")
player = input("\nRemind me of your name again? ")
print(f"\nWe are blessed with your presence {player}.")

while True:

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()
    print("\nYou will begin with 100 chips")

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)

        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        elif player_hand.value < dealer_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)

    # Inform Player of their chips total
    print("\nYour new chip count is ",player_chips.total)

    # Ask to play again
    replay = input("\n\n\nWould you like to play again? Answer 'Yes' or 'No' ")

    if replay.upper()[0] == 'Y':
        playing = True
        continue

    else:
        print("\nThanks for playing. Have a nice life!")
        break
