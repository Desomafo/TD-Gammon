import os
import pickle

from Game import Game
from net import Net

from play import parse_game

from glob import glob
from datetime import datetime
from matplotlib import pyplot


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
                "Compare two ANNs",
                "Compare all ANNs to most experienced",
                "Search for old examples",
                ]


        # Main control cycle of programm
        while True:
            
            self.ANN_instances = self.scan_ANN_instances()
            if len(self.ANN_instances) > 1:
                self.more_than_one_network_instance = True
            else:
                self.more_than_one_network_instance = False
                
            os.system('cls')
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
                print("Choose what ANN you want to continue to train:\n")
                self.display_existing_ANN_instances()

                instances = self.scan_ANN_instances()
                choosen_instance_number = int(input("Enter instance number: "))
                choosen_instance_name = instances[choosen_instance_number-1]
                with open(choosen_instance_name, 'rb') as pi:
                    ANN_instance = pickle.load(pi)
                games_amount = input("Enter desired additional experience of ANN"
                                     "(games amount): ")
                games_amount = int(games_amount)
                self.continue_machine_learning(ANN_instance, games_amount)

            elif choosen_option == '3':
                os.system('cls')
                answer = input("Enter 'y' is you made your setup in example.xlsx.\n"
                               "Overwise press 'n'.")
                if answer == 'n':
                    continue
                elif answer == 'y':
                    self.display_existing_ANN_instances()
                    instances = self.scan_ANN_instances()
                    choosen_instance_number = int(input("Enter instance number: "))
                    choosen_instance_name = instances[choosen_instance_number-1]
                    with open(choosen_instance_name, 'rb') as pi:
                        ANN_instance = pickle.load(pi)

                    print("Next move - {}".format(self.get_hint(ANN_instance)))
                    
            elif choosen_option == '4':
                os.system('cls')
                self.display_existing_ANN_instances() 

                instances = self.scan_ANN_instances()
                numbers_str = input("Enter two numbers of instances "
                                    "to compare (* *): ")
                numbers = numbers_str.split(' ')
                first_instance_name = instances[int(numbers[0])-1]
                second_instance_name = instances[int(numbers[1])-1]
                
                with open(first_instance_name, 'rb') as pi:
                    first_instance = pickle.load(pi)
                with open(second_instance_name, 'rb') as pi:
                    second_instance = pickle.load(pi)

                games_amount = input("Enter amount of games to compare (games amount): ")
                games_amount = int(games_amount)

                stats = self.compare_two_ANNs(first_instance, second_instance,
                                              games_amount)
                print(stats)

            elif choosen_option == '5':
                games_amount = input("Enter amount of games to compare (games amount): ")
                games_amount = int(games_amount)
                stats = self.compare_ANNs_with_most_experienced(games_amount)

                pyplot.plot(stats[0], stats[1])
                pyplot.show()
                
                print(stats)

            elif choosen_option == '6':
                self.search_for_xlsx_instances('data//November')

            input("Press any key to continue...")


    def display_menu(self):
        """
        Print available actions.
        """
        print("Backgammon game using TD-Gammon")
        print("Available options:")

        out_str = "\t{}. {}"
        if self.more_than_one_network_instance == True:
            for number, option in enumerate(self.options, 1):
                print(out_str.format(number, option))
        else:
            print(out_str.format(1, self.options[0]))

        print("\nEnter option number to continue")
        print("Press X to exit")


    def display_existing_ANN_instances(self):
        for n, instance_file_name in enumerate(self.scan_ANN_instances(), 1):
            instance_props = instance_file_name.split('_')
            instance_props[0] = instance_props[0][5:]
            instance_props[-1] = instance_props[-1][:3]
            print(f"{n}.\t{instance_props[0]} - experience")
            print(f"\t{instance_props[5][1:]}:{instance_props[6][1:]} - "
                  f"{instance_props[1]}/{instance_props[2]}/{instance_props[3]}"
                  " - creation date")
            print("--------------------------------------------")


    def create_new_ANN_instance(self, games_amount):
        """
        Create new instance of ANN and start machine learning
        process of entered number of games.
        """
        new_ANN = Net()
        self.continue_machine_learning(new_ANN, games_amount)


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
                g = Game(ANN_instance, None, True)
                winner, states = g.play()
                if winner == 'white':
                    wins += 1
                # Build the eligibility trace with the list of states white has accumulated
                ANN_instance.learn(states)
        except KeyboardInterrupt:
            pass
        print("Win percentage: {}".format(wins/count))
        ANN_instance.save()


    def scan_ANN_instances(self):
        """
        Scan created instances in data folder.
        """
        return [f for f in glob("data\*.pkl")]


    def get_hint(self, ANN_instance):
        """
        Get hint for one turn for given board state.
        """
        g = Game(ANN_instance)
        g.parse_game('example.xlsx')
        best_action = g.find_best_action(g.find_moves(g.roll, g.turn))
        best_action = (best_action[0]+1, best_action[1]+1)
        return best_action


    def compare_two_ANNs(self, first_instance, second_instance, games_amount):
        """
        Two given instances of ANN will play against each other for
        entered amount of games. Result is win percentage for first
        choosen network.
        """

        count = 0
        wins = 0
        stats = []
        while count < games_amount:
            count += 1
            print("Game #:{}".format(count))
            g = Game(first_instance, second_instance)
            winner, _ = g.play()
            if winner == 'white':
                wins += 1
            stats.append(wins/count)

        return stats


    def compare_ANNs_with_most_experienced(self, games_amount):
        """
        Compare all ANN instances to most experienced of them.
        """

        count = 0
        wins = 0
        stats = []
        ANN_files = self.scan_ANN_instances()
        with open(ANN_files[-1], 'rb') as most_experienced_file:
            most_experiensed_ANN = pickle.load(most_experienced_file)
            for ANN_instance_name in ANN_files:
                with open(ANN_instance_name, 'rb') as pi:
                    ANN_instance = pickle.load(pi)
                    while count < games_amount:
                        count += 1
                        print("Game #:{}".format(count))
                        g = Game(ANN_instance, most_experiensed_ANN)
                        winner, _ = g.play()
                        if winner == 'white':
                            wins += 1
                        stats.append([ANN_instance.games_amount_experience, wins/count])

        return stats


    def search_for_xlsx_instances(self, dirrectory):
        """
        Search and parse all instances from xlsx files that were
        created in November last year.
        """
        xlsx_file_names = glob(dirrectory + '//*.xlsx')
        for file_name in xlsx_file_names:
            new_instance = Net()
            new_instance.parse_weights_from_xlsx(file_name)
            new_instance.save()
        
        print("Search and creation are finished")
        return len(xlsx_file_names)





if __name__ == '__main__':
    Interface()
