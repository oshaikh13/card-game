# heavily modified version of: 
# https://codereview.stackexchange.com/questions/82103/ascii-fication-of-playing-cards

class Card(object):

    card_values = {
        'Ace': 11,  # value of the ace is high until it needs to be low
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'Jack': 10,
        'Queen': 10,
        'King': 10
    }

    suit_to_color = {
        'Diamonds': 'red',
        'Hearts': 'red',
        'Spades': 'black',
        'Clubs': 'black'
    }

    def __init__(self, suit, rank):
        """
        :param suit: The face of the card, e.g. Spade or Diamond
        :param rank: The value of the card, e.g 3 or King
        """
        self.suit = suit.capitalize()
        self.rank = rank
        self.color = self.suit_to_color[suit]
        self.points = self.card_values[rank]
    
    def is_matching(self, provided_card):
        return  self.color == provided_card.color and self.rank == provided_card.rank

def ascii_row_of_cards(cards, mask, row, return_string=True):
    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    :param return_string: By default we return the string version of the card, but the dealer hide the 1st card and we
    keep it as a list so that the dealer can add a hidden card in front of the list
    """

    suits_name = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
    suits_symbols = ['♠', '♦', '♥', '♣']


    lines = [
      ['  '], 
      ['  '],
      ['  '], 
      ['  '], 
      [str(row) + ' '], 
      ['  '], 
      ['  '], 
      ['  '], 
      ['  ']
    ]
    hidden_lines = [
      '┌─────────┐', 
      '│░░░░░░░░░│',
      '│░░░░░░░░░│', 
      '│░░░░░░░░░│', 
      '│░░░░░░░░░│', 
      '│░░░░░░░░░│', 
      '│░░░░░░░░░│', 
      '│░░░░░░░░░│', 
      '└─────────┘'
    ]

    for index, card in enumerate(cards):

        if mask[index]:
            for i in range(0, len(hidden_lines)):
                lines[i].append(hidden_lines[i])
        
        if mask[index]:
            continue

        if card.rank == '10': 
            rank = card.rank
            space = ''
        else:
            rank = card.rank[0]  
            space = ' '

        suit = suits_name.index(card.suit)
        suit = suits_symbols[suit]

        lines[0].append('┌─────────┐')
        lines[1].append('│{}{}       │'.format(rank, space)) 
        lines[2].append('│         │')
        lines[3].append('│         │')
        lines[4].append('│    {}    │'.format(suit))
        lines[5].append('│         │')
        lines[6].append('│         │')
        lines[7].append('│       {}{}│'.format(space, rank))
        lines[8].append('└─────────┘')

    result = [''.join(line) for line in lines]

    if return_string:
        return '\n'.join(result)
    else:
        return result

