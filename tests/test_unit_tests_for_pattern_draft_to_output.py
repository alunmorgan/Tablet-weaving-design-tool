from from_pattern_draft import pattern_draft_to_output
import unittest


class TestCardInstantiation(unittest.TestCase):

    def setUp(self):
        self.expected_thread_colours = ['RRR', 'BBB', 'YYY', 'WWW']
        self.expected_thread_types = ['CCC', 'CCC', 'CCC', 'CCC']
        self.expected_number_of_holes = 4

    def test_passes_with_expected_input(self):
        thread_dirs = ['LTR', 'RTL', 'ltr', 'rtl']  # All the valid inputs for threading direction.
        for thread_dir in thread_dirs:
            test_card = pattern_draft_to_output.Card(number_of_holes=self.expected_number_of_holes,
                                                     threading_direction=thread_dir,
                                                     list_of_thread_colours=self.expected_thread_colours,
                                                     list_of_thread_types=self.expected_thread_types
                                                     )
            self.assertEqual(test_card.N_holes, self.expected_number_of_holes)
            self.assertEqual(test_card.thread_direction, thread_dir)
            self.assertListEqual(test_card.thread_cols, self.expected_thread_colours)
            self.assertListEqual(test_card.thread_types, self.expected_thread_types)

    def test_raises_TypeError_with_not_int_for_number_of_holes (self):
        self.assertRaises(TypeError,
                          pattern_draft_to_output.Card, number_of_holes='4',
                          threading_direction='LTR',
                          list_of_thread_colours=self.expected_thread_colours,
                          list_of_thread_types=self.expected_thread_types
                          )

    def test_raises_TypeError_with_not_str_for_threading_direction(self):
        self.assertRaises(TypeError,
                          pattern_draft_to_output.Card, number_of_holes=self.expected_number_of_holes,
                          threading_direction=['LTR'],
                          list_of_thread_colours=self.expected_thread_colours,
                          list_of_thread_types=self.expected_thread_types
                          )

    def test_raises_ValueError_with_incorrect_str_for_threading_direction(self):
        self.assertRaises(ValueError,
                          pattern_draft_to_output.Card, number_of_holes=self.expected_number_of_holes,
                          threading_direction='AAA',
                          list_of_thread_colours=self.expected_thread_colours,
                          list_of_thread_types=self.expected_thread_types
                          )

    def test_raises_ValueError_with_incorrect_length_for_list_of_thread_colours(self):
        self.assertRaises(ValueError,
                          pattern_draft_to_output.Card, number_of_holes=self.expected_number_of_holes,
                          threading_direction='LTR',
                          list_of_thread_colours=['RRR', 'BBB', 'YYY'],
                          list_of_thread_types=self.expected_thread_types
                          )
        self.assertRaises(ValueError,
                          pattern_draft_to_output.Card, number_of_holes=self.expected_number_of_holes,
                          threading_direction='LTR',
                          list_of_thread_colours=['RRR', 'BBB', 'YYY', 'WWW', 'XXX'],
                          list_of_thread_types=self.expected_thread_types
                          )

    def test_raises_ValueError_with_incorrect_length_for_list_of_thread_types(self):
        self.assertRaises(ValueError,
                          pattern_draft_to_output.Card, number_of_holes=self.expected_number_of_holes,
                          threading_direction='LTR',
                          list_of_thread_colours=self.expected_thread_colours,
                          list_of_thread_types=['CCC', 'CCC', 'CCC']
                          )
        self.assertRaises(ValueError,
                          pattern_draft_to_output.Card, number_of_holes=self.expected_number_of_holes,
                          threading_direction='LTR',
                          list_of_thread_colours=self.expected_thread_colours,
                          list_of_thread_types=['CCC', 'CCC', 'CCC', 'CCC', 'XXX']
                          )


class TestCardFunctions(unittest.TestCase):
    def setUp(self):
        self.test_card = pattern_draft_to_output.Card(number_of_holes=4,
                                                      threading_direction='LTR',
                                                      list_of_thread_colours=['Red', 'Blue', 'Yellow', 'White'],
                                                      list_of_thread_types=['cotton', 'cotton', 'cotton', 'cotton']
                                                      )

    def test_raises_typeerror_with_str_input(self):
        self.assertRaises(TypeError, self.test_card.turn_card, direction='AAA')

    def test_passes_with_int_input(self):
        self.test_card.turn_card(1)

    def test_raises_typeerror_with_float_input(self):
        self.assertRaises(TypeError, self.test_card.turn_card, direction=1.111)

    def test_neutral_to_away_gives_expected_behaviour(self):
        # Top should go from 0 to 0
        # Bottom should go from 1 to 2
        self.test_card.turn_card(1)
        self.assertEqual(self.test_card.visible_top, 0)
        self.assertEqual(self.test_card.visible_bottom, 2)

    def test_neutral_to_towards_gives_expected_behaviour(self):
        # Top should go from 0 to 3
        # Bottom should go from 1 to 1
        self.test_card.turn_card(-1)
        self.assertEqual(self.test_card.visible_top, 3)
        self.assertEqual(self.test_card.visible_bottom, 1)

    def test_away_to_away_gives_expected_behaviour(self):
        # Top should go from 0 to 0 then to 1
        # Bottom should go from 1 to 2 then to 3
        self.test_card.turn_card(1)
        self.test_card.turn_card(1)
        self.assertEqual(self.test_card.visible_top, 1)
        self.assertEqual(self.test_card.visible_bottom, 3)

    def test_towards_to_towards_gives_expected_behaviour(self):
        # Top should go from 0 to 3 then to 2
        # Bottom should go from 1 to 1 then to 0
        self.test_card.turn_card(-1)
        self.test_card.turn_card(-1)
        self.assertEqual(self.test_card.visible_top, 2)
        self.assertEqual(self.test_card.visible_bottom, 0)

    def test_towards_to_away_gives_expected_behaviour(self):
        # Both should stay the same over the reversal
        # Top should go from 0 to 3 then to 2 and then to 2
        # Bottom should go from 1 to 1 then to 0 and then to 0
        self.test_card.turn_card(-1)  # Neutral --> Towards
        self.test_card.turn_card(-1)  # Towards --> Towards
        self.test_card.turn_card(1)   # Towards --> Away
        self.assertEqual(self.test_card.visible_top, 2)
        self.assertEqual(self.test_card.visible_bottom, 0)

    def test_away_to_towards_gives_expected_behaviour(self):
        # Both should stay the same over the reversal
        # Top should go from 0 to 0 then to 1 and then to 1
        # Bottom should go from 1 to 2 then to 3 and then to 3
        self.test_card.turn_card(1)   # Neutral --> Away
        self.test_card.turn_card(1)   # Away --> Away
        self.test_card.turn_card(-1)  # Away --> Towards
        self.assertEqual(self.test_card.visible_top, 1)
        self.assertEqual(self.test_card.visible_bottom, 3)

    def test_raises_valueerror_with_neutral(self):
        # Top should go from 0 to 0
        # Bottom should go from 1 to 2
        self.assertRaises(ValueError, self.test_card.turn_card, 0)


class TestStackInitialisation(unittest.TestCase):
    def setUp(self):
        self.Input_data = {'Card_number_of_holes': 4,
                           'Threading_directions': ['LTR', 'LTR'],
                           'Thread_colours': [['Red', 'Blue', 'Yellow', 'White'], ['R', 'B', 'Y', 'W']],
                           'Thread_types': [['cotton', 'cotton', 'cotton', 'cotton'],
                                            ['cotton', 'cotton', 'cotton', 'cotton']]}

    def test_passes_with_expected_input(self):
        card_stack = pattern_draft_to_output.Stack(self.Input_data)
        self.assertEqual(len(card_stack.card_stack), 2)

    def test_stack_raises_typeerror_if_input_is_str(self):
        self.assertRaises(TypeError, pattern_draft_to_output.Stack, 'AAA')

    def test_stack_raises_typeerror_if_input_is_a_list(self):
        self.assertRaises(TypeError, pattern_draft_to_output.Stack, ['AAA'])

    def test_stack_raises_typeerror_if_input_is_int(self):
        self.assertRaises(TypeError, pattern_draft_to_output.Stack, 444)


class TestStackFunctions(unittest.TestCase):
    def setUp(self):
        self.Input_data = {'Card_number_of_holes': 4,
                           'Threading_directions': ['LTR', 'LTR'],
                           'Thread_colours': [['Red', 'Blue', 'Yellow', 'White'], ['R', 'B', 'Y', 'W']],
                           'Thread_types': [['cotton', 'cotton', 'cotton', 'cotton'],
                                            ['cotton', 'cotton', 'cotton', 'cotton']]}
        self.card_stack = pattern_draft_to_output.Stack(self.Input_data)

    def test_turn_card_set_errors_with_cards_int(self):
        self.assertRaises(TypeError, self.card_stack.turn_card_set, 7, 1)

    def test_turn_card_set_errors_with_cards_float(self):
        self.assertRaises(TypeError, self.card_stack.turn_card_set, 7.7, 1)

    def test_turn_card_set_errors_with_cards_str(self):
        self.assertRaises(TypeError, self.card_stack.turn_card_set, '7', 1)

    def test_turn_card_set_errors_with_cards_greater_than_stack_length(self):
        self.assertRaises(ValueError, self.card_stack.turn_card_set, [0, 1, 2], 1)

    def test_turn_card_set_errors_with_cards_negative(self):
        self.assertRaises(ValueError, self.card_stack.turn_card_set, [-1, 0, 1], 1)

    def test_turn_card_set_away(self):
        self.card_stack.turn_card_set([1], 1)

    def test_turn_card_set_towards(self):
        self.card_stack.turn_card_set([1], -1)

    def test_turn_all_cards_away(self):
        self.card_stack.turn_all_cards(1)

    def test_turn_all_cards_towards(self):
        self.card_stack.turn_all_cards(-1)

    def test_weft(self):
        top_cols, top_typs, bottom_cols, bottom_typs = self.card_stack.weft()
        self.assertEqual(top_cols, ['Red', 'R'])
        self.assertEqual(top_typs, ['cotton', 'cotton'])
        self.assertEqual(bottom_cols, ['Blue', 'B'])
        self.assertEqual(bottom_typs, ['cotton', 'cotton'])


if __name__ == '__main__':
    unittest.main()
