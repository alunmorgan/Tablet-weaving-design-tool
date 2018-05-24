from from_pattern_draft.pattern_draft_to_output import Stack, accumulate_pattern

Input_data = {'Card_number_of_holes': 4,
              'Threading_directions': ['LTR', 'LTR'],
              'Thread_colours': [['Red', 'Blue', 'Yellow', 'White'], ['R', 'B', 'Y', 'W']],
              'Thread_types': [['cotton', 'cotton', 'cotton', 'cotton'], ['cotton', 'cotton', 'cotton', 'cotton']]}

Card_stack = Stack(Input_data)
Card_stack.turn_card_set([0, 1], 1)

top_pattern_colours = []
top_pattern_types = []
bottom_pattern_colours = []
bottom_pattern_types = []

top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types = \
    accumulate_pattern(Card_stack, top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types)
Card_stack.turn_card_set([0, 1], 1)
top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types = \
    accumulate_pattern(Card_stack, top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types)
Card_stack.turn_card_set([0, 1], 1)
top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types = \
    accumulate_pattern(Card_stack, top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types)
Card_stack.turn_card_set([0, 1], 1)
top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types = \
    accumulate_pattern(Card_stack, top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types)
Card_stack.turn_card_set([0, 1], 1)
top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types = \
    accumulate_pattern(Card_stack, top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types)
Card_stack.turn_card_set([0, 1], 1)
top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types = \
    accumulate_pattern(Card_stack, top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types)
Card_stack.turn_card_set([0, 1], 1)
top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types = \
    accumulate_pattern(Card_stack, top_pattern_colours, top_pattern_types, bottom_pattern_colours, bottom_pattern_types)

print(top_pattern_colours)

