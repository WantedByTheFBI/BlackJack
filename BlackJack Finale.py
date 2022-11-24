import random
import time


class Hand:
    def __init__(self):
        self.cardsinhand = []  # A list that contains the cards in the hand
        self.cardsinhandvalue = []  # A list containing the numberical values of each card
        self.active = False  # used to tell if the players 2nd hand is being used
        self.splittable = False  # used at the start of the game to see if the player hand is splittable
        self.Handvalue = 0  # the sum of the cards in their hand
        self.Busted = False  # Whether or not the hand has busted
        self.Standing = False  # Whether or not the hand is standing
        self.Bet = 0  # The amount of money the hand is worth for winnings or lose calculations

    def addcardtohand(self, deck, deckcount):  # returns a card for the
        cardholder = deck[random.randint(0, deckcount - 1)]  # The variable card holder generates a random card from the deck, temporarily holds that card for use imediately after
        deck.remove(cardholder)  # removes the same card from a copy of the deck
        self.cardsinhand.append(cardholder)  # Adds the card to it's own card list
        self.addcardsinhandvalue(cardholder)
        global Deck
        Deck = deck  # edits the global deck to the copy of the deck without the dealt card
        global Deckcount
        Deckcount -= 1

    def addcardsinhandvalue(self, cardholder):
        # this function is called whenever a card is added to a hand to add the value of the card to the cards in hand list
        if type(cardholder) == int:    # if the card being added is an integer it just adds the integer to the list
            self.cardsinhandvalue.append(cardholder)
        elif cardholder == "J" or cardholder == "Q" or cardholder == "K":   # otherwise if it's a face card then it's worth 10, so it adds to the list
            self.cardsinhandvalue.append(10)
        elif cardholder == "A":     # and finally it would otherwise be an ace and so it would add 11 to the list
            self.cardsinhandvalue.append(11)
        self.updateHandValue() # calls update hand value since the hand has been modified

    def updateHandValue(self): # a function that gets called when the hand gets modified to update the value
        self.Handvalue = 0 # resets the hand value to 0
        for i in self.cardsinhandvalue:
            self.Handvalue += i # adds each number in the list to the value
        if self.Handvalue > 21:
            self.Checkifbusted()
        return

    def Checkifbusted(self):  # checks if the hand is busted or not
        print(self.Handvalue)
        if self.Handvalue > 21:
            if (11 in self.cardsinhandvalue) == True:  # if there is an ace worth 11 in their hand
                self.cardsinhandvalue.insert(self.cardsinhandvalue.index(11), 1) # it replaces it with a 1
                self.cardsinhandvalue.remove(11)  # removes the 11
                print(self.cardsinhandvalue)
                self.updateHandValue()  # updates the handvalue
                if self.Checkifbusted() == False: return False  # recursively checks if it's still busted
            else:
                self.Busted = True  # otherwise it sets it to busted
                return True  # then returns that it has busted
        else:
            return False  # if the handvalue isn't busted, it returns false
    def CalculatingMoneyGainLoss(self):
        if self == Player.PlayerHand:  # if it's the first hand the variable x is first
            x = "First"
        else:  # if it's the second hand the variable x is second
            x = "Second"
        if self.Handvalue == Dealer.Handvalue:  # if they tie just return
            print(f"Your {x} hand tied against the dealer so you didn't win or lose anything!")
            return
        if self.Busted == True and Dealer.Busted != True:  # if the dealer busted and your hand didn't
            print(f"Your {x} hand busted! You lost $", end='')
            print(self.Bet)
            Player.Money -= self.Bet
            return
        if self.Busted != True and self.Handvalue != 21 and Dealer.Busted == True:  # if you haven't busted and your hand isn't 21 but the dealer busted
            print(f"The Dealer busted and your {x} hand didn't! You won $", end='')
            print(self.Bet)
            Player.Money += self.Bet
            return
        if self.Busted != True and Dealer.Busted != True:  # if neither person busted
            if self.Handvalue > Dealer.Handvalue and self.Handvalue != 21:  # if you win and didn't blackjack
                print(f"Your {x} hand was better than the dealer's, you won $", end='')
                print(self.Bet)
                Player.Money += self.Bet
                return
            elif self.Handvalue > Dealer.Handvalue and self.Handvalue == 21:  # if you win and do blackjack
                print(f"Your {x} hand blackjacked against the dealer and won $", end='')
                print(self.Bet * 1.5)
                Player.Money += self.Bet * 1.5
                return
            if self.Handvalue < Dealer.Handvalue:  # if you lose
                print(f"Your {x} hand was worse than the dealer's, you lost $", end='')
                print(self.Bet)
                Player.Money -= self.Bet
                return
def Checkifsplittable():  # checks if the first and second card in the hand are the same then makes it splittable
    if len(Player.PlayerHand.cardsinhand) == 2 and Player.PlayerHand.cardsinhand[0] == Player.PlayerHand.cardsinhand[1]:
        Player.PlayerHand.splittable = True
class player:  # exclusively used for the player
    Money = 1000  # initial starting money
    PlayerHand = Hand()  # Their first hand is a new Hand object
    PlayerHand2 = Hand()  # Their second hand is a new Hand object
    def Split(self):  # splits the players hand into hand 1 and hand 2
        Player.PlayerHand.cardsinhand = Player.PlayerHand.cardsinhand[0]  # makes both their hands the cards they split
        Player.PlayerHand2.cardsinhand = Player.PlayerHand.cardsinhand
        Player.PlayerHand2.active = True  # makes it active for the game loop to see and use the second hand
        Player.split = True
        Player.PlayerHand2.Standing = False
        return
    split = False  # will be changed by the splitting action
Player = player()
def CheckifDealercanplay():
    Dealer.updateHandValue()
    if Dealer.Handvalue > 16:
        Dealer.Standing = True
        return False
    else: return True
Deck_Constant = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']*12 #the deck will make itself this if the deck ever hits 0 cards
def printing_hands(playerhand, owner):
    print(owner + " Hand:  [", end='') #prints "(Owner of the hand) Hand :["
    for i in range(0,len(playerhand)):
        print(playerhand[i], end='')
        if i != len(playerhand)-1:
            print("][", end='')
    print("]")
Player.PlayerHand2.Standing = True #makes sure if it isn't active it will become active

def printing_both_hands():
    if Player.PlayerHand2.active == True:
        printing_hands(Player.PlayerHand.cardsinhand, "Player First")
        printing_hands(Player.PlayerHand2.cardsinhand, "Player Second")
    else: printing_hands(Player.PlayerHand.cardsinhand, "Player")
    printing_hands(Dealer.cardsinhand, "Dealer")
Dealer = Hand() #makes our "Dealer", which will just be a Hand Object that has to follow certain rules (thanks blackjack dealer rules for making them essentially a robot)
Deck = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'] * 12
Deckcount = 156
print("Welcome to Jack's Blackjack! Note that you can only split once per round, and buying insurance is removed") #because otherwise it gets annoying to code
while True: #this runs until it doesn't
    Player.PlayerHand = Hand()
    Player.PlayerHand2 = Hand()
    Dealer = Hand()
    Player.PlayerHand2.Standing = True
    Player.split = False
    while Deck == 0: #if the deck hits 0 cards left then it resets itself
        Deck = Deck_Constant
    print("You have $", end='')
    print(Player.Money)
    bet = int(input("How much would you like to bet? ")) #how much they want to bet
    while bet > Player.Money or bet <= 0: #if the bet is more then they have or <0 then it makes them reenter a valid number
        print("You cannot bet $" + bet)
        bet = input("Please reenter how much you would like to bet: ")
    Player.PlayerHand.Bet = bet
    for startingdealing in range(0, 4):
        if startingdealing == 0 or startingdealing == 2:
            Player.PlayerHand.addcardtohand(Deck, Deckcount)
            # this alternates between dealing a card to the player and a card to the dealer to start off the game
        else:
            Dealer.addcardtohand(Deck,Deckcount)
    Player.PlayerHand.updateHandValue()
    Player.PlayerHand.Busted = Player.PlayerHand.Checkifbusted  # checks if they've busted at 2nd card dealt, this is really just to force a second ace to be worth 1
    Player.PlayerHand.splittable = Checkifsplittable()
    Dealer.updateHandValue()
    Dealer.Checkifbusted()
    print("Your Hand:  [", end='')  # spaces after "Your Hand:" are to make them all line up properly
    print(Player.PlayerHand.cardsinhand[0], end='')
    print("]")  # the square brackets are to give the shape of the playing card
    time.sleep(1)  # small break in time before it prints the next line, maybe a second or two to give the impression of cards being dealt out
    print("Dealer Hand:[", end='')
    print(Dealer.cardsinhand[0], end='')
    print("]")
    time.sleep(1)
    print("Your Hand:  [", end='')
    print(Player.PlayerHand.cardsinhand[0], end='')
    print("][", end='')
    print(Player.PlayerHand.cardsinhand[1], end='')
    print("]")
    time.sleep(1)
    print("Dealer Hand:[", end='')
    print(Dealer.cardsinhand[0], end='')
    print("]", end='')
    print("[ ]")
    courseofaction = input("Would you like to Play or Surrender this hand? ")
    if courseofaction.lower() == "surrender":
        Player.Money -= Player.PlayerHand.Bet / 2 #if you surrender you lose half your bet rather than all of it
        Player.PlayerHand.splittable = False
        Dealer.Standing = True
        Player.PlayerHand.Standing = True
    if courseofaction.lower() == "play":
        if Dealer.Handvalue == 21 and Player.PlayerHand.Handvalue != 21:
            time.sleep(1)
            printing_hands(Dealer.cardsinhand, "Dealer")
            time.sleep(1)
            print("The Dealer natural blackjacked, you auto-lost the hand")
            Player.Money -= Player.PlayerHand.Bet
            Player.PlayerHand.splittable = False
            Dealer.Standing = True
            Player.PlayerHand.Standing = True
        if Player.PlayerHand.splittable == True:
            action = input("Would you like to Split your hand?(Yes or No)")
            if action.lower() == "Yes":
                Player.Split()
        while Player.PlayerHand.Standing == False or Player.PlayerHand2 == False or Dealer.Standing == False:
            printing_both_hands()
            if Player.PlayerHand.Checkifbusted() != False:
                Player.PlayerHand.Standing = True
            if Player.PlayerHand2.active == True:
                if Player.PlayerHand2.Checkifbusted() != False:
                    Player.PlayerHand2.Standing = True
                if Player.PlayerHand.Standing != True: #if their first hand is standing it won't have a turn
                    print("What would you like to do with your first hand?")
                    print("Would you like to Hit, Stand or Double Down?")
                    action = input()  # asks them what they want to do
                    if "hit" == action.lower():  # if they want to hit
                        Player.PlayerHand.addcardtohand(Deck,Deckcount)
                    elif action.lower() == "stand":  # if they want to stand they get set to standing
                        Player.PlayerHand.Standing = True
                    elif action.lower() == "double down":  # this hits, stands, and doubles their bet
                        Player.PlayerHand.addcardtohand(Deck,Deckcount)
                        Player.PlayerHand.Standing = True
                        Player.PlayerHand.Bet *= 2
                if Player.PlayerHand2.Standing != True: #if the second hand is standing it won't have a turn
                    print("What would you like to do with your second hand?")
                    print("Would you like to Hit, Stand or Double Down?")
                    action = input()  # asks them what they want to do
                    if "hit" == action.lower():  # if they want to hit
                        Player.PlayerHand2.addcardtohand(Deck, Deckcount)
                    elif action.lower() == "stand":  # if they want to stand they get set to standing
                        Player.PlayerHand2.Standing = True
                    elif action.lower() == "double down":  # this hits, stands, and doubles their bet
                        Player.PlayerHand2.addcardtohand(Deck, Deckcount)
                        Player.PlayerHand2.Standing = True
                        Player.PlayerHand2.Bet *= 2
            else:
                if Player.PlayerHand.Standing != True:
                    print("What would you like to do with your hand?")
                    print("Would you like to Hit, Stand or Double Down?")
                    action = input()  # asks them what they want to do
                    if action.lower() == "hit":  # if they want to hit
                        Player.PlayerHand.addcardtohand(Deck, Deckcount)
                    elif action.lower() == "stand":  # if they want to stand they get set to standing
                        Player.PlayerHand.Standing = True
                    elif action.lower() == "double down":  # this hits, stands, and doubles their bet
                        Player.PlayerHand.addcardtohand(Deck, Deckcount)
                        Player.PlayerHand.Standing = True
                        Player.PlayerHand.Bet *= 2
            if CheckifDealercanplay() == False:
                Dealer.Standing = True
            if Dealer.Standing == False:
                Dealer.addcardtohand(Deck, Deckcount)
            Player.PlayerHand.updateHandValue()


        printing_both_hands()
        Player.PlayerHand.updateHandValue() #just does a final check of all of their handvalues before paying out
        Player.PlayerHand2.updateHandValue()
        Dealer.updateHandValue()
        Player.PlayerHand.CalculatingMoneyGainLoss()
        if Player.PlayerHand2.active == True:
            Player.PlayerHand2.CalculatingMoneyGainLoss()
        print("Would you like to play again? Yes or No")
        playagain = input()
        if playagain.lower() == "yes":
            continue
        elif playagain.lower() == "no":
            print("You went home with $",end='')
            print(Player.Money)
            break