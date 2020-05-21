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
        # Forming list of all options
        self.options = [
                "Make a new instance of ANN",
                "Continue process of machine learning",
                "Get hint for one turn",
                "Watch ANN play",
                "Compare two ANNs",
                "Start game from example",
                "Play game with ANN",
                ]
        display_menu()

        # Main control cycle of programm
        while True:
            choosen_option = input("Enter option number")
            if choosen_option == 1:
                pass
            elif choosen_option == 2:
                pass
            elif choosen_option == 4:
                pass
            elif choosen_option == 5:
                pass
            elif choosen_option == 6:
                pass
            elif choosen_option == 7:
                pass


    def play(self):
        """
        Play game with installed config.
        If configuration was not given new neural network will be
        created and will learn play with itself on 1000 games. 
        """
        pass


    def display_menu(self):
        """
        Print available actions.
        """
        print("Backgammon game using TD-Gammon")
        print("Available options:")

        if more_than_one_network_instance == True:
            for number, option in enumerate(options.keys()):
                print(number, option)
        else:
            print(1, options[0])
