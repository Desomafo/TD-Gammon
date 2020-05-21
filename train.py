import time
import copy
import sys

import Game
import net

from play import parse_game

from datetime import datetime
from openpyxl import Workbook

class Interface:
    """
    Class for using neural network for one gaming session.
    Session can be with learning and without it.
    Use cases:
        - Play one game form given turn
        - Evaluate one turn
        - Play and reinforce network on any number of games
    """
    

    def __init__(self, keys):
        

    def play(self):
        """
        Play game with installed config.
        If configuration was not given new neural network will be created
        and will learn play with itself on 1000 games. 
        """



    def display_menu(self):
        """
        Print current state of config and available actions.
        """
        pass

    
