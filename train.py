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
    

    class Option:

        def __init__(self, name, is_dependent):
            self.name = name
            self.network_availability_dependent = is_dependent


    def __init__(self, keys):
        display_menu()
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
            

    
