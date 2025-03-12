import numpy as np

#winrate: float = 0.55
Diamonds = 10000

class Draft:
    pass

class Quickdraft(Draft):
    cost = 750
    reward = {0:50, 1: 100, 2:200, 3:300, 4:450, 5:650, 6:850, 7:950}

class Premierdraft(Draft):
    cost = 1500
    reward = {0:50, 1: 100, 2:250, 3:1000, 4:1400, 5:1600, 6:1800, 7:2200}

def start_game(winrate)->bool:
    # get a 55% chance win to be true
    win = np.random.choice([True, False], p=[winrate, 1-winrate])
    return win

def start_simulation(Draft, winrate):
    try:
        Draft.cost
        Draft.reward
    except:
        print("Draft class has no cost")

    global Diamonds
    Diamonds = Diamonds - Draft.cost
    wins = 0
    looses = 0

    for game in range(10):
        if start_game(winrate):
            wins += 1
        else:
            looses += 1
        if wins == 7 or looses == 3:
            rewards = Draft.reward[wins]
            Diamonds += rewards
            wins, looses = 0, 0 
            break


  