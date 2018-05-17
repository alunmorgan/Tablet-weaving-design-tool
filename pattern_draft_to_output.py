

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
        self.visible_top = 0  # Starting location of top visible thread.
        self.visible_bottom = 1  # Starting location of bottom visible thread.
        self.prev_turn = 0  # 0 is neutral, away is 1 and towards is -1

    def turn_card(self, direction):
        if not isinstance(direction, int):
            raise(TypeError, 'The direction needs to be an integer (Away=1 Towards=-1)')

        if direction != 1 and direction != -1:
            raise(ValueError, 'The direction needs to be 1 or -1 (Away, Towards)')

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


card1 = Card(number_of_holes=4,
             threading_direction='LTR',
             list_of_thread_colours=['Red', 'Red', 'Yellow', 'White'],
             list_of_thread_types=['cotton', 'cotton', 'cotton', 'cotton']
             )
