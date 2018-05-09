

class Card:

    def __init__(self, number_of_holes, list_of_thread_colours, list_of_thread_types, list_of_threading_directions):
        self.N_holes = number_of_holes
        self.thread_cols = list_of_thread_colours
        self.thread_types = list_of_thread_types
        self.thread_direction = list_of_threading_directions
        self.visible_top = 0
        self.visible_bottom = 1

    def turn_card(self, direction):
        pass

    def flip_card(self):
        pass


card1 = Card(number_of_holes=4,
             list_of_thread_colours=['Red', 'Red', 'Yellow', 'White'],
             list_of_thread_types=['cotton', 'cotton', 'cotton', 'cotton'],
             list_of_threading_directions=['Forward', 'Forward', 'Forward', 'Forward']
             )
