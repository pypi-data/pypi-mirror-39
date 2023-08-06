from enum import Enum, auto
import random
import sys

class Moves(Enum):
    '''each possible move is created'''
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()
    LIZARD = auto()
    SPOCK = auto()
    SPIDERMAN = auto()
    BATMAN = auto()
    WIZARD = auto()
    GLOCK = auto()


###vital dictionary for determining winner
WEAKNESS_LOOKUP = {
    Moves.ROCK: [Moves.SCISSORS, Moves.SPIDERMAN, Moves.LIZARD, Moves.WIZARD],
    Moves.PAPER: [Moves.ROCK, Moves.SPOCK, Moves.GLOCK, Moves.BATMAN],
    Moves.SCISSORS: [Moves.PAPER, Moves.SPIDERMAN, Moves.WIZARD, Moves.LIZARD],
    Moves.LIZARD: [Moves.PAPER, Moves.SPOCK, Moves.GLOCK, Moves.BATMAN],
    Moves.SPOCK: [Moves.ROCK, Moves.SPIDERMAN, Moves.WIZARD, Moves.SCISSORS],
    Moves.SPIDERMAN: [Moves.LIZARD, Moves.WIZARD, Moves.GLOCK, Moves.PAPER],
    Moves.BATMAN: [Moves.SPOCK, Moves.SPIDERMAN, Moves.SCISSORS, Moves.ROCK],
    Moves.WIZARD: [Moves.PAPER, Moves.BATMAN, Moves.GLOCK, Moves.LIZARD],
    Moves.GLOCK: [Moves.SCISSORS,Moves.ROCK,Moves.BATMAN, Moves.SPOCK]
    
    }
###dict provides description of the matchup between moves
DESC_LOOKUP = {
    'PAPER SCISSORS':'Scissor cuts Paper',
    'PAPER ROCK':'Paper covers Rock',
    'LIZARD ROCK':'Rock crushes Lizard',
    'LIZARD SPOCK':'Lizard poisons Spock',
    'SPOCK WIZARD':'Spock zaps Wizard',
    'BATMAN WIZARD':'Wizard stuns Batman',
    'BATMAN SPIDERMAN':'Batman scares Spiderman',
    'GLOCK SPIDERMAN':'Spiderman disarms Glock',
    'GLOCK ROCK':'Glock breaks Rock',
    'ROCK WIZARD':'Rock interupts Wizard',
    'PAPER WIZARD':'Wizard burns Paper',
    'PAPER SPOCK':'Paper disproves Spock',
    'SPIDERMAN SPOCK':'Spock befuddles Spiderman',
    'LIZARD SPIDERMAN':'Spiderman defeats Lizard',
    'BATMAN LIZARD':'Lizard confuses Batman',
    'BATMAN SCISSORS':'Batman dismantles Scissors',
    'SCISSORS WIZARD':'Scissors cut Wizard',
    'LIZARD WIZARD':'Wizard transorms Lizard',
    'LIZARD PAPER':'Lizard eats Paper',
    'GLOCK PAPER':'Paper jams Glock',
    'BATMAN GLOCK':'Glock kills Batmans mum :(',
    'BATMAN ROCK':'Batman explodes Rock',
    'ROCK SCISSORS':'Rock crushes Scissors',
    'LIZARD SCISSORS':'Scissors decapitate Lizard',
    'GLOCK LIZARD':'Lizard is too small for Glock',
    'GLOCK SPOCK':'Glock shoots Spock',
    'ROCK SPOCK':'Spock vaporizes Rock',
    'ROCK SPIDERMAN':'Rock KOs Spiderman',
    'PAPER SPIDERMAN':'Spiderman rips Paper',
    'BATMAN PAPER':'Paper delays Batman',
    'BATMAN SPOCK':'Batman hangs Spock',
    'SCISSORS SPOCK':'Spock smashes Scissors',
    'SCISSORS SPIDERMAN':'Scissors cut Spiderman',
    'SPIDERMAN WIZARD':'Spiderman annoys Wizard',
    'GLOCK WIZARD':'Wizard melts Glock',
    'GLOCK SCISSORS':'Glock dents Scissors'
    
    
    
    }

###score starts at zero 
score = {'human':0,'robot':0}

class Outcome(Enum):
    '''each outcome of matchups is defined'''
    TIE = auto()
    WON = auto()
    LOST = auto()

def determine_game_outcome(player_move, computer_move):
    """Function provides the result of each round

        Args:
            player_move: weapon selection of human.
            computer_move: weapon selection of robot.

        Returns:
            win / lose / tie .

    """
    if computer_move in WEAKNESS_LOOKUP[player_move]:
        score['human'] += 1
        return Outcome.WON
    elif player_move in WEAKNESS_LOOKUP[computer_move]:
        score['robot'] += 1
        return Outcome.LOST
    else:
        return Outcome.TIE
    

def get_description(player_move, computer_move):
    """Function provides the description of each round

        Args:
            player_move: weapon selection of human.
            computer_move: weapon selection of robot.

        Returns:
            string of the description of the round result .
                e.g Rock smashes Scissors
                Note if the human / robot moves are the same it returns generic message

    """
    if player_move == computer_move:
        return 'OH SNAP '
    else:
        return DESC_LOOKUP[' '.join(sorted([player_move.name, computer_move.name]))]
    

    
def play():
        """Function is the main driver behind the game 

        Args:
            None 

        Returns:
            results of the computer random choice, result and description
            at the end of each round player is asked if want to continue

        """
        computer = computer_move()
        player = player_move()
        print("You play {} Robot plays {}".format(player.name, computer.name))
        print("{} - Result : {}".format(get_description(player,computer), determine_game_outcome(player, computer).name))
        print(score)
        again = str(input("Do you want to play again (type Y / N): ")).lower()
        if again == "y":
            play()
        else:
            sys.exit(0)


def computer_move():
    """Function provides the computers weapon choice

        Args:
            None

        Returns:
            random weapon choice from Move class

    """
    return random.choice(list(move for move in Moves))
        

def player_move():
    """Function provides the human input weapon choice

        Args:
            typed input of weapon

        Returns:
            matching class attr

    """
    print("Choose your weapon - ROCK, PAPER, SCISSORS, LIZARD, SPOCK, SPIDERMAN, BATMAN, WIZARD or GLOCK")
    choice = input(">:").upper()
    return getattr(Moves,choice)
    
play()    