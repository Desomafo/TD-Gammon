import time
import copy
import sys

import Game
import net

from play import parse_game

from datetime import datetime
from openpyxl import Workbook


global count, wins


def play_game(worksheet, by_example=False):
    global count, wins
    g = Game.Game()

    start = 1

    if by_example:
        g.set_game_state(parse_game(example_name))
        start = 0
    else:
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


    moves = 0
    states = []
    dice_rolls = []

    while not g.game_over():
        actions = []
        dice_roll = ()

        if start == 1:
            actions = g.find_moves(p1Roll, g.turn)
            dice_rolls.append(p1Roll)
            start = 0
        else:
            dice_roll = g.roll_dice()
            actions = g.find_moves(dice_roll, g.turn)
            dice_rolls.append(dice_roll)

        if len(actions) > 0:
            values = []

            # Find the action with the most appealing value
            for action in actions:
                g.take_action(g.turn, action)
                representation = g.get_representation(g.board, g.players, g.on_bar, g.off_board, g.turn)
                values.append(net.getValue(representation)[0])
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
            print("Best action for {}: {}, with roll {}".format(g.turn, best_action, dice_roll))

            # Take the best action
            g.take_action(g.turn, best_action)

            # Get the representation
            expected_board = g.get_representation(g.board, g.players, g.on_bar, g.off_board, g.turn)
            if g.turn == 'white':
                # Save the state
                states.append(expected_board)
                # print(net.getValue(expected_board))
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
    ws = worksheet
    for i in range(0, len(states) - 2):

            for j in range(len(states[i])):
                ws.cell(row=i+1, column=j+1).value = states[i][j]
            ws.cell(row=i+1, column=200).value = str(dice_rolls[i])

            # Feed in current state and the next state
            # the eligibility is based on states t and t+1
            current_state = states[i]
            predicted_state = states[i+1]

            # Optimazation to save getValue(current_state)
            repr_of_current_state = net.getValue(current_state)
            hidden_layer_results = repr_of_current_state[1]['hidden_layer']
            for j in range(len(hidden_layer_results)):
                ws.cell(row=i+1, column=202+j).value = hidden_layer_results[j]

            output_layer_results = repr_of_current_state[1]['output_layer']
            for j in range(len(output_layer_results)):
                ws.cell(row=i+1, column=203+len(hidden_layer_results)+j).value = output_layer_results[j]
            
            value_of_current_state = repr_of_current_state[0]
            error = net.getValue(predicted_state)[0][0] - value_of_current_state[0]

            if learn_key:
                net.feedforward(current_state)
                net.do_td(current_state, value_of_current_state, error)

    print("Win percentage: {}".format(wins/count))


if __name__ == '__main__':
    global net
    net = net.Net()

    count = 0
    wins = 0

    global weights_load_key, example_key, learn_key
    learn_key = True

    global example_name

    print(sys.argv)
    time_now = datetime.now()

    if 'l' in sys.argv[1]:
        print("Entered l flag")
        weights_load_key = True
        net.load()

    if 's' in sys.argv[1]:
        print("Entered s flag")
        learn_key = False

    if 'e' in sys.argv[1]:
        print("Entered e flag")
        count += 1
        if (len(argv) > 1):
            example_name = sys.argv[2]
        else:
            example_name = 'example.xlxs'

        wb = Workbook()
        ws = wb.active
        ws.title = '1'
        play_game(ws, true)
        net.save()
    else:
        while count < 3:
            time_now = datetime.now()

            count += 1
            print("Game #:{}".format(count))

            wb = Workbook()
            ws = wb.active
            ws.title = 'Weights'

            for i, row in enumerate(net.input_weights):
                for j, cell in enumerate(row):
                   ws.cell(row=i+1, column=j+1).value = cell 

            for i, row in enumerate(net.hidden_weights):
                for j, cell in enumerate(row):
                   ws.cell(row=i+2+len(net.input_weights), column=j+1).value = cell 

            ws = wb.create_sheet('Net output')
            play_game(ws)
            wb.save("data/inputs{} : {:%d, %b %Y, %H:%M}.xlsx".format(count,time_now))
            net.save()

            
    
