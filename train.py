import os

from Game import Game
from net import Net

from play import parse_game

from glob import glob
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
        self.ANN_instances = self.scan_ANN_instances()
        if len(ANN_instances) > 1:
            self.more_than_one_network_instance = True
        else:
            self.more_than_one_network_instance = False


        # Main control cycle of programm
        while True:
            self.display_menu()
            choosen_option = input("\nEnter option number: ")
            print()
            if choosen_option == 'x':
                break
            elif choosen_option == '1':
                os.system('cls')
                games_amount = input("Enter desired experience of ANN"
                                     "(games amount): ")
                games_amount = int(games_amount)
                self.create_new_ANN_instance(games_amount)

            elif choosen_option == '2':
                os.system('cls')
                for instance in self.scan_ANN_instances():
                    print()
                games_amount = input("Enter desired additional experience of ANN"
                                     "(games amount): ")
                games_amount = int(games_amount)
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


    def create_new_ANN_instance(self, games_amount):
        """
        Create new instance of ANN and start machine learning
        process of entered number of games.
        """
        new_ANN = Net()
        continue_machine_learning(new_ANN, games_amount)

    def continue_machine_learning(self, ANN_instance, games_amount):
        """
        Continue process of machine learning on choosen ANN with
        additional entered number of games.
        """

        count = 0
        wins = 0

        try:
            while count < games_amount:
                count += 1
                print("Game #:{}".format(count))
                g = Game()
                winner, states = g.play(new_ANN)
                if winner == 'white':
                    wins += 1
                # Build the eligibility trace with the list of states white has accumulated
                ANN_instance.learn(states)
        except KeyboardInterrupt:
            pass
        print("Win percentage: {}".format(wins/count))
        ANN_instance.save(count)


    def scan_ANN_instances(self):
        """
        Scan created instances in data folder.
        """
        return [f for f in glob("data\*.pkl")]


    def get_hint(self):
        """
        Get hint for one turn for given board state.
        """
        pass


    def compare_two_ANNs(self):
        """
        Two given instances of ANN will play against each other for
        entered amount of games. Result is win percentage for first
        choosen network.
        """
        pass


    def start_game_from_example(self):
        """
        Start playing game from given board state. Than pass control
        to third or seventh options.
        """
        pass

    
    def play_with_ANN(self):
        """
        Start playing against choosen ANN. GIU option only.
        """
        pass


if __name__ == '__main__':
    Interface()
