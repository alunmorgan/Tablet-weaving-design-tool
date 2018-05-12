import pattern_draft_to_output
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