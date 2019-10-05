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

    def __init__(self, width, height):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.total_cards = width * height
        self.width = width
        self.height = height
        self.generate_game_state()
        self.print_state()
        self.start_game()
        self.matching = 0

    def print_state(self):
        top = "  "
        for i in range(0, self.width):
            top += '     ' + str(i + 1) + '     '

        print(top)
        for i in range(0, self.height):
            print(ascii_row_of_cards(self.selected_deck[i], self.mask[i], i + 1))
        

    def generate_game_state(self):
        generated_deck = []
        for suit in self.card_suit:
            generated_deck.extend([Card(suit, rank) for rank in self.card_rank])

        # generated_deck = [[suit, value] for value in card_values] for suit in card_suit]

        random.shuffle(generated_deck)
        generated_deck = generated_deck[:self.total_cards]
        self.mask = [[True for x in range(self.width)] for y in range(self.height)]
        self.selected_deck = [[True for x in range(self.width)] for y in range(self.height)] 

        curr_idx = 0
        for i in range(self.height):
            for j in range(self.width):
                self.selected_deck[i][j] = generated_deck[curr_idx]
                curr_idx += 1

    def start_game(self):
        print("Hey! This is Memory; cards must match in Rank and Color! Enter something out of bounds to quit!")
        print("Remember, diamonds and hearts are red; spades and clubs are black.")
        while True:
            print("Type the row and column of two cards.")
            try:
                print("Card 1 row: ", end="")
                r1 = int(input()) - 1
                print("Card 1 column: ", end="")
                w1 = int(input()) - 1
                print("Card 2 row: ", end="")
                r2 = int(input()) - 1
                print("Card 2 column: ", end="")
                w2 = int(input()) - 1
            except:
                print("Invalid Input!")
                continue

            if r1 >= self.height or r2 >= self.height:
                sys.exit()

            if w1 >= self.width or w2 >= self.width:
                sys.exit()

            if (r1, w1) == (r2,  w2):
                print("Cards must be different!")
                continue

            if not self.mask[r1][w1] or not self.mask[r2][w2]:
                print("Both cards must be hidden!")
                continue

            matching = self.selected_deck[r1][w1].is_matching(self.selected_deck[r2][w2])
            self.mask[r1][w1] = False
            self.mask[r2][w2] = False
            if matching:
                os.system('cls' if os.name == 'nt' else 'clear')
                self.matching += 1
                print("Cards are matching! Total Matched: " + str(self.matching))
                time.sleep(4)
                self.print_state()
                if self.matching == self.total_cards:
                    print("YOU WON! GAME OVER.")
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Not matching! Try again")
                self.print_state()
                self.mask[r1][w1] = True
                self.mask[r2][w2] = True
                time.sleep(4)
                os.system('cls' if os.name == 'nt' else 'clear')
                self.print_state()

my_mem = Memory(13, 4)

  

