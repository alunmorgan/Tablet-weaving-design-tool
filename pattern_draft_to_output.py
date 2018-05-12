

class Card:

    def __init__(self, number_of_holes, threading_direction, list_of_thread_colours, list_of_thread_types):
        if type(number_of_holes) is not int:
            raise(TypeError, 'number of holes needs to be an int')
        if len(list_of_thread_colours) != number_of_holes:
            raise(ValueError, 'Incorrect number of thread colours assigned')
        if len(list_of_thread_types) != number_of_holes:
            raise(ValueError, 'Incorrect number of thread types assigned')
        if type(threading_direction) is not str:
            raise(TypeError, 'The threading direction needs to be a string')
        if threading_direction != 'LTR' and threading_direction != 'RTL' and \
           threading_direction != 'ltr' and threading_direction != 'rtl':
            raise(ValueError, 'The threading directions needs to be RTL or LTR')

        self.N_holes = number_of_holes
        self.thread_cols = list_of_thread_colours
        self.thread_types = list_of_thread_types
        self.thread_direction = threading_direction
        self.visible_top = 0
        self.visible_bottom = 1
        self.prev_turn = 0  # 0 is neutral, away is 1 and towards is -1

    def turn_card(self, direction):
        pass

    def flip_card(self):
        pass


card1 = Card(number_of_holes=4,
             threading_direction='LTR',
             list_of_thread_colours=['Red', 'Red', 'Yellow', 'White'],
             list_of_thread_types=['cotton', 'cotton', 'cotton', 'cotton']
             )
