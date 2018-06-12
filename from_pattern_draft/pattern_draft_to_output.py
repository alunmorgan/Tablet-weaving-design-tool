import json
import os
import tkinter
from tkinter import messagebox


class Card:

    def __init__(self, number_of_holes, threading_direction, list_of_thread_colours, list_of_thread_types):
        if type(number_of_holes) is not int:
            raise TypeError('number of holes needs to be an int')
        if len(list_of_thread_colours) != number_of_holes:
            raise ValueError('Incorrect number of thread colours assigned')
        if len(list_of_thread_types) != number_of_holes:
            raise ValueError('Incorrect number of thread types assigned')
        if type(threading_direction) is not str:
            raise TypeError('The threading direction needs to be a string')
        if threading_direction != 'LTR' and threading_direction != 'RTL' and \
           threading_direction != 'ltr' and threading_direction != 'rtl':
            raise ValueError('The threading directions needs to be RTL or LTR')

        self.N_holes = number_of_holes
        self.thread_cols = list_of_thread_colours
        self.thread_types = list_of_thread_types
        self.thread_direction = threading_direction
        self.visible_top = 0  # Starting location of top visible thread.
        self.visible_bottom = 1  # Starting location of bottom visible thread.
        self.prev_turn = 0  # 0 is neutral, away is 1 and towards is -1

    def turn_card(self, direction):
        if not isinstance(direction, int):
            raise TypeError('The direction needs to be an integer (Away=1 Towards=-1)')

        if direction != 1 and direction != -1:
            raise ValueError('The direction needs to be 1 or -1 (Away, Towards)')

        if direction == 1:
            if self.prev_turn == 1:  # Carrying on in the same direction.
                self.visible_top += 1
                self.visible_bottom += 1

            elif self.prev_turn == 0:  # Starting from neutral
                # Visible top remains the same
                self.visible_bottom += 1
            #  No need for the case where self.prev_turn == -1
            #  as the visibility of the threads remains the same over a reversal of direction
        elif direction == -1:
            if self.prev_turn == -1:  # Carrying on in the same direction.
                self.visible_top += -1
                self.visible_bottom += -1
            elif self.prev_turn == 0:  # Starting from neutral
                self.visible_top += -1
                # Visible bottom remains the same
            #  No need for the case where self.prev_turn == -1
            #  as the visibility of the threads remains the same over a reversal of direction

        # Wrap the values around so theya re always withing the range 0 - self.N_holes.
        self.visible_top = self.visible_top % self.N_holes
        self.visible_bottom = self.visible_bottom % self.N_holes
        self.prev_turn = direction

    def flip_card(self):
        pass


class Stack:

    def __init__(self, input_data):
        self.card_stack = {}

        for card_index in range(len(input_data['Threading_directions'])):
            self.card_stack['card%s' % card_index] = Card(number_of_holes=len(input_data['Thread_colours'][0]),
                                                          threading_direction=input_data['Threading_directions'][card_index],
                                                          list_of_thread_colours=input_data['Thread_colours'][card_index],
                                                          list_of_thread_types=input_data['Thread_types'][card_index]
                                                          )

    def turn_card_set(self, cards, direction):
        if not isinstance(cards, list):
            raise TypeError('The cards selection needs to be a list')
        if any([temp_card > len(self.card_stack) -1 for temp_card in cards]) or \
           any([temp_card < 0 for temp_card in cards]):
            raise ValueError('An invalid card has been selected')
        for card in cards:
            self.card_stack['card%s' % card].turn_card(direction)

    def turn_all_cards(self, direction):
        for card in range(len(self.card_stack)):  # Using index rather than keys directly so that I can set the order.
            self.card_stack['card%s' % card].turn_card(direction)

    def weft(self):
        """Reads and outputs the current state of the card stack"""
        top_cols = []
        top_typs = []
        bottom_cols = []
        bottom_typs = []
        for card_index in range(len(self.card_stack)):
            current_card = self.card_stack['card%s' % card_index]
            top_cols.append(current_card.thread_cols[current_card.visible_top])
            top_typs.append(current_card.thread_types[current_card.visible_top])
            bottom_cols.append(current_card.thread_cols[current_card.visible_bottom])
            bottom_typs.append(current_card.thread_types[current_card.visible_bottom])
        return top_cols, top_typs, bottom_cols, bottom_typs


def accumulate_pattern(input_data):
    top_pattern_colours = []
    top_pattern_types = []
    bottom_pattern_colours = []
    bottom_pattern_types = []

    card_stack = Stack(input_data)
    for turn_instruction in input_data['Turning_instructions'] + input_data['Turning_instructions']:
        if len(turn_instruction) == 1:
            card_stack.turn_all_cards(convert_turns_to_numeric(turn_instruction[0]))
        else:
            card_index = 0
            for individual_card in turn_instruction:
                card_stack.turn_card_set([card_index], convert_turns_to_numeric(individual_card))
                card_index += 1
        tc, tt, bc, bt = card_stack.weft()
        top_pattern_colours.append(tc)
        top_pattern_types.append(tt)
        bottom_pattern_colours.append(bc)
        bottom_pattern_types.append(bt)
    return {'top_cols': top_pattern_colours,
            'top_types': top_pattern_types,
            'bottom_cols': bottom_pattern_colours,
            'bottom_types': bottom_pattern_types}


def convert_turns_to_numeric(turn_string):
    if turn_string.casefold() == 'away'.casefold():
        return 1
    elif turn_string.casefold() == 'toward'.casefold() or turn_string.casefold() == 'towards'.casefold():
        return -1
    else:
        raise ValueError('Turn instructions must be away or toward(s)')


def import_data(data_location, data_file):
    input_file = open(os.path.join(data_location, "%s.json" % data_file))
    return json.load(input_file)


def export_data(input_data, save_location, save_name):
    full_path = os.path.join(save_location, "%s.json" % save_name)
    if os.path.exists(full_path):
        if messagebox.askyesno("File exists", "Would you like to overwrite the file?"):
            save_data_file(input_data, full_path)
            print("File saved: %s" % full_path)
        else:
            print('Save aborted by user')
    else:
        save_data_file(input_data, full_path)


def save_data_file(input_data, full_path):
    save_file = open(full_path, "w")
    json.dump(input_data, save_file, indent=4)
    save_file.close()
