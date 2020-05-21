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
                os.system('cls')
                games_amount = input("Enter desired experience of ANN"
                                     "(games amount): ")
                games_amount = int(games_amount)
                try:
                    self.create_new_ANN_instance(games_amount)
                except KeyboardInterrupt:

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


    def create_new_ANN_instance(self, games_amount):
        """
        Create new instance of ANN and start machine learning
        process of entered number of games.
        """
        new_ANN = Net()

        count = 0
        wins = 0

        while count < games_amount:
            count += 1
            print("Game #:{}".format(count))
            g = Game.Game()

            # print("White player rolled {}, Black player rolled {}".format(p1Roll[0] + p1Roll[1], p2Roll[0] + p2Roll[1]))
            p1Roll = (0,0)
            p2Roll = (0,0)
            while sum(p1Roll) == sum(p2Roll):
                p1Roll = g.roll_dice()
                p2Roll = g.roll_dice()

            if sum(p1Roll) > sum(p2Roll):
                print("White player gets the first turn...")
                g.turn = g.players[0]
            else:
                print("Black player gets the first turn")
                g.turn = g.players[1]
            start = 1
            moves = 0
            states = []

            while not g.game_over():
                actions = []

                if start == 1:
                    actions = g.find_moves(p1Roll, g.turn)
                    start = 0
                else:
                    actions = g.find_moves(g.roll_dice(), g.turn)

                if len(actions) > 0:
                    values = []

                    # Find the action with the most appealing value
                    for action in actions:
                        g.take_action(g.turn, action)
                        representation = g.get_representation(g.board, g.players, g.on_bar, g.off_board, g.turn)
                        values.append(new_ANN.getValue(representation))
                        # Undo the action and try the rest
                        g.undo_action(g.turn, action)

                    # We want white to win so find the max for white and the smallest for black
                    max = 0
                    max_index = 0
                    min = 1
                    min_index = 0
                    for i in range(0, len(values)):
                        if g.turn == 'white':
                            if max < values[i][0]:
                                max = values[i][0]
                                max_index = i
                        elif g.turn == 'black':
                            if min > values[i][1]:
                                min = values[i][1]
                                min_index = i
                    if g.turn == 'white':
                        best_action = actions[max_index]
                    else:
                        best_action = actions[min_index]

                    # Take the best action
                    g.take_action(g.turn, best_action)

                    # Get the representation
                    expected_board = g.get_representation(g.board, g.players, g.on_bar, g.off_board, g.turn)
                    if g.turn == 'white':
                        # Save the state
                        states.append(expected_board)
                        # print(new_ANN.getValue(expected_board))
                        # print('state size',len(states))
                    # Swap turns and increment move count
                    moves += 1
                    g.turn = g.get_opponent(g.turn)
                    reward = 0
                    if g.game_over():
                        print("Game over in {} moves".format(moves))
                        print("Num states: ", len(states))
                        print("{} won".format(g.find_winner()))

                        if g.find_winner() == 'white':
                            reward = 1
                            wins += 1
                        for i in range(len(g.board)):
                            g.print_point(i)

            # Build the eligibility trace with the list of states white has accumulated
            new_ANN.learn(states)

            print("Win percentage: {}".format(wins/count))
        new_ANN.save(count)


    def continue_machine_learning(self):
        """
        Continue process of machine learning on choosen ANN with
        additional entered number of games.
        """
        pass


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
