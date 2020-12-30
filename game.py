import random


# kupa  a
# karo  b
# maça  c
# sinek d
# 1, 10 yerine geçecek

def compare(card1, card2, length):
    if card1[0] == card2[0] or card1[0] == 'J':
        if length == 2:
            if card2[0] == 'J':
                return 20
            return 10
        return 0
    else:
        return 'x'


class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        # pişti
        self.isFirstRound = True
        self.p1Points = 0
        self.p2Points = 0
        self.p1Turn = True
        self.p2Turn = True
        self.leftCards = ['Aa', 'Ab', 'Ac', 'Ad', '1a', '1b', '1c', '1d', '2a', '2b', '2c', '2d', '3a', '3b', '3c',
                          '3d', '4a', '4b', '4c', '4d', '5a', '5b', '5c', '5d', '6a', '6b', '6c', '6d', '7a', '7b',
                          '7c', '7d', '8a', '8b', '8c', '8d', '9a', '9b', '9c', '9d', 'Ja', 'Jb', 'Jc', 'Jd', 'Qa',
                          'Qb', 'Qc', 'Qd', 'Ka', 'Kb', 'Kc', 'Kd']
        self.p1cards = []
        self.p1cards1 = []
        self.p1Deadcards = []
        self.p2Deadcards = []
        self.p2cards = []
        self.p2cards1 = []
        self.middleCards = []
        self.pishticard = ''
        self.dealt = False  # deal() sonunda true, card_played() sonunda false oluyor

    def deal_cards_first(self):
        for i in range(4):
            x = random.randint(0, len(self.leftCards) - 1)
            self.middleCards.append(self.leftCards[x])
            del self.leftCards[x]
            self.isFirstRound = False
            self.p2Turn = False
        self.deal_cards()

    def deal_cards(self):
        for i in range(4):
            x = random.randint(0, len(self.leftCards) - 1)
            self.p1cards.append(self.leftCards[x])
            del self.leftCards[x]

            x = random.randint(0, len(self.leftCards) - 1)
            self.p2cards.append(self.leftCards[x])
            del self.leftCards[x]
        self.p1cards1 = self.p1cards.copy()
        self.p2cards1 = self.p2cards.copy()
        self.dealt = True

    def card_played(self, p, card):

        if p == 0:
            self.middleCards.append(card)
            self.p1cards.remove(card)
            self.p1cards1[self.p1cards1.index(card)] = 'x'
            if len(self.middleCards) > 1:
                check = compare(self.middleCards[-1], self.middleCards[-2], len(self.middleCards))
                if check != 'x':
                    self.p1Points += check
                    self.p1Deadcards.extend(self.middleCards)
                    self.pishticard = self.middleCards[-1]
                    self.middleCards.clear()


        elif p == 1:
            self.middleCards.append(card)
            self.p2cards.remove(card)
            self.p2cards1[self.p2cards1.index(card)] = 'x'
            if len(self.middleCards) > 1:
                check = compare(self.middleCards[-1], self.middleCards[-2], len(self.middleCards))
                if check != 'x':
                    self.p2Points += check
                    self.p2Deadcards.extend(self.middleCards)
                    self.pishticard = self.middleCards[-1]
                    self.middleCards.clear()

        self.p1Turn = not self.p1Turn
        self.p2Turn = not self.p2Turn
        self.dealt = False

    def connected(self):
        return self.ready

    def calculator1(self):
        for x in self.p1Deadcards:
            if x == '2d':
                self.p1Points += 2
            if x == '1d':
                self.p1Points += 3
            if x[0] == 'A' or x[0] == 'J':
                self.p1Points += 1
        if len(self.p1Deadcards) > len(self.p2Deadcards):
            self.p1Points += 3
        return self.p1Points

    def calculator2(self):
        for x in self.p2Deadcards:
            if x == '2d':
                self.p2Points += 2
            if x == '1d':
                self.p2Points += 3
            if x[0] == 'A' or x[0] == 'J':
                self.p2Points += 1
        if len(self.p2Deadcards) > len(self.p1Deadcards):
            self.p2Points += 3
        return self.p2Points
