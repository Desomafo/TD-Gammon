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


    def __init__(self):
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
        self.more_than_one_network_instance = False
        self.display_menu()

        # Main control cycle of programm
        while True:
            choosen_option = input("\nEnter option number: ")
            print()
            if choosen_option == 'x':
                break
            elif choosen_option == '1':
                self.create_new_ANN_instance()
            elif choosen_option == '2':
                self.continue_machine_learning()
            elif choosen_option == '3':
                self.get_hint()
            elif choosen_option == '4':
                self.watch_ANNs_play()
            elif choosen_option == '5':
                self.compare_two_ANNs()
            elif choosen_option == '6':
                self.start_game_from_example()
            elif choosen_option == '7':
                self.play_with_ANN()


    def display_menu(self):
        """
        Print available actions.
        """
        print("Backgammon game using TD-Gammon")
        print("Available options:")

        out_str = "\t{}. {}"
        if self.more_than_one_network_instance == True:
            for number, option in enumerate(self.options):
                print(out_str.format(number, option))
        else:
            print(out_str.format(1, self.options[0]))

        print("\nEnter option number to continue")
        print("Press X to exit")


    def create_new_ANN_instance(self):
        """
        Create new instance of ANN and start machine learning
        process of entered number of games.
        """
        pass


    def continue_machine_learning(self):
        """
        Continue process of machine learning on choosen ANN with
        additional entered number of games.
        """
        pass


    def get_hint(self):
        pass


    def compare_two_ANNs(self):
        pass


    def start_game_from_example(self):
        pass

    
    def play_with_ANN(self):
        pass


if __name__ == '__main__':
    Interface()
