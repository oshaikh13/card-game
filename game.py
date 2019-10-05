import random
import time
import os
import sys
from card import Card, ascii_row_of_cards

class Memory():
    card_rank = [
        'Ace',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        'Jack',
        'Queen',
        'King'
    ]

    card_suit = ['Spades', 'Diamonds', 'Hearts', 'Clubs']

    # params
    # width, height: the width/height of the rendered deck 
    # self_play: bool - computer naievly plays itself.
    # wait_time: int - how long should the revealed cards be shown.
    def __init__(self, width=13, height=4, self_play=False, wait_time=4):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.total_cards = width * height
        self.width = width
        self.height = height
        self.self_play = self_play
        self.wait_time = wait_time
        self.generate_game_state()
        self.total_matching = 0
        self.moves = 0
        self.print_state()

    # renders the current state of cards
    def print_state(self):

        # print the column headers.
        top = "  "
        for i in range(0, self.width):
            top += '     ' + str(i + 1) + '     '
        print(top)

        # print the rows of cards.
        for i in range(0, self.height):
            print(ascii_row_of_cards(self.selected_deck[i], self.mask[i], i + 1))
        
    # generates the initial game state.
    def generate_game_state(self):
        # creates a deck of 52 cards.
        generated_deck = [Card(suit, rank) for rank in self.card_rank for suit in self.card_suit]

        # shuffles the cards, picks out a total
        random.shuffle(generated_deck)
        generated_deck = generated_deck[:self.total_cards]

        # creates a mask to hide specific cards.
        # if a value at a mask index is true, then the card is hidden.
        self.mask = [[True for x in range(self.width)] for y in range(self.height)]
        self.selected_deck = [[True for x in range(self.width)] for y in range(self.height)] 

        # loads shuffled cards into a "selected" deck.
        curr_idx = 0
        for i in range(self.height):
            for j in range(self.width):
                self.selected_deck[i][j] = generated_deck[curr_idx]
                curr_idx += 1

    # a generating function for computer self-play
    # note that this is probably the worst possible way to play.
    # computer brute forces all options until it wins.
    def next_card_generator(self):
        possible_cards = [(i, j) for i in range(self.height) for j in range(self.width)]
        for card_a in possible_cards:
            for card_b in possible_cards:
                if card_a != card_b and self.check_mask(card_a) and self.check_mask(card_b):
                    yield (card_a, card_b)
                else:
                    continue

    # checks a mask to see if a card is hidden
    # card - tuple of form (r - int, w - int)
    def check_mask(self, card):
        r, w = card
        return self.mask[r][w]

    # sets a mask to hide/show a card
    # card - tuple of form (r - int, w - int)
    # new_mask_val - bool
    def set_mask(self, card, new_mask_val):
        r, w = card
        self.mask[r][w] = new_mask_val

    # checks if a card is out of bounds.
    # card - tuple of form (r - int, w - int)
    def card_out_of_bounds(self, card):
        r, w = card
        return r >= self.height or w >= self.width

    # checks two cards are matching.
    # card_a - tuple of form (r - int, w - int)
    # card_b - tuple of form (r - int, w - int)
    def cards_matching(self, card_a, card_b):
        r1, w1 = card_a
        r2, w2 = card_b
        return self.selected_deck[r1][w1].is_matching(self.selected_deck[r2][w2])

    # kicks the game off
    def start_game(self):
        print("Hey! This is single player Memory.")
        print("Cards must match in Rank and Color! Enter something out of bounds to quit!")
        print("Remember, diamonds and hearts are red; spades and clubs are black.")
        print("Do you want to watch the computer play a VERY naive round with itself? (Y/N): ", end="")
        self_play_response = str(input()).lower()

        if len(self_play_response) > 0 and self_play_response[0] == "y":
            self.self_play = True
            self.wait_time = 0

        all_cards_generator = self.next_card_generator()

        while True:
            if self.self_play:
                # use the generator if the computer is playing itself.
                next_cards = next(all_cards_generator)
                card_a, card_b = next_cards
            else:
                print("Enter your selections.")
                try:
                    print("Card 1 row: ", end="")
                    r1 = int(input()) - 1
                    print("Card 1 column: ", end="")
                    w1 = int(input()) - 1
                    print("Card 2 row: ", end="")
                    r2 = int(input()) - 1
                    print("Card 2 column: ", end="")
                    w2 = int(input()) - 1
                    card_a = (r1, w1)
                    card_b = (r2, w2)
                except:
                    print("Invalid Input!")
                    continue

            # exit if cards are out of bounds.
            if self.card_out_of_bounds(card_a) or self.card_out_of_bounds(card_b):
                sys.exit()

            if card_a == card_b:
                print("Cards must be different!")
                continue

            if not self.check_mask(card_a) or not self.check_mask(card_b):
                print("Both cards must be hidden!")
                continue

            # check if cards are matching, remove masks
            self.moves += 1
            matching = self.cards_matching(card_a, card_b)
            self.set_mask(card_a, False)
            self.set_mask(card_b, False)

            if matching:
                os.system('cls' if os.name == 'nt' else 'clear')
                self.total_matching += 1
                print("Cards are matching!") 
                print("Total Matched: " + str(self.total_matching))
                print("Total Moves: " + str(self.moves))

                time.sleep(self.wait_time)
                self.print_state()
                if self.total_matching == self.total_cards / 2:
                    print("YOU WON! GAME OVER.")
                    sys.exit()
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Not matching! Try again")
                self.print_state()
                self.set_mask(card_a, True)
                self.set_mask(card_b, True)
                time.sleep(self.wait_time)
                os.system('cls' if os.name == 'nt' else 'clear')
                self.print_state()

my_mem = Memory()
my_mem.start_game()
